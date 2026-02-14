from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import DagRun
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect
import threading

# Default arguments
default_args = {
    'owner': 'dhruv',
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
}

def check_dag_status(**kwargs):
    """Check the status of the last Airflow_Lab2 DAG run"""
    from airflow.models import DagRun
    from airflow.utils.session import provide_session
    
    @provide_session
    def get_last_dag_run(session=None):
        last_run = session.query(DagRun).filter(
            DagRun.dag_id == 'Airflow_Lab2'
        ).order_by(DagRun.execution_date.desc()).first()
        
        if last_run:
            return last_run.state == 'success'
        return False
    
    return get_last_dag_run()

# Create Flask app
app = Flask(__name__, template_folder='/opt/airflow/templates')

@app.route('/api')
def api():
    """API endpoint to check DAG status"""
    status = check_dag_status()
    if status:
        return redirect('/success')
    else:
        return redirect('/failure')

@app.route('/success')
def success():
    """Success page"""
    return render_template('success.html')

@app.route('/failure')
def failure():
    """Failure page"""
    return render_template('failure.html')

def start_flask_app(**kwargs):
    """Start the Flask server"""
    print("Starting Flask server on port 5002...")
    print("Access the API at: http://localhost:2/api")
    
    # Run Flask in a separate thread
    def run_app():
        app.run(host='0.0.0.0', port=5002, debug=False)
    
    flask_thread = threading.Thread(target=run_app)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Flask server started successfully!")
    print("Visit http://localhost:5002/api to check pipeline status")
    
    # Keep the task running for 5 minutes
    import time
    time.sleep(300)

# Create DAG
dag = DAG(
    'Airflow_Lab2_Flask',
    default_args=default_args,
    description='Flask API for checking DAG status',
    schedule_interval=None,
    catchup=False,
    tags=['lab2', 'flask', 'api'],
)

# Start Flask API
start_flask_task = PythonOperator(
    task_id='start_flask_api',
    python_callable=start_flask_app,
    dag=dag,
)
