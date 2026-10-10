#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <math.h>
#include <psapi.h> // Necesario para medir la memoria en Windows

void multiplicar_triple_bucle(int n, double **A, double **B, double **C) {
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

void test_correctitud() {
    double *A_test[2], *B_test[2], *C_test[2];
    double A_data[2][2] = {{1.0, 2.0}, {3.0, 4.0}};
    double B_data[2][2] = {{2.0, 0.0}, {1.0, 2.0}};
    double C_expected[2][2] = {{4.0, 4.0}, {10.0, 8.0}};

    for (int i = 0; i < 2; i++) {
        A_test[i] = A_data[i];
        B_test[i] = B_data[i];
        C_test[i] = (double *)malloc(2 * sizeof(double));
    }

    multiplicar_triple_bucle(2, A_test, B_test, C_test);

    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            if (fabs(C_test[i][j] - C_expected[i][j]) > 1e-6) {
                printf("Error en la validacion de correctitud.\n");
                exit(1);
            }
        }
    }
    printf("Correctitud validada exitosamente con matriz de prueba 2x2.\n");
    
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
    const char *nombre_archivo = (argc > 1) ? argv[1] : "data/matrices_3.txt";

    FILE *f = fopen(nombre_archivo, "r");
    if (f == NULL) {
        printf("Error: no se pudo abrir el archivo %s\n", nombre_archivo);
        return 1;
    }

    int n;
    if (fscanf(f, "%d", &n) != 1) {
        printf("Error al leer la dimension.\n");
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

    // Validación
    test_correctitud();

    // 1. Warm-up
    multiplicar_triple_bucle(n, A, B, C);

    // 2. Medición de 5 repeticiones
    int num_repeticiones = 5;
    double tiempos_ms[5];
    LARGE_INTEGER frequency, start, end;
    QueryPerformanceFrequency(&frequency);

    printf("--- Midiendo C (%dx%d) ---\n", n, n);
    double suma_tiempos = 0.0;
    
    for (int rep = 0; rep < num_repeticiones; rep++) {
        QueryPerformanceCounter(&start);
        multiplicar_triple_bucle(n, A, B, C);
        QueryPerformanceCounter(&end);

        double tiempo_ms = ((double)(end.QuadPart - start.QuadPart) * 1000.0) / frequency.QuadPart;
        tiempos_ms[rep] = tiempo_ms;
        suma_tiempos += tiempo_ms;
        printf("Repeticion %d: %.4f ms\n", rep + 1, tiempo_ms);
    }

    // 3. Medición de Memoria (Pico de memoria del proceso en Windows)
    PROCESS_MEMORY_COUNTERS pmc;
    double memoria_mb = 0.0;
    if (GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
        memoria_mb = (double)pmc.PeakWorkingSetSize / (1024.0 * 1024.0);
    }

    // 4. Cálculos estadísticos (Mediana y Desviación Estándar)
    double media = suma_tiempos / num_repeticiones;
    double suma_varianzas = 0.0;
    for(int i = 0; i < num_repeticiones; i++) {
        suma_varianzas += pow(tiempos_ms[i] - media, 2);
    }
    double variabilidad_ms = sqrt(suma_varianzas / num_repeticiones);

    qsort(tiempos_ms, num_repeticiones, sizeof(double), compare_doubles);
    double mediana_ms = tiempos_ms[num_repeticiones / 2];

    printf("\n--- Resultados ---\n");
    printf("Mediana: %.4f ms\n", mediana_ms);
    printf("Variabilidad (StdDev): %.4f ms\n", variabilidad_ms);
    printf("Pico de Memoria: %.4f MB\n", memoria_mb);

    // Liberar memoria
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