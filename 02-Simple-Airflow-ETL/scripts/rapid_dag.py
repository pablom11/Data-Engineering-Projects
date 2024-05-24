from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from rapid_api import run_rapid_football_etl

# Defining dag arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'email': ['your_email@test.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# Defining dag
dag = DAG (
    'rapid_football_dag',
    default_args = default_args,
    description = 'First Airflow DAG',
    schedule_interval = timedelta(days=1),
)

# Defining PythonOperator task to be executed in DAG 
run_etl = PythonOperator(
    task_id='complete_rapid_football_etl',
    python_callable= run_rapid_football_etl,
    dag=dag
)

run_etl