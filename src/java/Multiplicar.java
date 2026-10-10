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

    public static void main(String[] args) {
        // Lee la ruta pasada como argumento o usa la ruta por defecto
        String nombreArchivo = (args.length > 0) ? args[0] : "data/matrices_3.txt";

        try {
            File archivo = new File(nombreArchivo);
            Scanner scanner = new Scanner(archivo);
            scanner.useLocale(Locale.US);

            if (!scanner.hasNextInt()) {
                System.out.println("Error al leer la dimensión.");
                scanner.close();
                return;
            }

            int n = scanner.nextInt();

            double[][] A = new double[n][n];
            double[][] B = new double[n][n];
            double[][] C = new double[n][n];

            // Cargar datos fuera de la región de tiempo
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

            // 1. Warm-up (Ejecución de calentamiento)
            multiplicarTripleBucle(n, A, B, C);

            // 2. Medición de 5 repeticiones
            int numRepeticiones = 5;
            double[] tiemposMs = new double[numRepeticiones];

            System.out.println("--- Midiendo Java (" + n + "x" + n + ") ---");
            for (int rep = 0; rep < numRepeticiones; rep++) {
                long inicio = System.nanoTime();
                multiplicarTripleBucle(n, A, B, C);
                long fin = System.nanoTime();

                double tiempoMs = (fin - inicio) / 1_000_000.0;
                tiemposMs[rep] = tiempoMs;
                System.out.printf(Locale.US, "Repetición %d: %.4f ms\n", rep + 1, tiempoMs);
            }

            // 3. Obtención de la mediana
            double[] tiemposOrdenados = tiemposMs.clone();
            Arrays.sort(tiemposOrdenados);
            double medianaMs = tiemposOrdenados[numRepeticiones / 2];

            System.out.println("\n--- Resultados ---");
            System.out.printf(Locale.US, "Mediana: %.4f ms\n", medianaMs);

        } catch (FileNotFoundException e) {
            System.out.println("No se encontró el archivo: " + nombreArchivo);
        }
    }
}