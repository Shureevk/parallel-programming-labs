import subprocess
import csv
import os
import re

SIZES = [200, 400, 800, 1200, 1600, 2000]
STATS_FILE = 'stats_sk_mpi.csv'
PROCS = [1, 2, 4, 8]
EXE_PATH = 'src/matrix'

def run_command(cmd, description):
    print(f"{description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    Error: {result.stderr.strip()}")
        return False, ""
    return True, result.stdout

def main():
    print("Running MPI experiments...")
    print("=" * 50)

    if not os.path.exists(EXE_PATH):
        print(f"File {EXE_PATH} not found!")
        print("Compile: mpic++ src/main.cpp -o src/matrix -O2")
        return

    results = []

    for n in SIZES:
        for procs in PROCS:
            print(f"\nTest: N = {n}, Processes = {procs}")

            success, _ = run_command(f"python3 gen_matrices.py {n}", "Generate matrices")
            if not success:
                continue

            cmd = f"mpirun -np {procs} {EXE_PATH}"
            success, output = run_command(cmd, f"Run MPI ({procs} processes)")
            if not success:
                continue

            time_match = re.search(r"Computation time:\s*([\d.]+)\s*seconds", output)
            exec_time = float(time_match.group(1)) if time_match else 0.0

            operations = n ** 3

            success, verify_out = run_command("python3 check_result.py", "Verification")
            status = "PASSED" if success and "PASSED" in verify_out else "FAILED"

            results.append({
                'Size': n,
                'Processes': procs,
                'Time_sec': exec_time,
                'Operations': operations,
                'Status': status,
            })
            print(f"Time: {exec_time:.6f} sec | Status: {status}")

    base_times = {}
    for r in results:
        if r['Processes'] == 1:
            base_times[r['Size']] = r['Time_sec']

    for r in results:
        n = r['Size']
        t_p = r['Time_sec']
        p = r['Processes']
        if t_p > 0 and n in base_times:
            t_1 = base_times[n]
            r['Speedup'] = round(t_1 / t_p, 2)
            r['Efficiency'] = round(r['Speedup'] / p * 100, 1)
        else:
            r['Speedup'] = 0.0
            r['Efficiency'] = 0.0

    with open(STATS_FILE, 'w', newline='') as f:
        fieldnames = ['Size', 'Processes', 'Time_sec', 'Speedup', 'Efficiency', 'Operations', 'Status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {STATS_FILE}")

if __name__ == "__main__":
    main()
