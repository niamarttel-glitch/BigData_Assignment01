import sys
import random

def generar_matrices(n, nombre_archivo):
    with open(nombre_archivo, 'w') as f:
        # 1. Escribir el tamaño
        f.write(f"{n}\n")
        
        # 2. Generar y escribir Matriz A
        for _ in range(n):
            fila = [str(float(random.randint(1, 10))) for _ in range(n)]
            f.write(" ".join(fila) + "\n")
            
        # 3. Generar y escribir Matriz B
        for _ in range(n):
            fila = [str(float(random.randint(1, 10))) for _ in range(n)]
            f.write(" ".join(fila) + "\n")

if __name__ == "__main__":
    # Lee 'n' y 'nombre_archivo' de la consola si existen, o usa valores por defecto
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    archivo = sys.argv[2] if len(sys.argv) > 2 else f"data/matrices_{n}.txt"
    
    generar_matrices(n, archivo)
    print(f"Archivo '{archivo}' ({n}x{n}) generado con éxito.")