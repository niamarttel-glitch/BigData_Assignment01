import sys
import random

def generate_matrices(n, filename):
    with open(filename, 'w') as f:
        # 1. Write the size
        f.write(f"{n}\n")
        
        # 2. Generate and write Matrix A
        for _ in range(n):
            row = [str(float(random.randint(1, 10))) for _ in range(n)]
            f.write(" ".join(row) + "\n")
            
        # 3. Generate and write Matrix B
        for _ in range(n):
            row = [str(float(random.randint(1, 10))) for _ in range(n)]
            f.write(" ".join(row) + "\n")

if __name__ == "__main__":
    # Read 'n' and 'filename' from the console if they exist, or use default values
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    filename = sys.argv[2] if len(sys.argv) > 2 else f"data/matrix_{n}.txt"
    
    generate_matrices(n, filename)
    print(f"File '{filename}' ({n}x{n}) successfully generated.")