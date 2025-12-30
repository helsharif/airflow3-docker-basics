
# 🚀 Apache Airflow Data Quality Pipeline (Dockerized)
**Airflow 3.1.5 | Docker Compose | Task Orchestration | Data Validation | Data Engineering**

This project demonstrates a **production-style data quality pipeline** built using **Apache Airflow 3.1.5** running inside a fully containerized **Docker** environment. It continuously generates synthetic (AirBnB style) booking data, validates it for quality issues, and stores structured anomaly reports—showcasing modern orchestration, scheduling, and pipeline reliability techniques.

This work was completed while advancing my Data Engineering skillset and serves as a portfolio demonstration of:
- Designing orchestrated data pipelines with Airflow
- Implementing automated quality checks
- Running Airflow in a local reproducible Docker environment
- Managing schedules, context handling, logging, and reproducibility
- Working with modern Airflow SDK patterns

---

## 🎯 What This Pipeline Does
✔️ Spins up **Airflow via Docker Compose**  
✔️ Runs a scheduled DAG **every minute**  
✔️ Generates synthetic bookings data  
✔️ Performs automated data validation checks  
✔️ Detects missing + invalid fields  
✔️ Outputs structured anomaly reports  
✔️ Stores generated + validated data in mounted host volumes  

---

## 🧠 Key Engineering Concepts Demonstrated
- Airflow DAG design using the **new Airflow 3 SDK (`airflow.sdk`)**
- Working with **tasks, dependencies, and scheduling**
- Writing/reading files across containers using mounted Docker volumes
- Clean, maintainable Python task functions
- Reusable helper utilities for path and execution context handling

---

## 🧰 Tech Stack
- **Apache Airflow 3.1.5**
- **Docker + Docker Compose**
- Python
- JSON data storage

---

## 📂 Project Structure
```
├── airflow-docker/
    ├── dags/
    │   └── data_validation_dag_airflow3.py
    ├── tmp/
    │   ├── bookings/
    │   └── anomalies/
    ├── logs/
    ├── config/
    ├── docker-compose.yaml
    └── README.md
```

---

## 🔎 Data Quality Logic
Each generated booking record is validated for:
- Missing `booking_id`
- Missing `listing_id`
- Missing `user_id`
- Missing `booking_time`
- Missing `status`
- Invalid `status` values  
  (must be: `confirmed`, `pending`, or `cancelled`)

Any violations are written to structured JSON anomaly files, including:
- record index
- list of validation failures

---

## ▶️ Running the Project

### 1️⃣ Clone the Repository
```
git clone <repo-url>
cd <repo>
```

### 2️⃣ Start Airflow
Navigate to the 'airflow-docker' folder in command line and run:
```
docker compose up airflow-init
docker compose up -d
```

### 3️⃣ Open Airflow UI
In a web-browser Navigate to:
```
http://localhost:8080
```
Default credentials:
```
user: airflow
pass: airflow
```

### 4️⃣ Enable the DAG
Turn on:
```
data_quality_pipeline
```

---

## 📁 Where the Data Lives
Synthetic data and anomaly outputs are written to **host-mounted volumes**, meaning you can inspect results directly from your machine.

```
tmp/bookings/<timestamp>/bookings.json
tmp/anomalies/<timestamp>/anomalies.json
```

This mapping is configured via Docker volumes and ensures reproducibility across environments.

---

## 🧪 Validation Output Example
```json
[
  {
    "booking_id": 2,
    "anomalies": [
      "Missing user_id",
      "Invalid status: 'error'"
    ]
  }
]
```

---

## 🧠 Learning Outcomes
Through this build, I strengthened practical experience in:
- Building reliable Airflow pipelines
- Understanding Airflow basics (DAGs, tasks, schedulers, executors)
- Dockerized infrastructure for data engineering
- Implementing automated data quality enforcement
- Designing pipelines aligned with real-world engineering workflows

---

## 🤝 Let’s Connect
If you’d like to discuss:
Data Engineering • Airflow • ML Pipelines • Analytics Engineering • Cloud Data Systems  
Feel free to reach out!
