from datetime import datetime, timedelta
import pandas as pd
from xecd_rates_client import XecdClient
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
import logging
import traceback


def connect_to_api_and_extract(api_id, api_key, country_dict):
    try:
        api_conn = XecdClient(api_id, api_key)
        dictionary = {}
        
        for country, currency in country_dict.items():
            columns = ['timestamp', 'currency_from', 'USD_to_currency_rate', 'currency_to_USD_rate', 'currency_to']
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            convert_to = api_conn.convert_to(currency, "USD", 1)
            convert_from = api_conn.convert_from("USD", currency, 1)
            USD_to_currency_rate = convert_to['from'][0]['mid']
            currency_to_USD_rate = convert_from['to'][0]['mid']
            daily_rate = [[current_datetime, "USD", USD_to_currency_rate, currency_to_USD_rate, currency]]
            df = pd.DataFrame(daily_rate, columns=columns)
            dictionary[country] = df
        
        return dictionary

    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        logging.error(f"Timestamp: {datetime.now()}")
        logging.error(f"Traceback: {traceback.format_exc()}")

def connect_to_postgres_and_load_data(dataframe_dict, conn_id):
    try:
        for table_name, df in dataframe_dict.items():
            # Convert the DataFrame to a list of tuples for bulk insert
            data_tuples = [tuple(row) for row in df.to_numpy()]

            # Use PostgresHook to execute the insert query
            hook = PostgresHook(postgres_conn_id=conn_id)
            hook.insert_rows(table=table_name, rows=data_tuples)

        logging.info('Data successfully inserted into PostgreSQL')

    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        logging.error(f"Timestamp: {datetime.now()}")
        logging.error(f"Traceback: {traceback.format_exc()}")

def main():
    default_args = {
        'owner': 'azeezolowookere@gmail.com',
        'depends_on_past': False,
        'start_date': datetime(2023, 12, 8),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }

    dag = DAG(
        'daily extraction of currency rates',
        default_args=default_args,
        description='DAG to extract daily currency rates and load into PostgreSQL',
        schedule_interval='0 1,23 * * *',
    )

    country_dict = {'Nigeria': 'NGN', 'Ghana': 'GHS', 'Kenya': 'KES', 'Uganda': 'UGX',
                    'Morocco': 'MAD', "Côte d'Ivoire": 'XOF', 'Egypt': 'EGP'}

    api_id = Variable.get("ACCOUNT_ID")
    api_key = Variable.get("API_KEY")
    postgres_conn_id = 'your_postgres_conn_id'  # Specify the Airflow connection ID for PostgreSQL

    # Task 1: Connect to API and Extract Daily Rates
    extract_task = PythonOperator(
        task_id='extract_currency_data',
        python_callable=connect_to_api_and_extract,
        op_kwargs={'api_id': api_id, 'api_key': api_key, 'country_dict': country_dict},
        provide_context=True,
        dag=dag,
    )

    # Task 2: Load Data into PostgreSQL
    load_task = PythonOperator(
        task_id='load_data_into_postgres',
        python_callable=connect_to_postgres_and_load_data,
        op_kwargs={'conn_id': postgres_conn_id},
        provide_context=True,
        dag=dag,
    )

    # Set task dependencies
    extract_task >> load_task

if __name__ == '__main__':
    main()
