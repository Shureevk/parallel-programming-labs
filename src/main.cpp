#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <mpi.h>

using namespace std;
using namespace chrono;

vector<vector<double>> readMatrix(const string& filename, int& size) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: cannot open file " << filename << endl;
        exit(1);
    }
    file >> size;
    vector<vector<double>> mat(size, vector<double>(size));
    for (int i = 0; i < size; ++i)
        for (int j = 0; j < size; ++j)
            file >> mat[i][j];
    file.close();
    return mat;
}

void writeMatrix(const string& filename, const vector<vector<double>>& mat, int size) {
    ofstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: cannot write file " << filename << endl;
        exit(1);
    }
    file << size << "\n";
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            file << fixed << setprecision(15) << mat[i][j];
            if (j < size - 1) file << " ";
        }
        file << "\n";
    }
    file.close();
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    int n;
    vector<vector<double>> A, B;
    
    if (rank == 0) {
        int n1, n2;
        A = readMatrix("data/matrixA.txt", n1);
        B = readMatrix("data/matrixB.txt", n2);
        if (n1 != n2) {
            cerr << "Error: matrices must be same size" << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        n = n1;
        cout << "Matrix size: " << n << "x" << n << endl;
        cout << "Processes: " << size << endl;
    }
    
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    
    vector<double> A_flat(n * n), B_flat(n * n), C_flat(n * n, 0.0);
    
    if (rank == 0) {
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                A_flat[i * n + j] = A[i][j];
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                B_flat[i * n + j] = B[i][j];
    }
    
    MPI_Bcast(A_flat.data(), n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(B_flat.data(), n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    
    int rows_per_proc = n / size;
    int remainder = n % size;
    
    int start_row = rank * rows_per_proc;
    if (rank < remainder) {
        start_row += rank;
        rows_per_proc++;
    } else {
        start_row += remainder;
    }
    int end_row = start_row + rows_per_proc;
    
    MPI_Barrier(MPI_COMM_WORLD);
    auto start_time = high_resolution_clock::now();
    
    for (int i = start_row; i < end_row; ++i) {
        for (int j = 0; j < n; ++j) {
            double sum = 0.0;
            for (int k = 0; k < n; ++k) {
                sum += A_flat[i * n + k] * B_flat[k * n + j];
            }
            C_flat[i * n + j] = sum;
        }
    }
    
    vector<double> result_flat;
    if (rank == 0) {
        result_flat.resize(n * n);
    }
    
    vector<int> recv_counts(size), displs(size);
    for (int p = 0; p < size; ++p) {
        int p_rows = n / size;
        if (p < remainder) p_rows++;
        recv_counts[p] = p_rows * n;
        displs[p] = (p < remainder) ? p * (n / size + 1) * n : (remainder * (n / size + 1) + (p - remainder) * (n / size)) * n;
    }
    
    MPI_Gatherv(C_flat.data(), rows_per_proc * n, MPI_DOUBLE,
                result_flat.data(), recv_counts.data(), displs.data(), MPI_DOUBLE,
                0, MPI_COMM_WORLD);
    
    auto end_time = high_resolution_clock::now();
    duration<double> elapsed = end_time - start_time;
    
    if (rank == 0) {
        vector<vector<double>> C(n, vector<double>(n));
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                C[i][j] = result_flat[i * n + j];
        
        writeMatrix("data/matrixC.txt", C, n);
        
        cout << "Computation time: " << elapsed.count() << " seconds" << endl;
        cout << "Operations: " << (long long)n * n * n << endl;
    }
    
    MPI_Finalize();
    return 0;
}
