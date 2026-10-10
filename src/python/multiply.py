import time
import statistics
import sys
import tracemalloc

def read_matrices(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    n = int(lines[0])
    
    matrix_a = []
    for i in range(1, n + 1):
        matrix_a.append([float(x) for x in lines[i].split()])
        
    matrix_b = []
    for i in range(n + 1, 2 * n + 1):
        matrix_b.append([float(x) for x in lines[i].split()])
        
    return n, matrix_a, matrix_b

def triple_loop_multiply(n, A, B):
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def test_correctness():
    # Quick test with known 2x2 matrices
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[2.0, 0.0], [1.0, 2.0]]
    expected = [[4.0, 4.0], [10.0, 8.0]]
    result = triple_loop_multiply(2, A, B)
    assert result == expected, "Error in correctness validation"
    print("Correctness successfully validated with 2x2 test matrix.")

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "data/matrix_3.txt"
    n, A, B = read_matrices(filename)

    test_correctness()

    # 1. Warm-up
    _ = triple_loop_multiply(n, A, B)

    # 2. Measurement of 5 repetitions (Time and Memory)
    num_repetitions = 5
    times_ms = []
    
    # Start memory tracking
    tracemalloc.start()

    print(f"--- Measuring Python ({n}x{n}) ---")
    for rep in range(num_repetitions):
        start = time.perf_counter()
        C = triple_loop_multiply(n, A, B)
        end = time.perf_counter()
        
        time_ms = (end - start) * 1000.0
        times_ms.append(time_ms)
        print(f"Repetition {rep + 1}: {time_ms:.4f} ms")

    # Capture peak memory used
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_mb = peak / (1024 * 1024)

    # 3. Statistical results
    median_ms = statistics.median(times_ms)
    variability_ms = statistics.stdev(times_ms) if len(times_ms) > 1 else 0.0

    print("\n--- Results ---")
    print(f"Median: {median_ms:.4f} ms")
    print(f"Variability (StdDev): {variability_ms:.4f} ms")
    print(f"Peak Memory: {memory_mb:.4f} MB")