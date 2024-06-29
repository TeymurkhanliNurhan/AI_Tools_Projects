package Perceptron;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class Perceptron2 {
    private double[] weights;
    private double learningRate;
    private double threshold = 0.2; // Initial threshold

    public Perceptron2(int inputSize, double learningRate) {
        // Initialize weights and threshold
        weights = new double[inputSize];
        for (int i = 0; i < inputSize; i++) {
            weights[i] = Math.random() * 0.1; // Small random value close to 0
        }
        this.learningRate = learningRate;
    }

    public void train(ArrayList<double[]> trainingData, int epochs) {
        for (int epoch = 0; epoch < epochs; epoch++) {
            Collections.shuffle(trainingData);
            for (double[] data : trainingData) {
                double predicted = predict(data);
                double error = data[data.length - 1] - predicted;
                // Update weights and threshold
                for (int i = 0; i < weights.length; i++) {
                    weights[i] += learningRate * error * data[i];
                }
                threshold += learningRate * error;
            }
            // Test accuracy after each epoch
            System.out.println("Epoch " + (epoch + 1) + ": " + test(trainingData) + "% accuracy");
        }
    }

    public double predict(double[] inputs) {
        double sum = 0.0;
        for (int i = 0; i < weights.length; i++) {
            sum += weights[i] * inputs[i];
        }
        return sum >= threshold ? 1.0 : 0.0;
    }

    public double test(ArrayList<double[]> testData) {
        int correct = 0;
        for (double[] data : testData) {
            double predicted = predict(data);
            if (predicted == data[data.length - 1]) {
                correct++;
            }
        }
        return 100.0 * correct / testData.size();
    }

    public static ArrayList<double[]> loadData(String path, boolean isIrisVirginica) throws FileNotFoundException {
        Scanner scanner = new Scanner(new File(path));
        ArrayList<double[]> dataSet = new ArrayList<>();
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine();
            String[] parts = line.split(",");
            double[] data = new double[parts.length];
            for (int i = 0; i < parts.length - 1; i++) {
                data[i] = Double.parseDouble(parts[i]);
            }
            data[data.length - 1] = parts[parts.length - 1].equals("Iris-virginica") == isIrisVirginica ? 1.0 : 0.0;
            dataSet.add(data);
        }
        scanner.close();
        return dataSet;
    }

    public static void main(String[] args) throws FileNotFoundException {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter path to training data:");
        String trainingPath = scanner.next();
        System.out.println("Enter path to test data:");
        String testPath = scanner.next();
        System.out.println("Enter learning rate:");
        double learningRate = scanner.nextDouble();
        System.out.println("Enter number of epochs:");
        int epochs = scanner.nextInt();

        // Assuming the last column is the class label and there are 4 features
        Perceptron2 perceptron = new Perceptron2(4, learningRate);

        ArrayList<double[]> trainingData = loadData(trainingPath, true);
        ArrayList<double[]> testData = loadData(testPath, true);

        perceptron.train(trainingData, epochs);
        System.out.println("Final Test Accuracy: " + perceptron.test(testData) + "%");

        // Predicting new observations
        while (true) {
            System.out.println("Enter new observation (4 attributes separated by space) or type 'exit':");
            if (scanner.hasNext("exit")) {
                System.out.println("Exiting program.");
                break;
            }
            double[] newObservation = new double[4];
            for (int i = 0; i < 4; i++) {
                if (scanner.hasNextDouble()) {
                    newObservation[i] = scanner.nextDouble();
                } else {
                    System.out.println("Invalid input. Please enter 4 numerical values separated by spaces.");
                    scanner.next(); // consume the invalid input
                }
            }
            double prediction = perceptron.predict(newObservation);
            System.out.println("Predicted class: " + (prediction == 1.0 ? "Iris-virginica" : "Iris-versicolor"));
        }
        scanner.close();
    }
}
