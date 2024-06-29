package KnnAlgorithm;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the path to the training file: ");
        String trainingFilePath = scanner.nextLine();
        List<String[]> trainingData = loadData(trainingFilePath);
        System.out.print("Enter the number of neighbors (K): ");
        int k = scanner.nextInt();
        scanner.nextLine(); // Consume newline left-over
        while (true) {
            System.out.println("\n1. Classify all observations from the test set");
            System.out.println("2. Classify a single observation");
            System.out.println("3.Change k");
            System.out.println("4. Exit");
            System.out.print("Choose an option: ");
            String choice = scanner.nextLine();
            switch (choice) {
                case "1":
                    System.out.print("Enter the path to the test file: ");
                    String testFilePath = scanner.nextLine();
                    List<String[]> testData = loadData(testFilePath);
                    classifyAll(trainingData, testData, k);
                    break;
                case "2":
                    System.out.print("Enter the observation (comma-separated): ");
                    String[] testPoint = scanner.nextLine().split(",");
                    String prediction = classify(trainingData, testPoint, k);
                    System.out.println("Predicted: " + prediction);
                    break;
                case "3":
                    System.out.println("Enter the new k");
                    k = scanner.nextInt();
                    break;
                case "4":
                    System.exit(0);
                default:
                    System.out.println("Invalid option. Please try again.");
            }
        }
    }
    private static List<String[]> loadData(String filePath) {
        List<String[]> data = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                data.add(line.split(","));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return data;
    }
    private static double euclideanDistance(String[] point1, String[] point2) {
        double sum = 0.0;
        for (int i = 0; i < point1.length - 1; i++) {
            sum += Math.pow(Double.parseDouble(point1[i]) - Double.parseDouble(point2[i]), 2);
        }
        return sum;
    }
    private static String classify(List<String[]> trainingData, String[] testPoint, int k) {
        List<DistanceLabel> distances = new ArrayList<>();
        for (String[] trainingPoint : trainingData) {
            double dist = euclideanDistance(testPoint, trainingPoint);
            distances.add(new DistanceLabel(dist, trainingPoint[trainingPoint.length - 1]));
        }
        Collections.sort(distances, Comparator.comparingDouble(DistanceLabel::getDistance));
        return majorityVote(distances, k);
    }
    private static void classifyAll(List<String[]> trainingData, List<String[]> testData, int k) {
        int correct = 0;
        for (String[] testPoint : testData) {
            String prediction = classify(trainingData, testPoint, k);
            System.out.println("Test point: " + String.join(",", testPoint) + " -> Predicted: " + prediction + ", Actual: " + testPoint[testPoint.length - 1]);
            if (prediction.equals(testPoint[testPoint.length - 1])) {
                correct++;
            }
        }
        double accuracy = (double) correct / testData.size();
        System.out.println("Accuracy: " + (accuracy * 100) + "%");
    }
    private static String majorityVote(List<DistanceLabel> distances, int k) {
        Map<String, Integer> labelCounts = new HashMap<>();
        for (int i = 0; i < k; i++) {
            String label = distances.get(i).getLabel();
            labelCounts.put(label, labelCounts.getOrDefault(label, 0) + 1);
        }
        return Collections.max(labelCounts.entrySet(), Map.Entry.comparingByValue()).getKey();
    }
    private static class DistanceLabel {
        private final double distance;
        private final String label;
        public DistanceLabel(double distance, String label) {
            this.distance = distance;
            this.label = label;
        }
        public double getDistance() {
            return distance;
        }
        public String getLabel() {
            return label;
        }
    }
}