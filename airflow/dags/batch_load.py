"""
Airflow DAG to ingest batch data for AntMart Analytics.

This DAG executes once per day and is responsible for loading synthetic or real
batch data into the staging area. It then triggers dbt to run transformations.

To start this DAG, run the Airflow webserver and scheduler (see docker-compose.yml)
and enable the DAG from the UI.

Note: The actual logic to load data and run dbt is delegated to functions in
scripts/generate_synthetic.py and dbt commands. You can customize these calls
according to your environment and data sources.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess
import os


def generate_batch_data(**context):
    """Generate synthetic batch data by invoking the generator script."""
    script_path = os.path.join(os.getcwd(), 'scripts', 'generate_synthetic.py')
    subprocess.check_call(['python', script_path])


def run_dbt_models(**context):
    """Run dbt models and tests using the project directory."""
    dbt_dir = os.path.join(os.getcwd(), 'dbt')
    profiles_dir = dbt_dir
    subprocess.check_call(['dbt', 'deps', '--project-dir', dbt_dir])
    subprocess.check_call(['dbt', 'run', '--project-dir', dbt_dir, '--profiles-dir', profiles_dir])
    subprocess.check_call(['dbt', 'test', '--project-dir', dbt_dir, '--profiles-dir', profiles_dir])


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    dag_id='antmart_batch_load',
    description='Daily batch ingestion and transformation for AntMart Analytics',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=['antmart', 'batch'],
) as dag:

    generate_data = PythonOperator(
        task_id='generate_batch_data',
        python_callable=generate_batch_data,
    )

    run_dbt = PythonOperator(
        task_id='run_dbt_models',
        python_callable=run_dbt_models,
    )

    generate_data >> run_dbt
