#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <cuda_runtime.h>

using namespace std;
using namespace chrono;

__global__ void matrixMulKernel(const double *A, const double *B, double *C, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    if (row < n && col < n) {
        double sum = 0.0;
        for (int k = 0; k < n; k++) {
            sum += A[row * n + k] * B[k * n + col];
        }
        C[row * n + col] = sum;
    }
}

bool readMatrixFlat(const string& filename, vector<double>& matrix, int& n) {
    ifstream file(filename);
    if (!file.is_open()) return false;
    file >> n;
    matrix.resize(n * n);
    for (int i = 0; i < n * n; ++i) {
        file >> matrix[i];
    }
    return true;
}

void writeMatrixFlat(const string& filename, const vector<double>& matrix, int n) {
    ofstream file(filename);
    if (!file.is_open()) return;
    file << n << endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            file << matrix[i * n + j] << " ";
        }
        file << endl;
    }
}

int main(int argc, char** argv) {
    int blockSize = 16;
    if (argc > 1) {
        blockSize = atoi(argv[1]);
    }

    int n;
    vector<double> A_host, B_host, C_host;

    if (!readMatrixFlat("data/matrixA.txt", A_host, n)) {
        cerr << "Error reading matrixA.txt" << endl;
        return 1;
    }

    ifstream fb("data/matrixB.txt");
    if (!fb.is_open()) {
        cerr << "Error reading matrixB.txt" << endl;
        return 1;
    }
    int n_tmp;
    fb >> n_tmp;
    B_host.resize(n * n);
    for (int i = 0; i < n * n; ++i) fb >> B_host[i];
    fb.close();

    cout << "Matrix size: " << n << "x" << n << endl;
    cout << "Block size: " << blockSize << "x" << blockSize << endl;

    double *A_device, *B_device, *C_device;
    size_t memSize = n * n * sizeof(double);

    cudaMalloc(&A_device, memSize);
    cudaMalloc(&B_device, memSize);
    cudaMalloc(&C_device, memSize);

    auto start = high_resolution_clock::now();

    cudaMemcpy(A_device, A_host.data(), memSize, cudaMemcpyHostToDevice);
    cudaMemcpy(B_device, B_host.data(), memSize, cudaMemcpyHostToDevice);

    dim3 blockDim(blockSize, blockSize);
    dim3 gridDim((n + blockSize - 1) / blockSize, (n + blockSize - 1) / blockSize);

    matrixMulKernel<<<gridDim, blockDim>>>(A_device, B_device, C_device, n);
    cudaDeviceSynchronize();

    C_host.resize(n * n);
    cudaMemcpy(C_host.data(), C_device, memSize, cudaMemcpyDeviceToHost);

    auto end = high_resolution_clock::now();
    duration<double> elapsed = end - start;

    cudaFree(A_device);
    cudaFree(B_device);
    cudaFree(C_device);

    writeMatrixFlat("data/matrixC.txt", C_host, n);

    cout << "Computation time: " << elapsed.count() << " seconds" << endl;
    cout << "Operations: " << (long long)n * n * n << endl;

    return 0;
}
