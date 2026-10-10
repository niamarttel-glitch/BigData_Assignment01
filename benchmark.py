import os
import subprocess
import re

tamanios = [10, 50, 100, 250, 500]
data_dir = "data"
results = {n: {} for n in tamanios}

os.makedirs(data_dir, exist_ok=True)

print("=== 1. COMPILACIÓN DE CÓDIGOS ===")
# Compilar C (¡Nota el -lpsapi añadido!)
print("Compilando C...")
res_c = subprocess.run(["gcc", "src/c/multiplicar.c", "-o", "src/c/multiplicar.exe", "-lpsapi"], capture_output=True, text=True)
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

def extraer_metricas(salida):
    mediana = re.search(r"Mediana:\s*([\d\.]+)\s*ms", salida)
    stddev = re.search(r"Variabilidad \(StdDev\):\s*([\d\.]+)\s*ms", salida)
    memoria = re.search(r"(?:Pico de Memoria|Uso de Memoria \(Heap\)):\s*([\d\.]+)\s*MB", salida)
    
    return {
        'mediana': float(mediana.group(1)) if mediana else None,
        'stddev': float(stddev.group(1)) if stddev else None,
        'memoria': float(memoria.group(1)) if memoria else None
    }

def formato_celda(metricas):
    if metricas['mediana'] is not None:
        # Formato: Mediana ± StdDev ms (Memoria MB)
        return f"{metricas['mediana']:.4f} ± {metricas['stddev']:.4f} ms | {metricas['memoria']:.4f} MB"
    return "Error | Error"

print("\n=== 3. EJECUCIÓN DE BENCHMARKS ===")
for n in tamanios:
    archivo_matriz = os.path.join(data_dir, f"matrices_{n}.txt")
    print(f"\n---> Evaluando n = {n} <---")
    
    # Python
    out_py = subprocess.run(["python", "src/python/multiplicar.py", archivo_matriz], capture_output=True, text=True).stdout
    results[n]['Python'] = extraer_metricas(out_py)
    print(f"  Python: {results[n]['Python']['mediana']} ms")
    
    # C
    out_c = subprocess.run(["src/c/multiplicar.exe", archivo_matriz], capture_output=True, text=True).stdout
    results[n]['C'] = extraer_metricas(out_c)
    print(f"  C:      {results[n]['C']['mediana']} ms")
    
    # Java
    out_java = subprocess.run(["java", "-cp", "src/java", "Multiplicar", archivo_matriz], capture_output=True, text=True).stdout
    results[n]['Java'] = extraer_metricas(out_java)
    print(f"  Java:   {results[n]['Java']['mediana']} ms")

print("\n\n=========================================================================================")
print("                                TABLA DE RESULTADOS                                      ")
print("=========================================================================================")

markdown_table = "| Dimensión (n) | Python (Tiempo | Memoria) | C (Tiempo | Memoria) | Java (Tiempo | Memoria) |\n"
markdown_table += "|---------------|---------------------------|----------------------|-------------------------|\n"

for n in tamanios:
    py_t = formato_celda(results[n]['Python'])
    c_t = formato_celda(results[n]['C'])
    java_t = formato_celda(results[n]['Java'])
    markdown_table += f"| {n}x{n} | {py_t} | {c_t} | {java_t} |\n"

print(markdown_table)

with open("resultados.md", "w", encoding="utf-8") as f:
    f.write("# Resultados de Benchmarking (Assignment 1)\n\n")
    f.write("Los tiempos se expresan como `Mediana ± Desviación Estándar`.\n\n")
    f.write(markdown_table)

print("Resultados guardados exitosamente en 'resultados.md'.")