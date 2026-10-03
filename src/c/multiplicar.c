#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

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

int compare_doubles(const void *a, const void *b) {
    double arg1 = *(const double *)a;
    double arg2 = *(const double *)b;
    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

int main(int argc, char *argv[]) {
    // Lee la ruta pasada como argumento o usa la ruta por defecto
    const char *nombre_archivo = (argc > 1) ? argv[1] : "data/matrices_prueba_3.txt";

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

    // Reserva dinámica de memoria para las matrices
    double **A = (double **)malloc(n * sizeof(double *));
    double **B = (double **)malloc(n * sizeof(double *));
    double **C = (double **)malloc(n * sizeof(double *));
    for (int i = 0; i < n; i++) {
        A[i] = (double *)malloc(n * sizeof(double));
        B[i] = (double *)malloc(n * sizeof(double));
        C[i] = (double *)malloc(n * sizeof(double));
    }

    // Lectura de datos
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

    // 1. Warm-up (Ejecución de calentamiento)
    multiplicar_triple_bucle(n, A, B, C);

    // 2. Medición de 5 repeticiones
    int num_repeticiones = 5;
    double tiempos_ms[5];
    LARGE_INTEGER frequency, start, end;
    QueryPerformanceFrequency(&frequency);

    printf("--- Midiendo C (%dx%d) ---\n", n, n);
    for (int rep = 0; rep < num_repeticiones; rep++) {
        QueryPerformanceCounter(&start);
        multiplicar_triple_bucle(n, A, B, C);
        QueryPerformanceCounter(&end);

        double tiempo_ms = ((double)(end.QuadPart - start.QuadPart) * 1000.0) / frequency.QuadPart;
        tiempos_ms[rep] = tiempo_ms;
        printf("Repeticion %d: %.4f ms\n", rep + 1, tiempo_ms);
    }

    // 3. Cálculo de la mediana
    qsort(tiempos_ms, num_repeticiones, sizeof(double), compare_doubles);
    double mediana_ms = tiempos_ms[num_repeticiones / 2];

    printf("\n--- Resultados ---\n");
    printf("Mediana: %.4f ms\n", mediana_ms);

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