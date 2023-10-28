
# Passport Index Database

This project compiles and manages data showcasing the global travel access potential of different countries' passports. It scrapes the data from [passportindex.org](https://www.passportindex.org/byRank.php), adds an ID column, showcasing countries' names in unique ISO3 codes, and stores the data in a SQLite database "passport_index.db" with 'passport_data' table.

The database offers insights into the comparative strength of passports concerning visa-free or visa-on-arrival access to various countries worldwide.

## Table of Contents
- [Table Schema for `passport_data`](#table-schema-for-passport_data)
- [Sample Data from `passport_data`](#sample-data-from-passport_data)
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
- [ETL Functions Test Cases](##etl-functions-test-cases)
- [Tools and Libraries](##tools-and-libraries)
- [License](#license)
- [Contact](#contact)


## Table Schema for `passport_data`

| Column Name      | Data Type       |
|------------------|-----------------|
| country_id       | TEXT            |
| country          | TEXT            |
| power_rank       | INTEGER         |
| visa_free        | INTEGER         |
| visa_on_arrival  | INTEGER         |
| visa_required    | INTEGER         |

## Sample Data from `passport_data`

| country_id | country             | power_rank | visa_free | visa_on_arrival | visa_required |
|------------|---------------------|------------|-----------|-----------------|---------------|
| ARE        | United Arab Emirates| 1          | 129       | 51              | 18            |
| SWE        | Sweden              | 2          | 133       | 43              | 22            |
| DEU        | Germany             | 2          | 133       | 43              | 22            |
| FIN        | Finland             | 2          | 133       | 43              | 22            |
| ESP        | Spain               | 2          | 133       | 43              | 22            |


## Installation

1. Clone this repository.
2. Install the required libraries listed in the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

3. Run the main script to execute the ETL process.

## Usage

After installing the project, execute the main Python script (`main.py`) to start the ETL process and create a database.

## Functions

### `extract(url)`

The `extract` function retrieves passport index data from a provided URL through web scraping techniques, employing the **BeautifulSoup** library. It is responsible for:
- Fetching passport index data from a given URL.
- Utilizing web scraping methods with BeautifulSoup to extract the required information.
- Stripping and converting the retrieved data to ensure proper formatting and structure.

### `transform(df)`

The `transform` function processes the extracted data. This function leverages the **country_converter** library to convert country names into ISO3 codes. It conducts the following operations:
- Converts country names to ISO3 codes using the **country_converter** library.
- Adds an additional column 'country_id' for storing the ISO3 codes.
- Resides the data in a Pandas DataFrame for loading into a database on the next step.

### `load(df)`

The `load` function is responsible for persisting the transformed data into a SQLite database. This process involves the following steps:
1. **Connection Establishment:** Establishes a connection to the SQLite database.
2. **Table Verification:** Verifies the existence of the table within the database.
3. **Table Creation:** If the table does not exist, it creates a 'passport_data' table with columns for 'country_id', 'country_name', 'power_rank', 'visa_free', 'visa_on_arrival', and 'visa_required'.
4. **Data Insertion:** Stores the transformed data, represented as a Pandas DataFrame, into the 'passport_data' table within the SQLite database.


## ETL Functions Test Cases
The test suite below validates the functionality of the ETL (Extract, Transform, Load) processes for a passport index data processing system.

### `test_extract()`
- **Objective:** Validates the extraction process.
- **Process:**
    - Extracts passport index data from a specific URL.
    - Verifies that the returned DataFrame is not `None`.
    - Checks if the DataFrame contains the expected number of columns (5 columns).

### `test_transform()`
- **Objective:** Validates the transformation process for the extracted data.
- **Process:**
    - Extracts data from the URL and transforms it using the `transform` function.
    - Ensures the existence of the 'country_id' column in the transformed DataFrame.
    - Validates that columns with visa information store integer values.
    - Verifies the count of distinct values for 'power_rank' and 'country'.
    - Confirms the absence of null or 'n/a' values in the DataFrame.
    - Validates the proper stripping of string values within DataFrame columns.

### `test_uniqueness()`
- **Objective:** Ensures the uniqueness of specific columns in the loaded SQLite database.
- **Process:**
    - Connects to the SQLite database and retrieves data.
    - Checks the uniqueness of the 'country_id' and 'country' columns in the database, ensuring that these columns have unique values.

## Tools and Libraries
 - Python
 - SQLite3
 - BeautifulSoup
 - pandas
 - country_converter
 
## License

This project is licensed under the [MIT License](LICENSE). You can use, modify, and distribute the code.

## Contact

For any questions, feedback, or issues, please feel free to contact the project owner:

- Name: Ilia Munaev
- Email: ilyamunaev@gmail.com
- LinkedIn: [iliamunaev]( https://www.linkedin.com/in/iliamunaev/)