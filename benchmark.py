import os
import subprocess
import re

sizes = [10, 50, 100, 250, 500]
data_dir = "data"
results = {n: {} for n in sizes}

os.makedirs(data_dir, exist_ok=True)

print("=== 1. CODE COMPILATION ===")
# Compile C
print("Compiling C...")
res_c = subprocess.run(["gcc", "src/c/multiply.c", "-o", "src/c/multiply.exe", "-lpsapi"], capture_output=True, text=True)
if res_c.returncode != 0:
    print("Error compiling C:", res_c.stderr)

# Compile Java
print("Compiling Java...")
res_java = subprocess.run(["javac", "src/java/Multiply.java"], capture_output=True, text=True)
if res_java.returncode != 0:
    print("Error compiling Java:", res_java.stderr)

print("\n=== 2. MATRIX GENERATION ===")
for n in sizes:
    filepath = os.path.join(data_dir, f"matrix_{n}.txt")
    if not os.path.exists(filepath):
        print(f"Generating {filepath}...")
        subprocess.run(["python", "src/python/generator.py", str(n), filepath])

def extract_metrics(output):
    median = re.search(r"Median:\s*([\d\.]+)\s*ms", output)
    stddev = re.search(r"Variability \(StdDev\):\s*([\d\.]+)\s*ms", output)
    memory = re.search(r"(?:Peak Memory|Memory Use \(Heap\)):\s*([\d\.]+)\s*MB", output)
    
    return {
        'median': float(median.group(1)) if median else None,
        'stddev': float(stddev.group(1)) if stddev else None,
        'memory': float(memory.group(1)) if memory else None
    }

def format_cell(metrics):
    if metrics['median'] is not None:
        # Format: Median ± StdDev ms | Memory MB
        return f"{metrics['median']:.4f} ± {metrics['stddev']:.4f} ms | {metrics['memory']:.4f} MB"
    return "Error | Error"

print("\n=== 3. BENCHMARK EXECUTION ===")
for n in sizes:
    matrix_file = os.path.join(data_dir, f"matrix_{n}.txt")
    print(f"\n---> Evaluating n = {n} <---")
    
    # Python
    out_py = subprocess.run(["python", "src/python/multiply.py", matrix_file], capture_output=True, text=True).stdout
    results[n]['Python'] = extract_metrics(out_py)
    print(f"  Python: {results[n]['Python']['median']} ms")
    
    # C
    out_c = subprocess.run(["src/c/multiply.exe", matrix_file], capture_output=True, text=True).stdout
    results[n]['C'] = extract_metrics(out_c)
    print(f"  C:      {results[n]['C']['median']} ms")
    
    # Java
    out_java = subprocess.run(["java", "-cp", "src/java", "Multiply", matrix_file], capture_output=True, text=True).stdout
    results[n]['Java'] = extract_metrics(out_java)
    print(f"  Java:   {results[n]['Java']['median']} ms")

print("\n\n=========================================================================================")
print("                                    RESULTS TABLE                                        ")
print("=========================================================================================")

markdown_table = "| Dimension (n) | Python (Time | Memory) | C (Time | Memory) | Java (Time | Memory) |\n"
markdown_table += "|---------------|---------------------------|----------------------|-------------------------|\n"

for n in sizes:
    py_t = format_cell(results[n]['Python'])
    c_t = format_cell(results[n]['C'])
    java_t = format_cell(results[n]['Java'])
    markdown_table += f"| {n}x{n} | {py_t} | {c_t} | {java_t} |\n"

print(markdown_table)

with open("results.md", "w", encoding="utf-8") as f:
    f.write("# Benchmarking Results (Assignment 1)\n\n")
    f.write("Times are expressed as `Median ± Standard Deviation`.\n\n")
    f.write(markdown_table)

print("Results successfully saved to 'results.md'.")