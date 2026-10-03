import time
import statistics
import sys

def leer_matrices(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        lineas = [linea.strip() for linea in f.readlines() if linea.strip()]
    
    n = int(lineas[0])
    
    matriz_a = []
    for i in range(1, n + 1):
        matriz_a.append([float(x) for x in lineas[i].split()])
        
    matriz_b = []
    for i in range(n + 1, 2 * n + 1):
        matriz_b.append([float(x) for x in lineas[i].split()])
        
    return n, matriz_a, matriz_b

def multiplicar_triple_bucle(n, A, B):
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

if __name__ == "__main__":
    # Lee la ruta enviada por la consola (benchmark.py)
    nombre_archivo = sys.argv[1] if len(sys.argv) > 1 else "data/matrices_prueba_3.txt"
    n, A, B = leer_matrices(nombre_archivo)

    # 1. Warm-up
    _ = multiplicar_triple_bucle(n, A, B)

    # 2. Medición de 5 repeticiones
    num_repeticiones = 5
    tiempos_ms = []

    print(f"--- Midiendo Python ({n}x{n}) ---")
    for rep in range(num_repeticiones):
        inicio = time.perf_counter()
        C = multiplicar_triple_bucle(n, A, B)
        fin = time.perf_counter()
        
        tiempo_ms = (fin - inicio) * 1000.0
        tiempos_ms.append(tiempo_ms)
        print(f"Repetición {rep + 1}: {tiempo_ms:.4f} ms")

    # 3. Mediana
    mediana_ms = statistics.median(tiempos_ms)
    print("\n--- Resultados ---")
    print(f"Tiempos raw: {[round(t, 4) for t in tiempos_ms]} ms")
    print(f"Mediana: {mediana_ms:.4f} ms")