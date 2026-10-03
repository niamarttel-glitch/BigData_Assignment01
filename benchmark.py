import os
import subprocess
import re

tamanios = [10, 50, 100, 250, 500]
data_dir = "data"
results = {n: {} for n in tamanios}

os.makedirs(data_dir, exist_ok=True)

print("=== 1. COMPILACIÓN DE CÓDIGOS ===")
# Compilar C
print("Compilando C...")
res_c = subprocess.run(["gcc", "src/c/multiplicar.c", "-o", "src/c/multiplicar.exe"], capture_output=True, text=True)
if res_c.returncode != 0:
    print("Error al compilar C:", res_c.stderr)

# Compilar Java
print("Compilando Java...")
res_java = subprocess.run(["javac", "src/java/Multiplicar.java"], capture_output=True, text=True)
if res_java.returncode != 0:
    print("Error al compilar Java:", res_java.stderr)

print("\n=== 2. GENERACIÓN DE MATRICES ===")
for n in tamanios:
    filepath = os.path.join(data_dir, f"matrices_{n}.txt")
    if not os.path.exists(filepath):
        print(f"Generando {filepath}...")
        subprocess.run(["python", "src/python/generador.py", str(n), filepath])

def extraer_mediana(salida):
    match = re.search(r"Mediana:\s*([\d\.]+)\s*ms", salida)
    if match:
        return float(match.group(1))
    return None

print("\n=== 3. EJECUCIÓN DE BENCHMARKS ===")
for n in tamanios:
    archivo_matriz = os.path.join(data_dir, f"matrices_{n}.txt")
    print(f"\n---> Evaluando n = {n} <---")
    
    # Python
    out_py = subprocess.run(["python", "src/python/multiplicar.py", archivo_matriz], capture_output=True, text=True).stdout
    mediana_py = extraer_mediana(out_py)
    results[n]['Python'] = mediana_py
    print(f"  Python: {mediana_py} ms")
    
    # C
    out_c = subprocess.run(["./src/c/multiplicar.exe", archivo_matriz], capture_output=True, text=True).stdout
    mediana_c = extraer_mediana(out_c)
    results[n]['C'] = mediana_c
    print(f"  C:      {mediana_c} ms")
    
    # Java
    out_java = subprocess.run(["java", "-cp", "src/java", "Multiplicar", archivo_matriz], capture_output=True, text=True).stdout
    mediana_java = extraer_mediana(out_java)
    results[n]['Java'] = mediana_java
    print(f"  Java:   {mediana_java} ms")

print("\n\n=============================================")
print("          TABLA DE RESULTADOS (ms)           ")
print("=============================================")
markdown_table = "| Dimensión (n) | Python (ms) | C (ms) | Java (ms) |\n"
markdown_table += "|---------------|-------------|--------|-----------|\n"

for n in tamanios:
    py_t = f"{results[n]['Python']:.4f}" if results[n]['Python'] is not None else "Error"
    c_t = f"{results[n]['C']:.4f}" if results[n]['C'] is not None else "Error"
    java_t = f"{results[n]['Java']:.4f}" if results[n]['Java'] is not None else "Error"
    markdown_table += f"| {n}x{n} | {py_t} | {c_t} | {java_t} |\n"

print(markdown_table)

with open("resultados.md", "w", encoding="utf-8") as f:
    f.write("# Resultados de Benchmarking\n\n")
    f.write(markdown_table)

print("Resultados guardados exitosamente en 'resultados.md'.")