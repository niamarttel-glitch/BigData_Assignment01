#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

// Función auxiliar para ordenar los tiempos y obtener la mediana
int comparar_doubles(const void *a, const void *b) {
    double arg1 = *(const double *)a;
    double arg2 = *(const double *)b;
    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

// Algoritmo de multiplicación
void multiplicar_triple_bucle(int n, const double *A, const double *B, double *C) {
    // Reiniciar C a cero antes de cada multiplicación
    for (int i = 0; i < n * n; i++) C[i] = 0.0;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                C[i * n + j] += A[i * n + k] * B[k * n + j];
            }
        }
    }
}

int main() {
    FILE *f = fopen("matrices_prueba_3.txt", "r");
    if (f == NULL) {
        printf("Error: no se pudo abrir el archivo de entrada.\n");
        return 1;
    }

    int n;
    if (fscanf(f, "%d", &n) != 1) {
        printf("Error al leer la dimensión n.\n");
        fclose(f);
        return 1;
    }

    // Reservar memoria fuera del cronómetro
    double *A = (double *)malloc(n * n * sizeof(double));
    double *B = (double *)malloc(n * n * sizeof(double));
    double *C = (double *)malloc(n * n * sizeof(double));

    for (int i = 0; i < n * n; i++) fscanf(f, "%lf", &A[i]);
    for (int i = 0; i < n * n; i++) fscanf(f, "%lf", &B[i]);
    fclose(f);

    // Configurar temporizador de alta frecuencia de Windows
    LARGE_INTEGER frecuencia, inicio, fin;
    QueryPerformanceFrequency(&frecuencia);

    // 1. Warm-up (Ejecución de calentamiento fuera de la medición)
    multiplicar_triple_bucle(n, A, B, C);

    // 2. Medición de 5 repeticiones
    int num_repeticiones = 5;
    double tiempos_ms[5];

    printf("--- Midiendo C (%dx%d) ---\n", n, n);
    for (int rep = 0; rep < num_repeticiones; rep++) {
        QueryPerformanceCounter(&inicio);
        multiplicar_triple_bucle(n, A, B, C);
        QueryPerformanceCounter(&fin);

        double tiempo_ms = (double)(fin.QuadPart - inicio.QuadPart) * 1000.0 / (double)frecuencia.QuadPart;
        tiempos_ms[rep] = tiempo_ms;
        printf("Repetición %d: %.4f ms\n", rep + 1, tiempo_ms);
    }

    // 3. Obtener mediana
    double tiempos_ordenados[5];
    for (int i = 0; i < num_repeticiones; i++) tiempos_ordenados[i] = tiempos_ms[i];
    qsort(tiempos_ordenados, num_repeticiones, sizeof(double), comparar_doubles);
    double mediana_ms = tiempos_ordenados[num_repeticiones / 2];

    printf("\n--- Resultados ---\n");
    printf("Mediana: %.4f ms\n", mediana_ms);

    free(A);
    free(B);
    free(C);

    return 0;
}