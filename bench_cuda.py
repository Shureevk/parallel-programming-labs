import subprocess
import csv
import os
import re

SIZES = [200, 400, 800, 1200, 1600, 2000]
BLOCK_SIZES = [8, 16, 32]
STATS_FILE = 'stats_cuda.csv'
EXE_PATH = 'src/matrix_cuda'

def run_command(cmd, description):
    print(f"{description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    Error: {result.stderr.strip()}")
        return False, ""
    return True, result.stdout

def main():
    print("Running CUDA experiments...")
    print("=" * 50)

    if not os.path.exists(EXE_PATH):
        print(f"File {EXE_PATH} not found!")
        print("Compile: nvcc src/main.cu -o src/matrix_cuda")
        return

    results = []

    for n in SIZES:
        for block in BLOCK_SIZES:
            print(f"\nTest: N = {n}x{n}, Block = {block}x{block}")

            success, _ = run_command(f"python3 gen_matrices.py {n}", "Generate matrices")
            if not success:
                continue

            cmd = f"{EXE_PATH} {block}"
            success, output = run_command(cmd, f"Run CUDA (block {block})")
            if not success:
                continue

            time_match = re.search(r"Computation time:\s*([\d.]+)\s*seconds", output)
            exec_time = float(time_match.group(1)) if time_match else 0.0

            operations = n ** 3

            success, verify_out = run_command("python3 check_result.py", "Verification")
            status = "PASSED" if success and "PASSED" in verify_out else "FAILED"

            results.append({
                'Size': n,
                'BlockSize': block,
                'Time_sec': exec_time,
                'Operations': operations,
                'Status': status,
            })
            print(f"Time: {exec_time:.6f} sec | Status: {status}")

    if results:
        base_times = {}
        for r in results:
            if r['BlockSize'] == 8:
                base_times[r['Size']] = r['Time_sec']

        for r in results:
            n = r['Size']
            t_p = r['Time_sec']
            b = r['BlockSize']
            if n in base_times and t_p > 0:
                t_base = base_times[n]
                r['Speedup'] = round(t_base / t_p, 2)
                ideal_ratio = (b * b) / 64.0
                if ideal_ratio > 0:
                    r['Efficiency'] = round((r['Speedup'] / ideal_ratio) * 100, 1)
                else:
                    r['Efficiency'] = 0.0
            else:
                r['Speedup'] = 1.0
                r['Efficiency'] = 100.0

        with open(STATS_FILE, 'w', newline='') as f:
            fieldnames = ['Size', 'BlockSize', 'Time_sec', 'Speedup', 'Efficiency', 'Operations', 'Status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\nResults saved to {STATS_FILE}")

if __name__ == "__main__":
    main()
