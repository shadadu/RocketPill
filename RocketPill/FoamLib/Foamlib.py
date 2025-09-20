#!/usr/bin/env python3
"""
pressure_controller.py

Controller to run either simpleFoam (incompressible) or rhoPimpleFoam (compressible)
in parallel to drive the chamber (volume-averaged) pressure to a target time-series
loaded from a CSV (time_ms, pressure_Pa). The controller modifies the inlet U fixedValue
(using a proportional controller) and iterates short solver runs until the average
chamber pressure matches the target within tolerance.

Assumptions:
 - Case directory exists and contains a mesh (constant/polyMesh).
 - The chamber interior region in the mesh is tagged by a patch name (chamberWalls, inlet, outlet).
 - The inlet patch name in boundary files is "inlet".
 - The patch representing the chamber walls (where wall pressure is wanted) is named "chamberWall".
 - OpenFOAM commands are on PATH.
"""

import argparse

import shutil
import time
import os
import re
import math
import pandas as pd
from RocketPill.FoamLib.FoamObjects import ensure_functionObjects_in_controlDict
from RocketPill.FoamLib import Inputs
from RocketPill.FoamLib import Solver

# ------------ User-configurable params ------------
INNER_RUN_TIME = 0.05  # simulated time (s) or pseudo-step horizon per inner run (small)
MAX_ITERS = 12  # controller iterations per target timepoint
TOL_P = 1e3  # Pa tolerance for pressure tracking
KP = 5e-6  # proportional gain (change inlet U by Kp * pressure_error). Tuning required.


# Note: KP units depend on solver (incompressible: m/s per Pa roughly). Tune for your case.

# ------------ Helper functions ------------



def edit_fixedValue_U(case_dir, inlet_patch_name, newU):
    """
    Naively edit 0/U boundaryField: find 'inlet' patch and set value to the vector newU
    newU: tuple (Ux,Uy,Uz)
    """
    ufile = os.path.join(case_dir, "0", "U")
    if not os.path.exists(ufile):
        raise FileNotFoundError("0/U not found at: " + ufile)
    txt = open(ufile).read()
    # Very simple regex-based edit: locate "inlet { ... value   uniform ( x y z );"
    pattern = re.compile(r"(" + re.escape(inlet_patch_name) + r"\s*\{[^}]*?value\s+uniform\s*\([^\)]*\)\s*;)", re.S)
    m = pattern.search(txt)
    if not m:
        # try to find the inlet block start and modify its value line specifically
        pattern2 = re.compile(r"(" + re.escape(inlet_patch_name) + r"\s*\{)", re.S)
        m2 = pattern2.search(txt)
        if not m2:
            raise RuntimeError(f"Could not find patch block for '{inlet_patch_name}' in 0/U")
        # locate end of block by finding the closing '}' after m2.start()
        start = m2.start()
        # find next '}' from start
        end = txt.find("}", start)
        block = txt[start:end + 1]
        # replace or inject value uniform line
        if "value" in block:
            block2 = re.sub(r"value\s+uniform\s*\([^\)]*\)\s*;", f"value    uniform ({newU[0]} {newU[1]} {newU[2]});",
                            block)
        else:
            block2 = block.replace("{", "{\n    value    uniform (%g %g %g);\n" % newU)
        txt = txt[:start] + block2 + txt[end + 1:]
    else:
        old = m.group(1)
        newval = f"{inlet_patch_name} {{\n    type            fixedValue;\n    value           uniform ({newU[0]} {newU[1]} {newU[2]});\n}}"
        txt = txt[:m.start(1)] + newval + txt[m.end(1):]
    open(ufile, "w").write(txt)
    print(f"Set inlet U to {newU} in {ufile}")


def read_latest_postproc_field_average(case_dir, name):
    """
    Read postProcessing/<name>/<time>/... output produced by fieldAverage or surfaceFieldValue functionObjects.
    We look for postProcessing/<name>/<latestTime>/data or *.dat
    Returns numeric value (first scalar found).
    """
    ppdir = str(os.path.join(case_dir, "postProcessing", name))
    if not os.path.exists(ppdir):
        print("postProcessing dir not found for", name)
        return None
    times = sorted([d for d in os.listdir(ppdir) if os.path.isdir(os.path.join(ppdir, d))], key=float)
    if not times:
        print("No time directories under", ppdir)
        return None
    latest = times[-1]
    datdir = os.path.join(ppdir, latest)
    # find any .dat or .txt file
    files = [f for f in os.listdir(datdir) if f.endswith(".dat") or f.endswith(".txt") or f.endswith(".dat.gz")]
    if not files:
        files = os.listdir(datdir)
    if not files:
        print("No files in", datdir)
        return None
    filepath = os.path.join(datdir, files[0])
    txt = open(filepath).read()
    # try to parse first float in file
    m = re.search(r"([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)", txt)
    if not m:
        return None
    return float(m.group(1))


def run_decompose_par(case_dir, np_proc):
    decompDict = os.path.join(case_dir, "system", "decomposeParDict")
    if not os.path.exists(decompDict):
        print("Warning: system/decomposeParDict not found — creating a simple one.")
        dd = f"""/* simple decomposeParDict */
        numberOfSubdomains {np_proc};
        method          scotch;
        """
        open(decompDict, "w").write(dd)

    Solver.run_cmd(["decomposePar", "-case", case_dir, "-force"])

