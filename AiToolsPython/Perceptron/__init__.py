import csv
import random
from sklearn.preprocessing import LabelEncoder

class PerceptronClassifier:
    def __init__(self, learning_rate, num_epochs):
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs
        self.weights = None
        self.threshold = None
        self.label_encoder = LabelEncoder()

    def load_training_data(self, file_path):
        return self.read_data_file(file_path)

    def load_test_data(self, file_path):
        return self.read_data_file(file_path)

    def read_data_file(self, file_path):
        data = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2:
                    continue
                features = list(map(float, row[:-1]))
                label = row[-1]
                data.append((features, label))
        return data

    def encode_labels(self, labels):
        self.label_encoder.fit(labels)

    def initialize_weights(self, num_features):
        self.weights = [random.uniform(-0.1, 0.1) for _ in range(num_features)]
        self.threshold = random.uniform(-0.1, 0.1)

    def predict(self, features):
        activation = sum(weight * feature for weight, feature in zip(self.weights, features)) + self.threshold
        return 1 if activation >= 0 else 0

    def train(self, training_data, test_data):
        num_features = len(training_data[0][0])
        self.initialize_weights(num_features)

        for epoch in range(self.num_epochs):
            random.shuffle(training_data)
            for features, label in training_data:
                prediction = self.predict(features)
                encoded_label = self.label_encoder.transform([label])[0]
                error = encoded_label - prediction
                if error != 0:
                    for i in range(num_features):
                        self.weights[i] += self.learning_rate * error * features[i]
                    self.threshold += self.learning_rate * error

            accuracy = self.test(test_data)
            print(f"Epoch {epoch + 1}: Accuracy: {accuracy:.2f}%")

    def test(self, test_data):
        correct_predictions = 0
        total_instances = len(test_data)
        for features, label in test_data:
            prediction = self.predict(features)
            encoded_label = self.label_encoder.transform([label])[0]
            if prediction == encoded_label:
                correct_predictions += 1
        return (correct_predictions / total_instances) * 100

    def classify_user_instance(self, features):
        prediction = self.predict(features)
        print("Predicted class:", self.label_encoder.inverse_transform([prediction])[0])

def main():
    while True:
        print("\nOptions:")
        print("1) Work with example dataset")
        print("2) Work with iris dataset")
        print("3) Exit")

        option = input("Select an option: ").lower()

        if option == '1':
            training_file_path = input("Enter the path to the example training: ")
            test_file_path = input("Enter the path to the example test: ")
            learning_rate = float(input("Enter the learning rate: "))
            num_epochs = int(input("Enter the number of epochs: "))

            classifier = PerceptronClassifier(learning_rate, num_epochs)

            training_data = classifier.load_training_data(training_file_path)
            test_data = classifier.load_test_data(test_file_path)
            labels = [label for _, label in training_data]
            classifier.encode_labels(labels)

            classifier.train(training_data, test_data)

            while True:
                print("\nOptions:")
                print("a) Classify user instance")
                print("b) Exit")

                sub_option = input("Select an option: ").lower()

                if sub_option == 'a':
                    user_instance = list(
                        map(float, input("Enter the features of the instance separated by commas: ").split(',')))
                    classifier.classify_user_instance(user_instance)
                elif sub_option == 'b':
                    break
                else:
                    print("Invalid option. Please choose again.")

        elif option == '2':

            training_file_path = input("Enter the path to the training file for generic dataset: ")

            test_file_path = input("Enter the path to the test file for generic dataset: ")

            learning_rate = float(input("Enter the learning rate: "))

            num_epochs = int(input("Enter the number of epochs: "))

            classifier = PerceptronClassifier(learning_rate, num_epochs)

            training_data = classifier.load_training_data(training_file_path)

            test_data = classifier.load_test_data(test_file_path)  # Load test data

            labels = [label for _, label in training_data]

            classifier.encode_labels(labels)

            classifier.train(training_data, test_data)  # Pass both training and test data

            while True:

                print("\nOptions:")

                print("a) Classify user instance")

                print("b) Exit")

                sub_option = input("Select an option: ").lower()

                if sub_option == 'a':

                    user_instance = list(

                        map(float, input("Enter the features of the instance separated by commas: ").split(',')))

                    classifier.classify_user_instance(user_instance)

                elif sub_option == 'b':

                    break

                else:

                    print("Invalid option. Please choose again.")



        elif option == '3':
            print("Exiting the program...")
            break


        else:
            print("Invalid option. Please choose again.")



if __name__ == "__main__":
    main()
