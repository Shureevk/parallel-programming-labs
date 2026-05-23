import matplotlib.pyplot as plt
import csv
import os

os.makedirs('plots', exist_ok=True)

sizes = []
times_1, times_2, times_4, times_8 = [], [], [], []
speedup_2, speedup_4, speedup_8 = [], [], []
efficiency_2, efficiency_4, efficiency_8 = [], [], []

with open('stats_sk_mpi.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        size = int(row['Size'])
        p = int(row['Processes'])
        if size not in sizes:
            sizes.append(size)
        if p == 1:
            times_1.append(float(row['Time_sec']))
        elif p == 2:
            times_2.append(float(row['Time_sec']))
            speedup_2.append(float(row['Speedup']))
            efficiency_2.append(float(row['Efficiency']))
        elif p == 4:
            times_4.append(float(row['Time_sec']))
            speedup_4.append(float(row['Speedup']))
            efficiency_4.append(float(row['Efficiency']))
        elif p == 8:
            times_8.append(float(row['Time_sec']))
            speedup_8.append(float(row['Speedup']))
            efficiency_8.append(float(row['Efficiency']))

plt.figure(figsize=(10, 6))
plt.plot(sizes, times_1, 'o-', label='1 process')
plt.plot(sizes, times_2, 's-', label='2 processes')
plt.plot(sizes, times_4, '^-', label='4 processes')
plt.plot(sizes, times_8, 'd-', label='8 processes')
plt.xlabel('Matrix size (N)')
plt.ylabel('Time (seconds)')
plt.title('Supercomputer: Execution time vs matrix size')
plt.legend()
plt.grid(True)
plt.savefig('plots/mpi_plot_time.png')

plt.figure(figsize=(10, 6))
plt.plot(sizes, speedup_2, 's-', label='2 processes')
plt.plot(sizes, speedup_4, '^-', label='4 processes')
plt.plot(sizes, speedup_8, 'd-', label='8 processes')
plt.plot(sizes, sizes, 'k--', label='Ideal speedup')
plt.xlabel('Matrix size (N)')
plt.ylabel('Speedup')
plt.title('Supercomputer: Speedup vs matrix size')
plt.legend()
plt.grid(True)
plt.savefig('plots/mpi_plot_speedup.png')

plt.figure(figsize=(10, 6))
plt.plot(sizes, efficiency_2, 's-', label='2 processes')
plt.plot(sizes, efficiency_4, '^-', label='4 processes')
plt.plot(sizes, efficiency_8, 'd-', label='8 processes')
plt.axhline(y=100, color='r', linestyle='--', label='100% efficiency')
plt.xlabel('Matrix size (N)')
plt.ylabel('Efficiency (%)')
plt.title('Supercomputer: Efficiency vs matrix size')
plt.legend()
plt.grid(True)
plt.savefig('plots/mpi_plot_efficiency.png')
print('Graphs saved to plots/')
