from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import configuration as conf

# Import your ML functions
import sys
sys.path.insert(0, '/opt/airflow')
from src.lab import load_data, data_preprocessing, build_save_model, load_model_elbow

# Enable pickle support for XCom
conf.set('core', 'enable_xcom_pickling', 'True')

# Define default arguments
default_args = {
    'owner': 'dhruv',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# Create the DAG
dag = DAG(
    'ml_clustering_pipeline',
    default_args=default_args,
    description='K-Means Clustering Pipeline with Elbow Method',
    schedule_interval=None,  # Manual trigger
    catchup=False,
    tags=['ml', 'clustering', 'kmeans'],
)

# Task 1: Load data
load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

# Task 2: Preprocess data
preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],
    dag=dag,
)

# Task 3: Build and save model
build_model_task = PythonOperator(
    task_id='build_and_save_model',
    python_callable=build_save_model,
    op_args=[preprocess_task.output, 'clustering_model.pkl'],
    dag=dag,
)

# Task 4: Load model and find optimal clusters
find_optimal_task = PythonOperator(
    task_id='find_optimal_clusters',
    python_callable=load_model_elbow,
    op_args=['clustering_model.pkl', build_model_task.output],
    dag=dag,
)

# Set task dependencies
load_data_task >> preprocess_task >> build_model_task >> find_optimal_task