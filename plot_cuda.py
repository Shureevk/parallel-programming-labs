import matplotlib.pyplot as plt
import csv
import os

os.makedirs('plots', exist_ok=True)

sizes = []
times_8, times_16, times_32 = [], [], []
efficiency_16, efficiency_32 = [], []

with open('stats_cuda.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        size = int(row['Size'])
        b = int(row['BlockSize'])
        if size not in sizes:
            sizes.append(size)
        if b == 8:
            times_8.append(float(row['Time_sec']))
        elif b == 16:
            times_16.append(float(row['Time_sec']))
            efficiency_16.append(float(row['Efficiency']))
        elif b == 32:
            times_32.append(float(row['Time_sec']))
            efficiency_32.append(float(row['Efficiency']))

plt.figure(figsize=(10, 6))
plt.plot(sizes, times_8, 'o-', label='Block 8x8')
plt.plot(sizes, times_16, 's-', label='Block 16x16')
plt.plot(sizes, times_32, '^-', label='Block 32x32')
plt.xlabel('Matrix size (N)')
plt.ylabel('Time (seconds)')
plt.title('CUDA: Execution time vs matrix size')
plt.legend()
plt.grid(True)
plt.savefig('plots/plot_time_cuda.png')

plt.figure(figsize=(10, 6))
plt.plot(sizes, efficiency_16, 's-', label='Block 16x16')
plt.plot(sizes, efficiency_32, '^-', label='Block 32x32')
plt.xlabel('Matrix size (N)')
plt.ylabel('Efficiency (%)')
plt.title('CUDA: Efficiency vs matrix size')
plt.legend()
plt.grid(True)
plt.savefig('plots/plot_efficiency_cuda.png')
print('Graphs saved to plots/')
