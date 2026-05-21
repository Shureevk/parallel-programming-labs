import numpy as np
import sys

def load_matrix(filename):
    with open(filename, 'r') as file:
        n = int(file.readline())
        matrix = []
        for line in file:
            if line.strip():
                row = [float(x) for x in line.split()]
                matrix.append(row)
    return matrix

def main():
    try:
        A = load_matrix('data/matrixA.txt')
        B = load_matrix('data/matrixB.txt')
        C_cpp = load_matrix('data/matrixC.txt')

        A_np = np.array(A)
        B_np = np.array(B)
        C_np = np.array(C_cpp)
        C_correct = np.dot(A_np, B_np)

        if np.allclose(C_np, C_correct):
            print("PASSED")
            return 0
        else:
            print("FAILED")
            return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
