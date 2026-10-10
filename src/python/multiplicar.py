import time
import statistics
import sys
import tracemalloc

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

def test_correctitud():
    # Prueba rápida con matrices 2x2 conocidas
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[2.0, 0.0], [1.0, 2.0]]
    esperado = [[4.0, 4.0], [10.0, 8.0]]
    resultado = multiplicar_triple_bucle(2, A, B)
    assert resultado == esperado, "Error en la validación de correctitud"
    print("Correctitud validada exitosamente con matriz de prueba 2x2.")

if __name__ == "__main__":
    nombre_archivo = sys.argv[1] if len(sys.argv) > 1 else "data/matrices_3.txt"
    n, A, B = leer_matrices(nombre_archivo)

    test_correctitud()

    # 1. Warm-up
    _ = multiplicar_triple_bucle(n, A, B)

    # 2. Medición de 5 repeticiones (Tiempo y Memoria)
    num_repeticiones = 5
    tiempos_ms = []
    
    # Iniciar el rastreo de memoria
    tracemalloc.start()

    print(f"--- Midiendo Python ({n}x{n}) ---")
    for rep in range(num_repeticiones):
        inicio = time.perf_counter()
        C = multiplicar_triple_bucle(n, A, B)
        fin = time.perf_counter()
        
        tiempo_ms = (fin - inicio) * 1000.0
        tiempos_ms.append(tiempo_ms)
        print(f"Repetición {rep + 1}: {tiempo_ms:.4f} ms")

    # Capturar el pico de memoria usado
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoria_mb = peak / (1024 * 1024)

    # 3. Resultados estadísticos
    mediana_ms = statistics.median(tiempos_ms)
    variabilidad_ms = statistics.stdev(tiempos_ms) if len(tiempos_ms) > 1 else 0.0

    print("\n--- Resultados ---")
    print(f"Mediana: {mediana_ms:.4f} ms")
    print(f"Variabilidad (StdDev): {variabilidad_ms:.4f} ms")
    print(f"Pico de Memoria: {memoria_mb:.4f} MB")