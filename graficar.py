import matplotlib.pyplot as plt

# Datos de las mediciones
dimensiones = [10, 50, 100, 250, 500]
python_ms = [0.0821, 19.3177, 85.8839, 1230.9025, 13434.5841]
c_ms = [0.0032, 0.4144, 5.0923, 54.4300, 564.5969]
java_ms = [0.0323, 5.2982, 2.6990, 14.7058, 157.4427]

plt.figure(figsize=(10, 6))
plt.plot(dimensiones, python_ms, marker='o', label='Python', color='red', linewidth=2)
plt.plot(dimensiones, c_ms, marker='s', label='C', color='blue', linewidth=2)
plt.plot(dimensiones, java_ms, marker='^', label='Java', color='green', linewidth=2)

plt.title('Comparativa de Rendimiento: Multiplicación de Matrices $O(n^3)$', fontsize=14)
plt.xlabel('Dimensión de la matriz (N x N)', fontsize=12)
plt.ylabel('Tiempo de Ejecución (ms)', fontsize=12)
plt.yscale('log')  # Escala logarítmica para apreciar las diferencias claramente
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend(fontsize=12)

plt.tight_layout()
plt.savefig('grafico_rendimiento.png', dpi=300)
print("Gráfico guardado exitosamente como 'grafico_rendimiento.png'.")