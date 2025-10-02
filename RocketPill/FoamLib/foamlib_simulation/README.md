# foamlib_project_v5

This project contains OpenFOAM case templates and a Python run controller for adjusting inlet velocity to track a target chamber pressure curve.

## Contents
- `cases/simpleFoam_case`: Simple incompressible case (simpleFoam)
- `cases/rhoPimpleFoam_case`: Compressible case (rhoPimpleFoam)
- `run_controller.py`: Python script to run solver, read pressures, and adjust inlet velocity
- `pressure_curve.csv`: Example chamber pressure profile

## Usage (macOS/Homebrew)
1. Install OpenFOAM via Homebrew: `brew install openfoam`.
2. Ensure `/opt/homebrew/bin` is in your PATH (check with `which simpleFoam`).
3. Run controller:
   ```bash
   python3 run_controller.py
   ```
