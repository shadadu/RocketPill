#!/usr/bin/env python3
"""run_controller.py (v2)
Updated to call postprocessing and helper scripts to compute averaged pressure and set inlet from mass flux.
"""
import argparse, csv, os, subprocess, time, math

def run(cmd, cwd=None):
    print('RUN:', ' '.join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)

def read_pressure_curve(csv_path):
    times = []
    pressures = []
    with open(csv_path) as f:
        r = csv.reader(f)
        for row in r:
            if not row: continue
            try:
                t = float(row[0])
                p = float(row[1])
            except:
                continue
            times.append(t/1000.0)
            pressures.append(p)
    return times, pressures

def write_inlet_velocity_case_incompressible(case_dir, patch='inlet', U=[1,0,0]):
    path = os.path.join(case_dir, '0', 'U')
    if not os.path.exists(path):
        print('0/U not found:', path); return
    with open(path, 'r') as f:
        txt = f.read()
    marker = f'/* PATCH {patch} START */'
    if marker in txt:
        start = txt.index(marker)
        end = txt.index(f'/* PATCH {patch} END */', start)
        before = txt[:start]
        after = txt[end + len(f'/* PATCH {patch} END */'):]
        patchBlock = f"""{marker}
{patch}
{{
    type            fixedValue;
    value           uniform ({U[0]:g} {U[1]:g} {U[2]:g});
}}
/* PATCH {patch} END */"""
        txt = before + patchBlock + after
        with open(path, 'w') as f:
            f.write(txt)
    else:
        print('Warning: marker for patch not found in 0/U. Please edit 0/U manually.')

def write_inlet_massflux_compressible(case_dir, massFlux, patch_area=1.0):
    os.makedirs(os.path.join(case_dir, 'constant'), exist_ok=True)
    with open(os.path.join(case_dir, 'constant', 'inletMassFlux'), 'w') as f:
        f.write(f"# inlet mass flux (kg/s)\n{massFlux}\n# patch_area (m2)\n{patch_area}\n")

def read_latest_avg_p(case_dir):
    pfile = os.path.join(case_dir, 'latest_avg_p.txt')
    if not os.path.exists(pfile):
        return None
    with open(pfile) as f:
        txt = f.read().strip()
    try:
        return float(txt)
    except:
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', required=True, help='case directory (relative or absolute)')
    parser.add_argument('--solver', required=True, choices=['simpleFoam', 'rhoPimpleFoam'])
    parser.add_argument('--np', type=int, default=1)
    parser.add_argument('--pressure-csv', required=True, help='CSV with time_ms,pressure_Pa')
    parser.add_argument('--inlet-area', type=float, default=0.001, help='inlet area (m2) for computing velocity from massflux')
    parser.add_argument('--burst-steps', type=int, default=20, help='number of internal timesteps or solver iterations per control update')
    args = parser.parse_args()

    times, pressures = read_pressure_curve(args.pressure_csv)
    if not times:
        raise SystemExit('No data in pressure CSV')

    run(['blockMesh', '-case', args.case])
    if args.np > 1:
        run(['decomposePar', '-case', args.case])

    for idx, t in enumerate(times):
        target_p = pressures[idx]
        print(f"Target at t={t:.4f}s -> p={target_p:.1f} Pa")
        C = 1e-5
        massFlux = C * target_p
        rho = 1.0
        U_mag = massFlux / (rho * args.inlet_area) if args.inlet_area>0 else 0.0

        if args.solver == 'simpleFoam':
            write_inlet_velocity_case_incompressible(args.case, patch='inlet', U=[U_mag,0,0])
        else:
            write_inlet_massflux_compressible(args.case, massFlux, patch_area=args.inlet_area)
            # convert to inlet U via helper script
            try:
                run(['bash','-c', f'./setInletFromMassFlux.sh {args.case} 1.0'], cwd=args.case)
            except subprocess.CalledProcessError:
                print('setInletFromMassFlux.sh failed; inlet file may need manual editing')

        if args.np > 1:
            cmd = ['mpirun', '-np', str(args.np), args.solver, '-case', args.case]
        else:
            cmd = [args.solver, '-case', args.case]
        print('Starting solver burst...')
        try:
            run(cmd)
        except subprocess.CalledProcessError:
            print('Solver run failed (likely no OpenFOAM here). Continuing.')

        # Run postprocessing helper which extracts averaged p produced by function object
        try:
            run(['bash','-c', f'./postprocess_avg_p.sh {args.case}'], cwd=args.case)
        except subprocess.CalledProcessError:
            print('postprocess_avg_p.sh did not find averaged pressure yet.')

        p_meas = read_latest_avg_p(args.case)
        print(f'Measured avg p: {p_meas}')

        if p_meas is not None:
            error = target_p - p_meas
            massFlux = massFlux + 1e-6 * error
            print(f'Adjusted massFlux -> {massFlux}')

        time.sleep(0.1)

    if args.np > 1:
        run(['reconstructPar', '-case', args.case])

    print('Controller finished.')

if __name__ == '__main__':
    main()
