import matplotlib.pyplot as plt
import csv

sizes = []
times_1 = []
times_2 = []
times_4 = []
times_8 = []
speedup_2 = []
speedup_4 = []
speedup_8 = []
efficiency_2 = []
efficiency_4 = []
efficiency_8 = []

with open('stats_omp.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        size = int(row['Size'])
        t = int(row['Threads'])
        time_val = float(row['Time_sec'])
        speedup = float(row['Speedup'])
        efficiency = float(row['Efficiency'])
        
        if size not in sizes:
            sizes.append(size)
        
        if t == 1:
            times_1.append(time_val)
        elif t == 2:
            times_2.append(time_val)
            speedup_2.append(speedup)
            efficiency_2.append(efficiency)
        elif t == 4:
            times_4.append(time_val)
            speedup_4.append(speedup)
            efficiency_4.append(efficiency)
        elif t == 8:
            times_8.append(time_val)
            speedup_8.append(speedup)
            efficiency_8.append(efficiency)

plt.figure(figsize=(10, 6))
plt.plot(sizes, times_1, 'o-', label='1 thread')
plt.plot(sizes, times_2, 's-', label='2 threads')
plt.plot(sizes, times_4, '^-', label='4 threads')
plt.plot(sizes, times_8, 'd-', label='8 threads')
plt.xlabel('Matrix size (N)')
plt.ylabel('Time (seconds)')
plt.title('Execution time vs matrix size')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('plot_time_vs_threads.png')
print('plot_time_vs_threads.png saved')

plt.figure(figsize=(10, 6))
plt.plot(sizes, speedup_2, 's-', label='2 threads')
plt.plot(sizes, speedup_4, '^-', label='4 threads')
plt.plot(sizes, speedup_8, 'd-', label='8 threads')
plt.plot(sizes, sizes, 'k--', label='Ideal speedup', linewidth=1)
plt.xlabel('Matrix size (N)')
plt.ylabel('Speedup')
plt.title('Speedup vs matrix size')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('plot_speedup.png')
print('plot_speedup.png saved')

plt.figure(figsize=(10, 6))
plt.plot(sizes, efficiency_2, 's-', label='2 threads')
plt.plot(sizes, efficiency_4, '^-', label='4 threads')
plt.plot(sizes, efficiency_8, 'd-', label='8 threads')
plt.axhline(y=100, color='r', linestyle='--', label='100% efficiency')
plt.xlabel('Matrix size (N)')
plt.ylabel('Efficiency (%)')
plt.title('Efficiency vs matrix size')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('plot_efficiency.png')
print('plot_efficiency.png saved')
