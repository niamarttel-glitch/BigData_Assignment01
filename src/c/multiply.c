#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <math.h>
#include <psapi.h> // Required to measure memory in Windows

void triple_loop_multiply(int n, double **A, double **B, double **C) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i][j] = 0.0;
        }
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

void test_correctness() {
    double *A_test[2], *B_test[2], *C_test[2];
    double A_data[2][2] = {{1.0, 2.0}, {3.0, 4.0}};
    double B_data[2][2] = {{2.0, 0.0}, {1.0, 2.0}};
    double C_expected[2][2] = {{4.0, 4.0}, {10.0, 8.0}};

    for (int i = 0; i < 2; i++) {
        A_test[i] = A_data[i];
        B_test[i] = B_data[i];
        C_test[i] = (double *)malloc(2 * sizeof(double));
    }

    triple_loop_multiply(2, A_test, B_test, C_test);

    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            if (fabs(C_test[i][j] - C_expected[i][j]) > 1e-6) {
                printf("Error in correctness validation.\n");
                exit(1);
            }
        }
    }
    printf("Correctness successfully validated with 2x2 test matrix.\n");
    
    for (int i = 0; i < 2; i++) free(C_test[i]);
}

int compare_doubles(const void *a, const void *b) {
    double arg1 = *(const double *)a;
    double arg2 = *(const double *)b;
    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

int main(int argc, char *argv[]) {
    // Note: Default file changed to matrix_3.txt
    const char *filename = (argc > 1) ? argv[1] : "data/matrix_3.txt";

    FILE *f = fopen(filename, "r");
    if (f == NULL) {
        printf("Error: could not open file %s\n", filename);
        return 1;
    }

    int n;
    if (fscanf(f, "%d", &n) != 1) {
        printf("Error reading the dimension.\n");
        fclose(f);
        return 1;
    }

    double **A = (double **)malloc(n * sizeof(double *));
    double **B = (double **)malloc(n * sizeof(double *));
    double **C = (double **)malloc(n * sizeof(double *));
    for (int i = 0; i < n; i++) {
        A[i] = (double *)malloc(n * sizeof(double));
        B[i] = (double *)malloc(n * sizeof(double));
        C[i] = (double *)malloc(n * sizeof(double));
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            fscanf(f, "%lf", &A[i][j]);
        }
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            fscanf(f, "%lf", &B[i][j]);
        }
    }
    fclose(f);

    // Validation
    test_correctness();

    // 1. Warm-up
    triple_loop_multiply(n, A, B, C);

    // 2. Measurement of 5 repetitions
    int num_repetitions = 5;
    double times_ms[5];
    LARGE_INTEGER frequency, start, end;
    QueryPerformanceFrequency(&frequency);

    printf("--- Measuring C (%dx%d) ---\n", n, n);
    double sum_times = 0.0;
    
    for (int rep = 0; rep < num_repetitions; rep++) {
        QueryPerformanceCounter(&start);
        triple_loop_multiply(n, A, B, C);
        QueryPerformanceCounter(&end);

        double time_ms = ((double)(end.QuadPart - start.QuadPart) * 1000.0) / frequency.QuadPart;
        times_ms[rep] = time_ms;
        sum_times += time_ms;
        printf("Repetition %d: %.4f ms\n", rep + 1, time_ms);
    }

    // 3. Memory Measurement (Peak process memory in Windows)
    PROCESS_MEMORY_COUNTERS pmc;
    double memory_mb = 0.0;
    if (GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
        memory_mb = (double)pmc.PeakWorkingSetSize / (1024.0 * 1024.0);
    }

    // 4. Statistical calculations (Median and Standard Deviation)
    double mean = sum_times / num_repetitions;
    double sum_variances = 0.0;
    for(int i = 0; i < num_repetitions; i++) {
        sum_variances += pow(times_ms[i] - mean, 2);
    }
    double variability_ms = sqrt(sum_variances / num_repetitions);

    qsort(times_ms, num_repetitions, sizeof(double), compare_doubles);
    double median_ms = times_ms[num_repetitions / 2];

    printf("\n--- Results ---\n");
    printf("Median: %.4f ms\n", median_ms);
    printf("Variability (StdDev): %.4f ms\n", variability_ms);
    printf("Peak Memory: %.4f MB\n", memory_mb);

    // Free memory
    for (int i = 0; i < n; i++) {
        free(A[i]);
        free(B[i]);
        free(C[i]);
    }
    free(A);
    free(B);
    free(C);

    return 0;
}