def reconstruct_par(case_dir):
    Solver.run_cmd(["reconstructPar", "-case", case_dir])


def extract_wall_patch_pressures(case_dir, wall_patch_name, out_csv="wall_pressure_last.csv"):
    """
    This reads the latest time p field patch values using the OpenFOAM sampling utility.
    We'll use 'postProcess -func patchAverage' but to get full distribution we can call the 'sample' utility:
      sample -case case -time <latestTime>
    However sample needs a sampleDict. Here, a quick approach is to call the sample utility configured by system/sampleDict.
    For brevity, we will attempt to read postProcessing/patchAverage_chamberWall which contains average; full face-by-face export may require a custom sampleDict.
    """
    patch_avg = read_latest_postproc_field_average(case_dir, "patchAverage_chamberWall")
    if patch_avg is None:
        print(
            "No patch average file found. To extract face-wise pressures, add a 'sample' utility sampleDict configured to write patch surfaces.")
        return None
    # Write a simple CSV with a single averaged value for now.
    open(os.path.join(case_dir, out_csv), "w").write("avg_wall_pressure_Pa\n%g\n" % patch_avg)
    print("Wrote averaged chamber wall pressure to", os.path.join(case_dir, out_csv))
    return os.path.join(case_dir, out_csv)


# ------------ Main control loop ------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, help="OpenFOAM case dir (with constant/polyMesh etc.)")
    parser.add_argument("--solver", required=True, choices=["simpleFoam", "rhoPimpleFoam"], help="solver to run")
    parser.add_argument("--np", type=int, default=4, help="number of MPI processes to run the solver with")
    parser.add_argument("--pressure-csv", required=True, help="CSV with time_ms,pressure_Pa")
    parser.add_argument("--inlet-patch", default="inlet", help="name of the inlet patch in 0/U")
    parser.add_argument("--wall-patch", default="chamberWall", help="name of the chamber wall patch")
    parser.add_argument("--start-U", type=float, default=1.0, help="initial inlet velocity magnitude (m/s)")
    args = parser.parse_args()

    case_dir = args.case
    solver = args.solver
    np_proc = args.np
    pressure_csv = args.pressure_csv
    inlet_patch = args.inlet_patch
    wall_patch = args.wall_patch
    U_mag = args.start_U

    df = Inputs.read_target_pressure_series(pressure_csv)

    # Ensure function objects appended to controlDict so we get postProcessing outputs
    ensure_functionObjects_in_controlDict(case_dir, inlet_patch, chamber_region_name="internalCells")

    # Decompose for parallel run
    run_decompose_par(case_dir, np_proc)

    # Loop over each timepoint in CSV (time_ms -> target pressure)
    for idx, row in df.iterrows():
        t_ms = float(row["time_ms"])
        t_s = t_ms / 1000.0
        target_p = float(row["pressure_Pa"])
        print(f"\n=== Time {t_ms} ms ({t_s:.4f} s): target pressure = {target_p:.3f} Pa ===")

        # Controller iterations per timepoint
        for it in range(MAX_ITERS):
            print(f" Controller iteration {it + 1}/{MAX_ITERS}, current inlet U = {U_mag:.6g} m/s")

            # 1) Edit 0/U inlet fixedValue
            # set vector aligned along x-axis (modify as needed)
            edit_fixedValue_U(case_dir, inlet_patch, (U_mag, 0.0, 0.0))

            # 2) Run solver for a short horizon (we rely on controlDict endTime to control run length)
            # For robustness, we run the solver and let it produce functionObjects to postProcessing
            try:
                Solver.run_solver_parallel(case_dir, solver, np_proc)
            except Exception as e:
                print("Solver run failed:", e)
                raise

            # 3) ReconstructPar so that postProcessing output is consolidated (useful for single-file reads)
            try:
                reconstruct_par(case_dir)
            except Exception as e:
                print("Warning: reconstructPar failed:", e)

            # 4) Read average chamber pressure from postProcessing/fieldAverage_chamberPressure/<time>/
            measured_p = read_latest_postproc_field_average(case_dir, "fieldAverage_chamberPressure")
            if measured_p is None:
                print("Measured pressure not found in postProcessing — ensure functionObjects were active during run.")
                break
            print(f"  Measured average chamber pressure = {measured_p:.3f} Pa")

            # 5) Compute error and adjust inlet velocity using proportional control
            err = target_p - measured_p
            if abs(err) <= TOL_P:
                print(f"  Within tolerance (|{err:.1f}| Pa <= {TOL_P} Pa). Accepting inlet U = {U_mag:.6g}")
                break
            # adjust U
            deltaU = KP * err
            # clip step to avoid instability
            max_step = max(0.2 * abs(U_mag), 0.5)  # limit
            deltaU = max(-max_step, min(deltaU, max_step))
            U_mag = max(0.0, U_mag + deltaU)  # do not go negative
            print(f"  Pressure error {err:.1f} Pa -> adjusting U by {deltaU:.6g} -> new U = {U_mag:.6g}")

        # After controller settled (or iter exhausted), extract chamber wall pressure average
        outcsv = extract_wall_patch_pressures(case_dir
                                              , wall_patch_name=wall_patch
                                              , out_csv=f"wall_pressure_time_{int(t_ms)}ms.csv")
        print("Saved wall pressure (avg) at this time to:", outcsv)

    print("Completed all target timepoints. Final inlet U:", U_mag)


if __name__ == "__main__":
    main()
