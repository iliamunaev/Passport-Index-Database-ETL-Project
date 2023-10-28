from datetime import datetime
import sqlite3
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import country_converter as coco


def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    print(f'{timestamp}:{message}')

    with open("etl_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(timestamp + ':' + message + '\n')


def extract(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        countries = []
        for section in soup.find_all(class_=re.compile(r'gpr_\d+')):
            country_name = section.find(class_='name_country').text.strip()
            power_rank = int(section['data-pr'])
            visa_free = int(section.find(class_='rank vf').text.strip())
            visa_on_arrival = int(section.find(class_='rank voa').text.strip())
            visa_required = int(section.find(class_='rank vr').text.strip())

            countries.append({
                'country': country_name,
                'power_rank': power_rank,
                'visa_free': visa_free,
                'visa_on_arrival': visa_on_arrival,
                'visa_required': visa_required
            })

        df = pd.DataFrame(countries)
        return df

    except requests.HTTPError as e:
        error_message = f"HTTP error occurred: {e}"
        print(error_message)
        log_progress(error_message)
        return None
    except requests.RequestException as e:
        error_message = f"Request exception occurred: {e}"
        print(error_message)
        log_progress(error_message)
        return None


def transform(df):
    try:
        df['country_id'] = coco.convert(names=df['country'], to='ISO3')
        df.loc[df['country_id'].isna(), 'country_id'] = 'n/a'
        
        # Reordering columns with country_id as the first column
        cols = list(df.columns)
        cols.insert(0, cols.pop(cols.index('country_id')))
        df = df[cols]
        
        return df
    except Exception as e:
        error_message = f"Error during transformation: {e}"
        print(error_message)
        log_progress(error_message)
        return df  # Return the original DataFrame in case of an error

def load(df):
    try:
        conn = sqlite3.connect('passport_index.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='passport_data'")
        result = cursor.fetchone()

        if not result:
            cursor.execute('''
                CREATE TABLE passport_data (
                    country_id TEXT,
                    country TEXT,
                    power_rank INTEGER,
                    visa_free INTEGER,
                    visa_on_arrival INTEGER,
                    visa_required INTEGER                    
                )
            ''')
            conn.commit()

        df.to_sql('passport_data', conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        error_message = f"Error occurred while writing to the SQLite database: {e}"
        print(error_message)
        log_progress(error_message)
    except Exception as e:
        error_message = f"Other error occurred: {e}"
        print(error_message)
        log_progress(error_message)
