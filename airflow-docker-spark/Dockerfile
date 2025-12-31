# Start from official Airflow 3.1.5 image
FROM apache/airflow:3.1.5

# --------------------------
# 1) Install Java 17 (fully supported by Spark 4.1)
# --------------------------
USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
           openjdk-17-jre-headless \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME for Java 17
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# --------------------------
# 2) Back to airflow user + install Spark provider + PySpark 4.1
# --------------------------
USER airflow

RUN pip install --no-cache-dir \
      "apache-airflow==${AIRFLOW_VERSION}" \
      apache-airflow-providers-apache-spark \
      "pyspark==4.1.0"
