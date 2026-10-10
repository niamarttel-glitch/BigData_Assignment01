import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.Locale;
import java.util.Scanner;

public class Multiply {

    public static void tripleLoopMultiply(int n, double[][] A, double[][] B, double[][] C) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                C[i][j] = 0.0;
            }
        }
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
    }

    public static void testCorrectness() {
        double[][] A = {{1.0, 2.0}, {3.0, 4.0}};
        double[][] B = {{2.0, 0.0}, {1.0, 2.0}};
        double[][] C = new double[2][2];
        double[][] expected = {{4.0, 4.0}, {10.0, 8.0}};

        tripleLoopMultiply(2, A, B, C);

        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                if (Math.abs(C[i][j] - expected[i][j]) > 1e-6) {
                    System.out.println("Error in correctness validation.");
                    System.exit(1);
                }
            }
        }
        System.out.println("Correctness successfully validated with 2x2 test matrix.");
    }

    public static void main(String[] args) {
        String filename = (args.length > 0) ? args[0] : "data/matrix_3.txt";
        int n = 0;
        double[][] A = null, B = null, C = null;

        try {
            Scanner scanner = new Scanner(new File(filename));
            scanner.useLocale(Locale.US);

            if (scanner.hasNextInt()) {
                n = scanner.nextInt();
            } else {
                System.out.println("Error reading the dimension.");
                return;
            }

            A = new double[n][n];
            B = new double[n][n];
            C = new double[n][n];

            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    A[i][j] = scanner.nextDouble();
                }
            }
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    B[i][j] = scanner.nextDouble();
                }
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            System.out.println("File not found: " + filename);
            return;
        }

        // Validation
        testCorrectness();

        // 1. Warm-up
        tripleLoopMultiply(n, A, B, C);

        // 2. Measurement of 5 repetitions
        int numRepetitions = 5;
        double[] timesMs = new double[numRepetitions];

        System.out.printf("--- Measuring Java (%dx%d) ---\n", n, n);
        double sumTimes = 0.0;

        for (int rep = 0; rep < numRepetitions; rep++) {
            long start = System.nanoTime();
            tripleLoopMultiply(n, A, B, C);
            long end = System.nanoTime();

            double timeMs = (end - start) / 1_000_000.0;
            timesMs[rep] = timeMs;
            sumTimes += timeMs;
            System.out.printf(Locale.US, "Repetition %d: %.4f ms\n", rep + 1, timeMs);
        }

        // 3. Memory Measurement (Heap used)
        Runtime runtime = Runtime.getRuntime();
        runtime.gc(); // Suggest garbage collection for a cleaner reading
        double memoryMB = (runtime.totalMemory() - runtime.freeMemory()) / (1024.0 * 1024.0);

        // 4. Statistical calculations
        double mean = sumTimes / numRepetitions;
        double sumVariances = 0.0;
        for (int i = 0; i < numRepetitions; i++) {
            sumVariances += Math.pow(timesMs[i] - mean, 2);
        }
        double variabilityMs = Math.sqrt(sumVariances / numRepetitions);

        Arrays.sort(timesMs);
        double medianMs = timesMs[numRepetitions / 2];

        System.out.println("\n--- Results ---");
        System.out.printf(Locale.US, "Median: %.4f ms\n", medianMs);
        System.out.printf(Locale.US, "Variability (StdDev): %.4f ms\n", variabilityMs);
        System.out.printf(Locale.US, "Memory Use (Heap): %.4f MB\n", memoryMB);
    }
}