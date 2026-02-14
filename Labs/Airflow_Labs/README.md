# Airflow Labs 1 & 2 - README

**Student:** Dhruv Kansara | **Course:** MLOps | **Institution:** Northeastern University | **Date:** February 2026

---

## Overview

Apache Airflow workflow orchestration labs using Docker on macOS.

**Lab 1:** Airflow basics, ML clustering pipeline with K-Means  
**Lab 2:** Email notifications, Flask API integration

**Tech:** Airflow 2.8.1, Docker, Python 3.8, PostgreSQL, Redis, Flask

---

## Lab 1: DAGs

### 1. `ml_clustering_pipeline`
```
load_data → preprocess_data → build_and_save_model → find_optimal_clusters
```
K-Means clustering on iris dataset, saves model to `working_data/clustering_model.pkl`

### 2. `sandbox_demo`
```
start → bash_with_params → greet_user → [process_task, multi_commands] → print_result → completion
```
Demonstrates Jinja templating, parallel tasks, XCom data passing

### 3. `my_first_dag`
```
print_hello → greet_task → print_date_task → print_goodbye
```
Basic introductory DAG

---

## Lab 2: DAGs

### 1. `Airflow_Lab2`
```
owner_task → send_start_email → load_data → preprocess_data → build_and_save_model → load_model → send_completion_email → trigger_flask_dag
```
ML pipeline with Gmail SMTP notifications, HTML emails, task callbacks

### 2. `Airflow_Lab2_Flask`
Flask API for DAG monitoring at `http://localhost:5001/api` or `5002`  
Routes: `/api`, `/success`, `/failure`

---

## Project Structure
```
airflow-docker/
├── dags/
│   ├── my_first_dag.py
│   ├── ml_pipeline.py
│   ├── sandbox.py
│   ├── airflow_lab2.py
│   └── airflow_lab2_flask.py
├── src/
│   ├── __init__.py
│   └── lab.py
├── data/
│   └── iris.csv
├── working_data/
│   ├── clustering_model.pkl
│   └── model_lab2.pkl
├── templates/
│   ├── success.html
│   └── failure.html
├── docker-compose.yaml
└── .env
```

---

## Installation
```bash
# 1. Create directory
mkdir -p ~/Documents/NEU/Sem3/MLOPs/MLOps/Labs/Airflow_Labs/airflow-docker
cd ~/Documents/NEU/Sem3/MLOPs/MLOps/Labs/Airflow_Labs/airflow-docker

# 2. Download docker-compose
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.1/docker-compose.yaml'

# 3. Create directories
mkdir -p dags logs plugins config working_data src data templates
touch src/__init__.py
echo -e "AIRFLOW_UID=$(id -u)" > .env

# 4. Edit docker-compose.yaml - Add these:
# AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
# _PIP_ADDITIONAL_REQUIREMENTS: pandas scikit-learn kneed flask
# AIRFLOW__SMTP__* (Gmail settings)
# volumes: working_data, src, data, templates
# ports: 8080:8080, 5001:5001
# _AIRFLOW_WWW_USER_USERNAME: airflow2
# _AIRFLOW_WWW_USER_PASSWORD: airflow2

# 5. Initialize
docker-compose up airflow-init

# 6. Start
docker-compose up

# 7. Access UI
# http://localhost:8080
# Login: airflow2 / airflow2
```

---

