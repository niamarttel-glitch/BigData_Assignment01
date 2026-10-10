import matplotlib.pyplot as plt
import re
import os

dimensiones = []
python_ms = []
c_ms = []
java_ms = []

# Leer automáticamente los datos generados por benchmark.py
ruta_resultados = 'resultados.md'

try:
    with open(ruta_resultados, 'r', encoding='utf-8') as f:
        for linea in f:
            # Buscar las filas de la tabla: | NxN | py_time ± py_std | py_mem | c_time ± c_std | ...
            match = re.search(r'\|\s*(\d+)x\d+\s*\|\s*([\d\.]+)\s*±.*?\|\s*([\d\.]+)\s*±.*?\|\s*([\d\.]+)\s*±', linea)
            if match:
                dimensiones.append(int(match.group(1)))
                python_ms.append(float(match.group(2)))
                c_ms.append(float(match.group(3)))
                java_ms.append(float(match.group(4)))
                
except FileNotFoundError:
    print(f"Error: No se encontró '{ruta_resultados}'. Ejecuta benchmark.py primero.")
    exit(1)

if not dimensiones:
    print("Error: No se pudieron extraer los datos de la tabla. Revisa el formato de resultados.md.")
    exit(1)

# Generación del gráfico
plt.figure(figsize=(10, 6))
plt.plot(dimensiones, python_ms, marker='o', label='Python', color='red', linewidth=2)
plt.plot(dimensiones, c_ms, marker='s', label='C', color='blue', linewidth=2)
plt.plot(dimensiones, java_ms, marker='^', label='Java', color='green', linewidth=2)

plt.title('Comparativa de Rendimiento: Multiplicación de Matrices $O(n^3)$', fontsize=14)
plt.xlabel('Dimensión de la matriz (N x N)', fontsize=12)
plt.ylabel('Tiempo de Ejecución (Mediana en ms)', fontsize=12)
plt.yscale('log')  # Escala logarítmica para apreciar las diferencias
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend(fontsize=12)

plt.tight_layout()
plt.savefig('grafico_rendimiento.png', dpi=300)
print("Gráfico guardado exitosamente como 'grafico_rendimiento.png'.")