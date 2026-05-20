#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>
#include <iomanip>

using namespace std;
using namespace chrono;

vector<vector<double>> multiplyMatrices(const vector<vector<double>>& A,
                                        const vector<vector<double>>& B,
                                        int n) {
    vector<vector<double>> C(n, vector<double>(n, 0.0));
    
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            double aik = A[i][k];
            for (int j = 0; j < n; ++j) {
                C[i][j] += aik * B[k][j];
            }
        }
    }
    return C;
}

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

int main() {
    int n1, n2;
    
    vector<vector<double>> A = readMatrix("data/matrixA.txt", n1);
    vector<vector<double>> B = readMatrix("data/matrixB.txt", n2);
    
    if (n1 != n2) {
        cerr << "Error: matrices must be same size" << endl;
        return 1;
    }
    
    int n = n1;
    cout << "Matrix size: " << n << "x" << n << endl;
    
    auto start = high_resolution_clock::now();
    vector<vector<double>> C = multiplyMatrices(A, B, n);
    auto end = high_resolution_clock::now();
    
    duration<double> elapsed = end - start;
    
    writeMatrix("data/matrixC.txt", C, n);
    
    cout << "Computation time: " << elapsed.count() << " seconds" << endl;
    cout << "Operations: " << (long long)n * n * n << endl;
    
    return 0;
}
