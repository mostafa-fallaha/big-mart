import textwrap
from datetime import datetime, timedelta
from scripts import etl, train_model
from airflow.models.dag import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG(
    "pipeline",
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(seconds=30),
    },
    description="pipeline for cleaning, versioning data and training a model",
    schedule=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["test 1"],
) as dag:

    etl = PythonOperator(
        task_id='etl',
        python_callable=etl.cleaning
    )

    train_model = PythonOperator(
        task_id = 'train_model',
        python_callable=train_model.train_model
    )

    shell_script = BashOperator(
        task_id="shell_script",
        bash_command="{{ '/home/mostafa/Desktop/FSD\ Projects/big_mart/dvc_commands.sh' }}",
        do_xcom_push=False
    )

    etl >> shell_script >> train_model