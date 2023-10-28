import unittest
import numpy as np
import sqlite3
import pandas as pd
from etl.etl import extract, transform


class TestExtractFunction(unittest.TestCase):

    def test_extract(self):
        url = 'https://www.passportindex.org/byRank.php'
        df = extract(url)
        self.assertIsNotNone(df)

        # Check if the DataFrame has 5 columns
        self.assertEqual(len(df.columns), 5)

    def test_transform(self):
        url = 'https://www.passportindex.org/byRank.php'
        df = extract(url)
        transformed_df = transform(df)

        # Check for 'get_alpha_3' columns
        self.assertTrue('country_id' in transformed_df.columns)

        # Check if the columns for visa information contain integers
        self.assertTrue(np.issubdtype(transformed_df['power_rank'].dtype, np.integer))
        self.assertTrue(np.issubdtype(transformed_df['visa_free'].dtype, np.integer))
        self.assertTrue(np.issubdtype(transformed_df['visa_on_arrival'].dtype, np.integer))
        self.assertTrue(np.issubdtype(transformed_df['visa_required'].dtype, np.integer))

        # Check the number of power_rank
        distinct_count = transformed_df['power_rank'].nunique()
        self.assertEqual(distinct_count, 93, "Distinct power_rank count is not 93")

        # Check the number of countries
        number_of_countries = transformed_df['country'].nunique()
        self.assertEqual(number_of_countries, 199, "Distinct country count is not 199")

        # Check for null values in the DataFrame
        null_values = transformed_df.isnull().sum()
        self.assertEqual(null_values.sum(), 0, "There are null values in the DataFrame")

        # Check for 'n/a' values
        na_values = transformed_df.isin(['n/a']).any().any()
        self.assertFalse(na_values, "The DataFrame contains 'n/a' values")

         # Check if the string values in rows are stripped
        columns_to_check = ['country_id',
                            'country',
                            'power_rank',
                            'visa_free',
                            'visa_on_arrival',
                            'visa_required']

        for column in columns_to_check:
            stripped_values = transformed_df[column].apply(lambda x: x.strip() if isinstance(x, str) else x)
            self.assertTrue((transformed_df[column] == stripped_values).all(), f"Values in {column} column are not stripped")

    def test_uniqueness(self):
        # Connect to the SQLite database and fetch data
        conn = sqlite3.connect('passport_index.db')
        query = "SELECT * FROM passport_data;"
        loaded_data = pd.read_sql_query(query, conn)
        conn.close()

        # Check the uniqueness of 'country', 'alpha_2_code', and 'alpha_3_code' columns
        unique_country = loaded_data['country_id'].is_unique
        unique_alpha_3 = loaded_data['country'].is_unique

        self.assertTrue(unique_country, "The 'country_id' column is not unique")
        self.assertTrue(unique_alpha_3, "The 'country' column is not unique")


if __name__ == '__main__':
    unittest.main()
