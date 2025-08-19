"""
Airflow DAG to ingest micro-batch event data for AntMart Analytics.

This DAG runs on a short schedule (e.g., every 5 minutes) to poll the events
directory for new JSONL files and ingest them into the staging table. It then
runs incremental dbt models to update the event fact tables.

Customize the schedule_interval as desired. The logic here is a placeholder
that calls a Python script to simulate event ingestion. Feel free to extend
with your own ingestion logic.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess
import os


def ingest_events(**context):
    """Simulate event ingestion by running the event producer script."""
    script_path = os.path.join(os.getcwd(), 'scripts', 'event_producer.py')
    # Produce a small batch of events (e.g., 100 rows)
    subprocess.check_call(['python', script_path, '--count', '100'])


def run_dbt_incremental(**context):
    """Run dbt incremental models for events."""
    dbt_dir = os.path.join(os.getcwd(), 'dbt')
    profiles_dir = dbt_dir
    subprocess.check_call(['dbt', 'run', '--project-dir', dbt_dir, '--profiles-dir', profiles_dir, '--select', 'fct_events'])
    subprocess.check_call(['dbt', 'test', '--project-dir', dbt_dir, '--profiles-dir', profiles_dir, '--select', 'fct_events'])


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


with DAG(
    dag_id='antmart_events_microbatch',
    description='Micro-batch ingestion and incremental updates for AntMart Analytics',
    schedule_interval='*/5 * * * *',  # every 5 minutes
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=['antmart', 'events'],
) as dag:

    produce_events = PythonOperator(
        task_id='produce_events',
        python_callable=ingest_events,
    )

    run_incremental = PythonOperator(
        task_id='run_dbt_incremental',
        python_callable=run_dbt_incremental,
    )

    produce_events >> run_incremental
