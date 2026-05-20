import matplotlib.pyplot as plt
import csv

sizes = []
times = []

with open('stats.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        sizes.append(int(row['Size']))
        times.append(float(row['Time_sec']))

plt.figure(figsize=(10, 6))
plt.plot(sizes, times, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Matrix size (N)')
plt.ylabel('Time (seconds)')
plt.title('Matrix multiplication time')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('graph_time.png')
print("graph_time.png saved")

plt.figure(figsize=(10, 6))
plt.plot(sizes, [n**3 for n in sizes], 'ro-', linewidth=2, markersize=8)
plt.xlabel('Matrix size (N)')
plt.ylabel('Operations')
plt.title('Operations vs matrix size')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('graph_ops.png')
print("graph_ops.png saved")
