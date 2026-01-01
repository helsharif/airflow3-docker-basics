# Husayn El Sharif
# revised DAG for Airflow 3

from datetime import datetime
import os
import csv
import random
from pathlib import Path
import json

from airflow.sdk import dag, task, get_current_context
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from airflow.providers.standard.sensors.filesystem import FileSensor # to incorporate file sensor

TMP_PATH = "/opt/airflow/tmp"  # plain string makes life easier

@dag(
    dag_id="bookings_spark_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="* * * * *",  # schedule_interval is removed in Airflow 3.x
    catchup=False,
    description="Generate synthetic bookings and process them with Spark",
)
def bookings_spark_pipeline():

    @task
    def generate_bookings():
        # In Airflow 3.x, execution_date is removed from context.
        # Use dag_run.logical_date instead. 
        context = get_current_context()
        logical_date = context["dag_run"].logical_date

        file_date = logical_date.strftime("%Y-%m-%d_%H%M")
        file_path = f"{TMP_PATH}/data/bookings/{file_date}/bookings.csv"

        num_bookings = random.randint(30, 50)
        bookings = []
        for _ in range(num_bookings):
            booking = {
                "booking_id": random.randint(1000, 5000),
                "listing_id": random.choice(
                    [69824, 191160, 1309185, 1559232, 2028061, 4494878, 24279533, 52537443]
                ), # select from listings csv
                "user_id": random.randint(1000, 5000),
                "booking_time": logical_date.strftime("%Y-%m-%d %H:%M:%S"),
                "status": random.choice(["confirmed", "cancelled", "pending"]),
            }
            bookings.append(booking)

        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)

        fieldnames = ["booking_id", "listing_id", "user_id", "booking_time", "status"]

        with open(file_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for booking in bookings:
                writer.writerow(booking)

        print(f"Generated bookings data written to {file_path}")
        return file_path  # optional, but handy for debugging / future use
    
    wait_for_listings_file = FileSensor(
        task_id="wait_for_listings_file",
        fs_conn_id="local_fs",  # connection to local filesystem
        filepath=f"{TMP_PATH}/airbnb_data/listings.csv.gz",
        poke_interval=30,  # check every 30 seconds
        timeout=600,  # timeout after 10 minutes if file not found
    )

    spark_job = SparkSubmitOperator(
        task_id="process_listings_and_bookings",
        application="/opt/airflow/dags/bookings_per_listing_spark.py", # <— absolute path to spark script inside container
        name="listings_bookings_join",
        application_args=[
            # Use logical_date in templates instead of execution_date.
            "--listings_file",
            TMP_PATH + "/airbnb_data/listings.csv.gz",  # static initial file
            "--bookings_file",
            TMP_PATH +"/data/bookings/{{ logical_date.strftime('%Y-%m-%d_%H%M') }}/bookings.csv", # plain string + Jinja (NO f-string!)
            "--output_path",
            TMP_PATH + "/data/bookings_per_listing/{{ logical_date.strftime('%Y-%m-%d_%H%M') }}", # plain string + Jinja (NO f-string!)
        ],
        conn_id="spark_booking",
    )

    bookings_file = generate_bookings()
    bookings_file >> spark_job
    wait_for_listings_file >> spark_job


dag_instance = bookings_spark_pipeline()