## docker-compose.yaml Changes
```yaml
environment:
  AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
  _PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:- pandas scikit-learn kneed flask}
  AIRFLOW__SMTP__SMTP_HOST: smtp.gmail.com
  AIRFLOW__SMTP__SMTP_STARTTLS: 'True'
  AIRFLOW__SMTP__SMTP_SSL: 'False'
  AIRFLOW__SMTP__SMTP_USER: your-email@gmail.com
  AIRFLOW__SMTP__SMTP_PASSWORD: your-app-password
  AIRFLOW__SMTP__SMTP_PORT: 587
  AIRFLOW__SMTP__SMTP_MAIL_FROM: your-email@gmail.com

volumes:
  - ${AIRFLOW_PROJ_DIR:-.}/working_data:/opt/airflow/working_data
  - ${AIRFLOW_PROJ_DIR:-.}/src:/opt/airflow/src
  - ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data
  - ${AIRFLOW_PROJ_DIR:-.}/templates:/opt/airflow/templates

# In airflow-webserver:
ports:
  - "8080:8080"
  - "5001:5001"

# In airflow-init:
_AIRFLOW_WWW_USER_USERNAME: airflow2
_AIRFLOW_WWW_USER_PASSWORD: airflow2
```

---

## How to Run

### Lab 1
```bash
# Via UI: http://localhost:8080 → Toggle ON → Play button

# Via CLI:
docker exec -it airflow-docker-airflow-scheduler-1 airflow dags trigger ml_clustering_pipeline
```

### Lab 2
```bash
# Prerequisites:
# 1. Get Gmail app password: https://myaccount.google.com/apppasswords
# 2. Update email in airflow_lab2.py (5 places)
# 3. Update SMTP in docker-compose.yaml
# 4. Restart: docker-compose down && docker-compose up

# Then trigger Airflow_Lab2 via UI
# Flask API auto-starts at http://localhost:5001/api
```

---

## Validation

### Lab 1
- [ ] 3 DAGs visible in UI
- [ ] ml_clustering_pipeline runs (all green)
- [ ] Model saved: working_data/clustering_model.pkl
- [ ] Logs show optimal K (usually 3)

### Lab 2
- [ ] Emails received (start, 4x success, completion)
- [ ] Airflow_Lab2_Flask auto-triggers
- [ ] Flask UI accessible at localhost:5001/api
- [ ] Success page displays
- [ ] Model saved: working_data/model_lab2.pkl

---

## Troubleshooting

**Port 5001 in use:**
```bash
lsof -i :5001
kill -9 <PID>
# Or change docker-compose.yaml to 5002:5001
```

**Import errors:**
```bash
touch src/__init__.py
docker-compose restart
```

**Email not working:**
- Use Gmail app password, not regular password
- Enable 2-Step Verification
- Restart after SMTP changes

**DAG not showing:**
```bash
python dags/your_dag.py  # Check syntax
docker-compose logs airflow-scheduler | grep ERROR
```

---

## Commands Reference
```bash
# Start
docker-compose up

# Stop
docker-compose down

# Clean slate
docker-compose down -v

# View logs
docker-compose logs -f airflow-scheduler

# Trigger DAG
docker exec -it airflow-docker-airflow-scheduler-1 airflow dags trigger <dag_id>
```

---

## Key Files

### src/lab.py
```python
def load_data(**kwargs):
    # Loads iris.csv, returns pickled DataFrame

def data_preprocessing(serialized_data, **kwargs):
    # Scales features, returns pickled array

def build_save_model(serialized_data, filename, **kwargs):
    # Trains K-Means k=1-10, saves model, returns SSE

def load_model_elbow(filename, serialized_sse, **kwargs):
    # Finds optimal K using elbow method
```

### data/iris.csv
```csv
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
...
```

---

## Key Learnings

**Lab 1:**
- DAG: Workflow definition with task dependencies
- Operators: BashOperator, PythonOperator
- XCom: Inter-task data passing
- Scheduling: Cron expressions
- Templating: Jinja variables

**Lab 2:**
- Email: SMTP, EmailOperator, callbacks
- DAG Triggering: TriggerDagRunOperator
- Flask: REST API within Airflow
- Metadata: Airflow database queries

---

## Results

**Execution Times:**
- ml_clustering_pipeline: ~30s
- sandbox_demo: ~15s
- Airflow_Lab2: ~45s
- Airflow_Lab2_Flask: 10min

**Storage:** ~2.2GB total (Docker images + logs)

---



