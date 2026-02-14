from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Default arguments for the DAG
default_args = {
    'owner': 'dhruv',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

# Define a Python function
def greet():
    print("Hello from Airflow!")
    print("This is my first DAG")
    return "Success!"

def print_date():
    print(f"Current date and time: {datetime.now()}")

# Create the DAG
with DAG(
    dag_id='my_first_dag',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['tutorial', 'beginner'],
) as dag:
    
    # Task 1: Run a bash command
    task1 = BashOperator(
        task_id='print_hello',
        bash_command='echo "Starting the pipeline..."'
    )
    
    # Task 2: Run a Python function
    task2 = PythonOperator(
        task_id='greet_task',
        python_callable=greet
    )
    
    # Task 3: Another Python function
    task3 = PythonOperator(
        task_id='print_date_task',
        python_callable=print_date
    )
    
    # Task 4: Final bash command
    task4 = BashOperator(
        task_id='print_goodbye',
        bash_command='echo "Pipeline completed successfully!"'
    )
    
    # Set task dependencies
    task1 >> task2 >> task3 >> task4