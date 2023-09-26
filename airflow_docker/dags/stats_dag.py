from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pandas as pd
import json


def transform_load_data(task_instance):
    data = task_instance.xcom_pull(task_ids="extract_nhl_stats")

    transformed_data = tuple(data)
    transformed_data_list = [transformed_data]
    df_data = pd.DataFrame(transformed_data_list)

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = 'current_weather_data_portland_' + dt_string
    print(data)
    df_data.to_csv(f"./nhl_stats.csv", index=False)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 30),
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}


with DAG('nhl_stats',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    is_nhl_stats_api_ready = HttpSensor(
        task_id='is_nhl_stats_api_ready',
        http_conn_id='nhl_api',
        endpoint='/api/v1/standings?season=20212022&expand=standings.record'
    )

    extract_nhl_stats = SimpleHttpOperator(
        task_id='extract_nhl_stats',
        http_conn_id='nhl_api',
        endpoint='/api/v1/standings?season=20212022&expand=standings.record',
        method='GET',
        response_filter=lambda x: json.loads(x.text),
        log_response=True
    )

    transform_load_nhl_data = PythonOperator(
        task_id='transform_load_nhl_data',
        python_callable=transform_load_data
    )

    is_nhl_stats_api_ready >> extract_nhl_stats >> transform_load_nhl_data
