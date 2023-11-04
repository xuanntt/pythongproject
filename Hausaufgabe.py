# Import required libraries
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from math import sqrt

class DataProcessor:
    def __init__(self, training_data_file, ideal_functions_file, test_data_file):
        try:
            # Create SQLAlchemy engine
            self.engine = create_engine("sqlite:///data.db")
            # Load training data, ideal functions, and test data from CSV files
            self.training_data = pd.read_csv("train.csv")
            self.ideal_functions = pd.read_csv("ideal.csv")
            self.test_data = pd.read_csv("test.csv")
        except Exception as e:
            print(f"An error occured during initializiation: {str(e)}")
            self.engine = None
            self.training_data = None
            self.ideal_functions = None
            self.test_data = None
        # Initialize empty lists to store best fits and deviations
        self.best_fits = []
        self.deviations = []

    def find_best_fits(self):
        # Iterate through the four training datasets
        for i in range(1, 5):
            # Calculate sum of squared deviations for each ideal function
            deviations = (self.ideal_functions.drop(columns=["x"]) - self.training_data[f"y{i}"]) ** 2
            # Find the index of the ideal function with the minimum deviation
            best_fit_index = deviations.sum(axis=1).idxmin()
            self.best_fits.append(best_fit_index)

    def validate_selection(self):
        for i in range(4):
            ideal_function = self.ideal_functions.iloc[:, self.best_fits[i]]
            deviation = abs(ideal_function - self.test_data["y"])
            max_deviation = deviation.max()
            self.deviations.append(max_deviation)

    def save_to_db(self):
        # Save training data, ideal functions, and test data to SQLite database
        self.training_data.to_sql("training_data", self.engine, if_exists='replace')
        self.ideal_functions.to_sql("ideal_functions", self.engine, if_exists='replace')
        self.test_data.to_sql("test_data", self.engine, if_exists='replace')

    def plot_data(self):
        # Plot training data
        plt.figure()
        for i in range(4):
            plt.scatter(self.training_data["x"], self.training_data[f'y{i+1}'], label=f'Training Data y{i+1}')
        # Add title and axis labels
        plt.title("Training Data")
        plt.xlabel("x")
        plt.ylabel("y")
        # Add legend to the plot
        plt.legend()
        # Show the plot
        plt.show()

        # Plot the four best fits
        plt.figure()
        for i in range(4):
            plt.plot(self.ideal_functions["x"], self.ideal_functions.iloc[:,self.best_fits[i]], label=f'Ideal Function y{i+1}')
        # Add title and axis labels
        plt.title("Ideal Functions")
        plt.xlabel("x")
        plt.ylabel("y")
        # Add legend to the plot
        plt.legend()
        # Show the plot
        plt.show()

        # Plot test data
        plt.figure()
        plt.scatter(self.test_data["x"], self.test_data["y"], label="Test Data")
        # Add title and axis labels
        plt.title("Test Data")
        plt.xlabel("x")
        plt.ylabel("y")
        # Show the plot
        plt.show()

def main():
    try:
        # Create DataProcessor object
        data_processor = DataProcessor("train.csv", "ideal.csv", "test.csv")
        # Find the four best fits
        data_processor.find_best_fits()
        # Validate the selection using the test data
        data_processor.validate_selection()
        # Save data to SQLite database
        data_processor.save_to_db()
        # Plot the data
        data_processor.plot_data()
    except DataLoadError as e:
        print(f"Data loading error: {str(e)}")
    except Exception as e:
        print(f"An error occured in the main process: {str(e)}")

# Run the main function
if __name__ == "__main__":
    main()


