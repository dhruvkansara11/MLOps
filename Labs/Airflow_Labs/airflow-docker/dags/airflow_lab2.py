from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta
from airflow import configuration as conf
import sys

# Add src to path
sys.path.insert(0, '/opt/airflow')
sys.path.insert(0, '/opt/airflow/src')

# Import from src.lab
from src.lab import load_data, data_preprocessing, build_save_model, load_model_elbow

# Enable XCom pickling
conf.set('core', 'enable_xcom_pickling', 'True')

# Email notification functions
def notify_success(context):
    """Send email on task success"""
    success_email = EmailOperator(
        task_id='success_email',
        to='suitelifeofshiv24@gmail.com',  # CHANGE THIS
        subject='airflow: {{ task_instance.task_id }}',
        html_content='''
        <h3>Task Succeeded!</h3>
        <p><strong>Task:</strong> {{ task_instance.task_id }}</p>
        <p><strong>DAG:</strong> {{ task_instance.dag_id }}</p>
        <p><strong>Execution Time:</strong> {{ execution_date }}</p>
        <p>The task completed successfully.</p>
        '''
    )
    return success_email.execute(context=context)

def notify_failure(context):
    """Send email on task failure"""
    failure_email = EmailOperator(
        task_id='failure_email',
        to='suitelifeofshiv24@gmail.com',  # CHANGE THIS
        subject='Airflow Alert: Task Failed - {{ task_instance.task_id }}',
        html_content='''
        <h3>Task Failed!</h3>
        <p><strong>Task:</strong> {{ task_instance.task_id }}</p>
        <p><strong>DAG:</strong> {{ task_instance.dag_id }}</p>
        <p><strong>Execution Time:</strong> {{ execution_date }}</p>
        <p><strong>Error:</strong> {{ exception }}</p>
        <p>Please check the logs for more details.</p>
        '''
    )
    return failure_email.execute(context=context)

# Default arguments
default_args = {
    'owner': 'dhruv',
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'Airflow_Lab2',
    default_args=default_args,
    description='ML Pipeline with Email Notifications',
    schedule_interval=None,
    catchup=False,
    tags=['lab2', 'ml', 'email'],
)

# Owner task
owner_task = BashOperator(
    task_id='owner_task',
    bash_command='echo "Owner: Dhruv Kansara"',
    dag=dag,
)

# Send start email
send_start_email = EmailOperator(
    task_id='send_start_email',
    to='suitelifeofshiv24@gmail.com',  # CHANGE THIS
    subject='Airflow Lab2: Pipeline Started',
    html_content='''
    <h2>ML Pipeline Started</h2>
    <p>The Airflow Lab2 ML pipeline has started execution.</p>
    <p><strong>DAG:</strong> {{ dag.dag_id }}</p>
    <p><strong>Execution Date:</strong> {{ execution_date }}</p>
    ''',
    dag=dag,
)

# ML Pipeline Tasks
load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    on_success_callback=notify_success,
    on_failure_callback=notify_failure,
    dag=dag,
)

preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],
    on_success_callback=notify_success,
    on_failure_callback=notify_failure,
    dag=dag,
)

build_model_task = PythonOperator(
    task_id='build_and_save_model',
    python_callable=build_save_model,
    op_args=[preprocess_task.output, 'model_lab2.pkl'],
    on_success_callback=notify_success,
    on_failure_callback=notify_failure,
    dag=dag,
)

load_model_task = PythonOperator(
    task_id='load_model',
    python_callable=load_model_elbow,
    op_args=['model_lab2.pkl', build_model_task.output],
    on_success_callback=notify_success,
    on_failure_callback=notify_failure,
    dag=dag,
)

# Send completion email
send_completion_email = EmailOperator(
    task_id='send_completion_email',
    to='suitelifeofshiv24@gmail.com',  # CHANGE THIS
    subject='Airflow Lab2: Pipeline Completed Successfully ✅',
    html_content='''
    <h2>ML Pipeline Completed!</h2>
    <p>The Airflow Lab2 ML pipeline has completed successfully.</p>
    <p><strong>DAG:</strong> {{ dag.dag_id }}</p>
    <p><strong>Execution Date:</strong> {{ execution_date }}</p>
    <p><strong>All tasks passed!</strong></p>
    ''',
    dag=dag,
)

# Trigger Flask DAG
trigger_flask = TriggerDagRunOperator(
    task_id='trigger_flask_dag',
    trigger_dag_id='Airflow_Lab2_Flask',
    dag=dag,
)

# Set dependencies
owner_task >> send_start_email >> load_data_task >> preprocess_task >> build_model_task >> load_model_task >> send_completion_email >> trigger_flask