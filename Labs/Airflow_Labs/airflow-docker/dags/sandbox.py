from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def process_data(name, age, **kwargs):
    print(f"Processing data for {name}, age {age}")
    print(f"Execution date: {kwargs['ds']}")
    return f"Processed {name} successfully"

def print_result(ti, **kwargs):
    result = ti.xcom_pull(task_ids='process_task')
    print(f"Result from previous task: {result}")

default_args = {
    'owner': 'dhruv',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='sandbox_demo',
    default_args=default_args,
    description='Sandbox DAG for experimenting',
    schedule_interval='0 2 * * *',
    catchup=False,
    tags=['sandbox', 'demo'],
    params={'user_name': 'Dhruv', 'user_age': 25}
) as dag:

    start_task = BashOperator(
        task_id='start_pipeline',
        bash_command='echo "Starting at $(date)"'
    )
    
    bash_with_params = BashOperator(
        task_id='bash_with_params',
        bash_command='echo "Hello {{ params.user_name }}! Today is {{ ds }}"'
    )
    
    process_task = PythonOperator(
        task_id='process_task',
        python_callable=process_data,
        op_kwargs={'name': '{{ params.user_name }}', 'age': '{{ params.user_age }}'}
    )
    
    print_task = PythonOperator(
        task_id='print_result',
        python_callable=print_result
    )
    
    final_task = BashOperator(
        task_id='completion',
        bash_command='echo "Completed at $(date)"'
    )
    
    start_task >> bash_with_params >> process_task >> print_task >> final_task