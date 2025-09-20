
import subprocess

def run_cmd(cmd, cwd=None, env=None, check=True):
    print("CMD:", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=cwd, env=env)
    if check and proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return proc.returncode

def run_solver_parallel(case_dir, solver, np_proc, run_runtime_seconds=None):
    """
    Run the solver in parallel. The solver will run until controlDict endTime or until it finishes.
    Optionally, you can pass a 'run_runtime_seconds' to allow killing after that real time (not ideal).
    We'll run: mpirun -np N solver -case case -parallel
    """
    cmd = ["mpirun", "-np", str(np_proc), solver, "-case", case_dir, "-parallel"]
    # Run and block until exit
    run_cmd(cmd, cwd=case_dir)