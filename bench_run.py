import os.path
import re
import subprocess
import csv

SIZES = [200, 400, 800, 1200, 1600, 2000]
STATS_FILE = 'stats_omp.csv'
THREADS = [1, 2, 4, 8]
EXE_PATH = 'src/matrix'

def run_command(command, description, env_param=None):
    print(f"{description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env_param)
    if result.returncode != 0:
        print(f"    Error: {result.stderr.strip()}")
        return False, ""
    return True, result.stdout

def main():
    print("Running OpenMP experiments...")
    print("=" * 50)

    if not os.path.exists(EXE_PATH):
        print(f"File {EXE_PATH} not found!")
        print("Compile: g++ -fopenmp -O2 -std=c++11 -o src/matrix src/main.cpp")
        return

    results = []

    for n in SIZES:
        for threads in THREADS:
            print(f"\nTest: N = {n}, Threads = {threads}")

            success, _ = run_command(f"python3 gen_matrices.py {n}", "Generate matrices")
            if not success:
                continue

            env = os.environ.copy()
            env['OMP_NUM_THREADS'] = str(threads)

            success, output = run_command(EXE_PATH, f"Run multiplication ({threads} threads)", env_param=env)
            if not success:
                continue

            time_match = re.search(r"Computation time:\s*([\d.]+)\s*seconds", output)
            exec_time = float(time_match.group(1)) if time_match else 0.0

            operations = n ** 3

            success_verify, output_verify = run_command("python3 check_result.py", "Verification")
            if success_verify and "PASSED" in output_verify:
                is_correct = "PASSED"
            else:
                is_correct = "FAILED"

            if is_correct == "PASSED":
                print("Verification PASSED")
            else:
                print("Verification FAILED")

            results.append({
                'Size': n,
                'Threads': threads,
                'Time_sec': exec_time,
                'Operations': operations,
                'Status': is_correct,
            })

    base_times = {}
    for r in results:
        if r['Threads'] == 1:
            base_times[r['Size']] = r['Time_sec']

    for r in results:
        n = r['Size']
        t_p = r['Time_sec']
        p = r['Threads']
        if t_p > 0 and n in base_times:
            t_1 = base_times[n]
            r['Speedup'] = round(t_1 / t_p, 2)
            r['Efficiency'] = round(r['Speedup'] / p * 100, 1)
        else:
            r['Speedup'] = 0.0
            r['Efficiency'] = 0.0

    if results:
        with open(STATS_FILE, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Size', 'Threads', 'Time_sec', 'Speedup', 'Efficiency', 'Operations', 'Status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print("\n" + "=" * 50)
        print(f"Results saved to: {STATS_FILE}")
        print("=" * 50)

if __name__ == "__main__":
    main()
