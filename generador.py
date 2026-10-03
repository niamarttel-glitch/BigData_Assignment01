import random

def generar_matrices(n, nombre_archivo):
    with open(nombre_archivo, 'w') as f:
        # 1. Escribir el tamaño
        f.write(f"{n}\n")
        
        # 2. Generar y escribir Matriz A (usamos floats simples para probar)
        for _ in range(n):
            fila = [str(float(random.randint(1, 10))) for _ in range(n)]
            f.write(" ".join(fila) + "\n")
            
        # 3. Generar y escribir Matriz B
        for _ in range(n):
            fila = [str(float(random.randint(1, 10))) for _ in range(n)]
            f.write(" ".join(fila) + "\n")

# Generamos una matriz de 3x3 para empezar
generar_matrices(3, "matrices_prueba_3.txt")
print("Archivo generado con éxito.")