
# 🚀 End-to-End Data Engineering with Docker, Apache Airflow & Spark

**Apache Airflow 3.1.5 | Docker Compose | Spark | Scheduling | ETL Orchestration | Data Quality | Portfolio Project**  

This repository demonstrates **modern, production-style data engineering pipelines** orchestrated using **Apache Airflow running in Docker**, with an advanced extension that integrates **Apache Spark processing** for scalable data transformation.

It showcases my ability to:
- Design and orchestrate automated data pipelines
- Run Airflow fully containerized for portability and reproducibility
- Generate and validate streaming‑style synthetic booking data
- Execute distributed data processing with Spark
- Manage real‑world engineering concerns like scheduling, dependencies, data storage, and logging
- Work confidently with the **new Airflow 3 SDK**

This project is intentionally structured to simulate real engineering workflows and demonstrates skills relevant to **Data Engineering, Analytics Engineering, and Machine Learning Engineering roles**.

---

## 📌 Two Major Implementations in This Repo

### 1️⃣ Airflow + Docker → Data Quality Pipeline
Located in:
```
airflow-docker/
```

This pipeline:
- Spins up Airflow in Docker
- Generates AirBnB‑style synthetic booking data
- Performs automated data validation
- Writes structured anomaly reports
- Demonstrates scheduling, logging, reliability, and reproducibility

#### 🧠 Key Concepts Demonstrated
- Airflow 3 (`airflow.sdk`) DAG development
- Task dependency design
- Mounted Docker volume data management
- Automated validation logic
- Realistic pipeline structure & engineering discipline

---

### 2️⃣ Airflow + Docker + Spark → ETL & Aggregation Pipeline
Located in:
```
airflow-docker-spark/
```

This is the newest addition to the project and represents a **step into scalable distributed data processing**.

This pipeline:
- Runs fully in Docker
- Uses Airflow to orchestrate Spark jobs
- Generates hourly booking data via Airflow (based on AirBnB data from Broward County, Florida USA see: https://insideairbnb.com/broward-county/ )
- Joins it with AirBnB listings data inside Spark
- Computes **bookings per listing + summary metrics**
- Writes output as structured results

#### 🧠 Key Concepts Demonstrated
- SparkSubmitOperator
- Local Spark cluster execution
- CLI argument handling between Airflow → Spark
- Data joins, aggregation, and output writing
- End‑to‑end orchestration: generate → process → output


---

## 🧰 Tech Stack
- Apache Airflow 3.1.5 (Latest stable release as of December 12, 2025)
- Docker & Docker Compose
- Apache Spark 4.1 (Latest stable release as of December 16, 2025)
- Python (version 3.12)
- JSON / CSV data outputs

---

## 📂 Repository Structure
```
├── airflow-docker/
│   └── Airflow + Docker Data Quality Implementation
│
├── airflow-docker-spark/
│   └── Airflow + Spark ETL Implementation
│
├── Notes on Airflow and Docker.docx
├── Notes on Airflow-Docker-Spark.docx
├── README.md
```

---

## ▶️ How to Run
Each implementation folder contains its own instructions and compose setup.  
Simply navigate into the desired project and follow the provided steps.

---

## 💡 Why This Project Matters
This project reflects:
- Experience with real (and modern version) orchestration tools (Airflow)
- Comfort designing reliable pipelines
- Ability to integrate multiple systems
- Hands‑on Spark processing (and troubleshooting!)

This aligns strongly with roles involving:
- Data Engineering
- Analytics / Platform Engineering
- ML Pipelines & MLOps
- Cloud & ETL Engineering

---

## 🧠 Learning Outcomes
Through this work I strengthened capabilities in:
- Workflow orchestration & design
- Distributed compute pipeline execution
- Dockerized engineering environments
- Airflow DAG design using modern SDKs
- Writing scalable & maintainable data pipelines

---

## 🤝 Let’s Connect
If you'd like to discuss:
Data Engineering • Spark • Airflow • ETL Pipelines • Cloud Data Systems

---

⭐ If you found this interesting, feel free to ⭐ the repo!
