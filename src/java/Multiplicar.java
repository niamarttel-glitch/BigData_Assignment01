import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.Locale;
import java.util.Scanner;

public class Multiplicar {

    public static void multiplicarTripleBucle(int n, double[][] A, double[][] B, double[][] C) {
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

    public static void testCorrectitud() {
        double[][] A = {{1.0, 2.0}, {3.0, 4.0}};
        double[][] B = {{2.0, 0.0}, {1.0, 2.0}};
        double[][] C = new double[2][2];
        double[][] esperado = {{4.0, 4.0}, {10.0, 8.0}};

        multiplicarTripleBucle(2, A, B, C);

        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                if (Math.abs(C[i][j] - esperado[i][j]) > 1e-6) {
                    System.out.println("Error en la validacion de correctitud.");
                    System.exit(1);
                }
            }
        }
        System.out.println("Correctitud validada exitosamente con matriz de prueba 2x2.");
    }

    public static void main(String[] args) {
        String nombreArchivo = (args.length > 0) ? args[0] : "data/matrices_3.txt";
        int n = 0;
        double[][] A = null, B = null, C = null;

        try {
            Scanner scanner = new Scanner(new File(nombreArchivo));
            scanner.useLocale(Locale.US);

            if (scanner.hasNextInt()) {
                n = scanner.nextInt();
            } else {
                System.out.println("Error al leer la dimensión.");
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
            System.out.println("No se encontró el archivo: " + nombreArchivo);
            return;
        }

        // Validación
        testCorrectitud();

        // 1. Warm-up
        multiplicarTripleBucle(n, A, B, C);

        // 2. Medición de 5 repeticiones
        int numRepeticiones = 5;
        double[] tiemposMs = new double[numRepeticiones];

        System.out.printf("--- Midiendo Java (%dx%d) ---\n", n, n);
        double sumaTiempos = 0.0;

        for (int rep = 0; rep < numRepeticiones; rep++) {
            long inicio = System.nanoTime();
            multiplicarTripleBucle(n, A, B, C);
            long fin = System.nanoTime();

            double tiempoMs = (fin - inicio) / 1_000_000.0;
            tiemposMs[rep] = tiempoMs;
            sumaTiempos += tiempoMs;
            System.out.printf(Locale.US, "Repetición %d: %.4f ms\n", rep + 1, tiempoMs);
        }

        // 3. Medición de Memoria (Heap usado)
        Runtime runtime = Runtime.getRuntime();
        runtime.gc(); // Sugerir recolección de basura para una lectura más limpia
        double memoriaMB = (runtime.totalMemory() - runtime.freeMemory()) / (1024.0 * 1024.0);

        // 4. Cálculos estadísticos
        double media = sumaTiempos / numRepeticiones;
        double sumaVarianzas = 0.0;
        for (int i = 0; i < numRepeticiones; i++) {
            sumaVarianzas += Math.pow(tiemposMs[i] - media, 2);
        }
        double variabilidadMs = Math.sqrt(sumaVarianzas / numRepeticiones);

        Arrays.sort(tiemposMs);
        double medianaMs = tiemposMs[numRepeticiones / 2];

        System.out.println("\n--- Resultados ---");
        System.out.printf(Locale.US, "Mediana: %.4f ms\n", medianaMs);
        System.out.printf(Locale.US, "Variabilidad (StdDev): %.4f ms\n", variabilidadMs);
        System.out.printf(Locale.US, "Uso de Memoria (Heap): %.4f MB\n", memoriaMB);
    }
}