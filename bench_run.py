import subprocess
import csv
import os
import re

SIZES = [10, 50, 100, 200, 400, 600, 800, 1000]
STATS_FILE = 'stats.csv'
EXE_PATH = 'src/matrix'

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr

def main():
    if not os.path.exists(EXE_PATH):
        print(f"Error: {EXE_PATH} not found!")
        print("Run: g++ src/main.cpp -o src/matrix -O2")
        return
    
    results = []
    
    for n in SIZES:
        print(f"\n--- Size: {n}x{n} ---")
        
        success, _ = run_command(f"python3 gen_matrices.py {n}")
        if not success:
            continue
        
        success, output = run_command(EXE_PATH)
        if not success:
            continue
        
        time_match = re.search(r"Computation time:\s*([\d.]+)\s*seconds", output)
        exec_time = float(time_match.group(1)) if time_match else 0.0
        
        operations = n ** 3
        
        success, verify_out = run_command("python3 check_result.py")
        status = "PASSED" if success and "PASSED" in verify_out else "FAILED"
        
        results.append({'Size': n, 'Time_sec': exec_time, 'Operations': operations, 'Status': status})
        print(f"Time: {exec_time:.6f} sec | Status: {status}")
    
    if results:
        with open(STATS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Size', 'Time_sec', 'Operations', 'Status'])
            writer.writeheader()
            writer.writerows(results)
        print(f"\nResults saved to {STATS_FILE}")

if __name__ == "__main__":
    main()
