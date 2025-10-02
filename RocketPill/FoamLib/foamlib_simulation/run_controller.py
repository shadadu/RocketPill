#!/usr/bin/env python3
import subprocess
import pandas as pd
from pathlib import Path

def run_cmd(case_dir, cmd):
    subprocess.run(cmd, cwd=case_dir, shell=True, check=True)

def set_inlet_velocity(case_dir, new_velocity):
    u_file = Path(case_dir) / "0" / "U"
    lines = u_file.read_text().splitlines()
    new_lines = []
    for line in lines:
        if "value" in line and "uniform" in line and "(" in line:
            new_lines.append(f"        value           uniform ({new_velocity} 0 0);")
        else:
            new_lines.append(line)
    u_file.write_text("\n".join(new_lines))

def get_avg_pressure(case_dir):
    run_cmd(case_dir, 'postProcess -func "volFieldValue(p)" -latestTime')
    f = Path(case_dir) / "postProcessing" / "volFieldValue(p)" / "0" / "volFieldValue.dat"
    if f.exists():
        last_line = f.read_text().strip().splitlines()[-1]
        return float(last_line.split()[-1])
    return None

def main():
    case_dir = "cases/simpleFoam_case"
    solver = "simpleFoam"
    target_csv = "pressure_curve.csv"

    df = pd.read_csv(target_csv)
    times = df["time_ms"].values / 1000.0
    pressures = df["pressure_Pa"].values

    run_cmd(case_dir, "rm -rf 1 2 3 processor* postProcessing log.*")
    run_cmd(case_dir, "blockMesh")

    inlet_velocity = 10.0
    set_inlet_velocity(case_dir, inlet_velocity)

    for t, p_target in zip(times, pressures):
        print(f"\n=== Target time {t:.4f}s, target pressure {p_target:.1f} Pa ===")
        run_cmd(case_dir, f"{solver} -stopAt writeNow > log.{solver} 2>&1")
        p_avg = get_avg_pressure(case_dir)
        if p_avg is None:
            print("Warning: could not get avg pressure")
            continue
        print(f"Measured avg pressure: {p_avg:.1f} Pa")
        error = p_target - p_avg
        inlet_velocity += 0.001 * error
        inlet_velocity = max(0.1, inlet_velocity)
        print(f"Adjusted inlet velocity to {inlet_velocity:.3f}")
        set_inlet_velocity(case_dir, inlet_velocity)

if __name__ == "__main__":
    main()
