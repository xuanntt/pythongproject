import unittest
import pandas as pd
from main import DataProcessor


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.training_data = pd.read_csv("train.csv")
        self.ideal_functions = pd.read_csv("ideal.csv")
        self.test_data = pd.read_csv("test.csv")
        self.data_processor = DataProcessor(self.training_data, self.ideal_functions, self.test_data)

    def test_init(self):
        self.assertIsInstance(self.data_processor, DataProcessor)
        self.assertIsInstance(self.data_processor.training_data, pd.DataFrame)
        self.assertIsInstance(self.data_processor.ideal_functions, pd.DataFrame)
        self.assertIsInstance(self.data_processor.test_data, pd.DataFrame)

    def test_find_best_fits(self):
        self.data_processor.find_best_fits()
        self.assertIsInstance(self.data_processor.best_fits, list)
        self.assertGreaterEqual(len(self.data_processor.best_fits), 4)

    def test_validate_selection(self):
        self.data_processor.find_best_fits()
        self.data_processor.validate_selection()
        self.assertIsInstance(self.data_processor.best_fits, list)
        self.assertEqual(len(self.data_processor.best_fits), 4)

    def test_save_to_db(self):
        self.data_processor.find_best_fits()
        self.data_processor.validate_selection()
        self.data_processor.save_to_db()
        # Assert that the data was correctly saved to the database

    def test_plot_data(self):
        self.data_processor.find_best_fits()
        self.data_processor.validate_selection()
        self.data_processor.plot_data()
        # Assert that the plots were correctly generated

if __name__ == '__main__':
    unittest.main()

