# Big Data Assignment 01: Matrix Multiplication Benchmark

**Author:** Daniela Eridenia Martel Valido  
**Course:** Big Data - University of Las Palmas de Gran Canaria (GCID)

## Description
This repository contains the source code and reproducibility materials for a comparative study on the performance and memory usage of a basic $O(n^3)$ matrix multiplication algorithm implemented in **Python**, **C**, and **Java**.

## Project Structure
```text
.
├── src/
│   ├── c/
│   │   └── multiply.c       # C implementation
│   ├── java/
│   │   └── Multiply.java    # Java implementation
│   └── python/
│       ├── generator.py     # Random matrix generator
│       ├── multiply.py      # Python implementation
│       ├── benchmark.py     # Orchestrator script for compilation and execution
│       └── plot.py          # Script to generate the performance graph
├── data/                    # Generated matrix text files (auto-generated)
├── results.md               # Markdown table with the output metrics (auto-generated)
├── performance_graph.png    # Performance plot (auto-generated)
└── README.md                # This file
```


## Prerequisites
To reproduce this benchmark on a Windows machine, ensure you have the following installed and added to your system's PATH:

1. Python 3.x (with matplotlib installed: pip install matplotlib).

2. GCC Compiler (MinGW or similar) to compile the C code.

3. Java Development Kit (JDK 17 or higher) to compile and run the Java code.

## How to Reproduce the Experiment
**1. Run the Benchmark**
The entire process (compiling C and Java code, generating matrices of sizes 10 to 500, and measuring execution time and memory) is fully automated by the benchmark.py script.

Run the following command from the root directory of the project:
python src/python/benchmark.py


Note: The execution for $N=500$ in Python will take a significant amount of time (approx. 100 seconds). Please let the script finish. Once completed, it will automatically generate the results.md file.


**2. Generate the Plot**
After the benchmark has finished and generated the results.md file, you can generate the comparative logarithmic chart by running:
python src/python/plot.py

This will read the generated metrics and save a performance_graph.png image in the root directory.



## Hardware Environment Used for the Report
CPU: 12th Gen Intel Core i5-12450H (2.00 GHz)

RAM: 16 GB

OS: Windows 11 Home

