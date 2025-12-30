# Husayn El Sharif
# see: https://academy.zerotomastery.io/courses/data-engineering-bootcamp/lectures/61065656
# edited to be compatible with Airflow 3.1.5

# imports
from airflow.sdk import dag, task, get_current_context
from datetime import datetime
#import pendulum
import os
import json
import random
from pathlib import Path


# TODO: Use the @dag decorator to create a DAG that:
# * Runs every minute
# * Does not use catchup

TMP_PATH = Path("/opt/airflow/tmp")


@dag(
    dag_id="data_quality_pipeline", # unique identifier for the DAG
    schedule='* * * * *', # This runs every minute
    catchup=False, # This prevents historical runs from being created
    description="Data Quality Check DAG", # description of the DAG
    start_date=datetime(2025, 1, 1), # start date of the DAG
    tags=["data quality", "validation"],
)
def data_quality_pipeline():

    CORRECT_PROB = 0.7

    def get_bookings_path(context):
        # Airflow 3: use logical_date instead of execution_date
        logical_date = context["logical_date"]
        file_date = logical_date.strftime("%Y-%m-%d_%H-%M")
        #return f"/tmp/data/bookings/{file_date}/bookings.json" 
        return str(TMP_PATH / "bookings" / file_date / "bookings.json") # updated path for bookings
    
    def get_anomalies_path(context):
        # Airflow 3: use logical_date instead of execution_date
        logical_date = context["logical_date"]
        file_date = logical_date.strftime("%Y-%m-%d_%H-%M")
        #return f"/tmp/data/anomalies/{file_date}/anomalies.json" # path for anomalies
        return str(TMP_PATH / "anomalies" / file_date / "anomalies.json") # path for anomalies

    def generate_booking_id(i):
        if random.random() < CORRECT_PROB:
            return i + 1

        return ""

    def generate_listing_id():
        if random.random() < CORRECT_PROB:
            return random.choice([1, 2, 3, 4, 5])

        return ""

    def generate_user_id(correct_prob=0.7):
        return random.randint(1000, 5000) if random.random() < correct_prob else ""

    def generate_booking_time(logical_date):
        if random.random() < CORRECT_PROB:
            return logical_date.strftime('%Y-%m-%d %H:%M:%S')

        return ""

    def generate_status():
        if random.random() < CORRECT_PROB:
            return random.choice(["confirmed", "pending", "cancelled"])

        return random.choice(["unknown", "", "error"])

    @task # Task to generate bookings data
    def generate_bookings():
        context = get_current_context()
        booking_path = get_bookings_path(context)

        num_bookings = random.randint(5, 15)
        bookings = []

        for i in range(num_bookings):
            booking = {
                "booking_id": generate_booking_id(i),
                "listing_id": generate_listing_id(),
                "user_id": generate_user_id(),
                "booking_time": generate_booking_time(context["logical_date"]),
                "status": generate_status()
            }
            bookings.append(booking)

        directory = os.path.dirname(booking_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(booking_path, "w") as f:
            json.dump(bookings, f, indent=4)

        print(f"Written to file: {booking_path}")

    @task # Task to perform data quality check
    def quality_check():
        context = get_current_context()
        booking_path = get_bookings_path(context)

        anomalies = []
        valid_statuses = {"confirmed", "pending", "cancelled"}

        with open(booking_path, "r") as f:
            bookings = json.load(f)

        for index, row in enumerate(bookings):
            row_anomalies = []
            if not row["booking_id"]:
                row_anomalies.append("Missing booking_id")
            if not row["listing_id"]:
                row_anomalies.append("Missing listing_id")
            if not row["user_id"]:
                row_anomalies.append("Missing user_id")
            if not row["booking_time"]:
                row_anomalies.append("Missing booking_time")
            if not row["status"]:
                row_anomalies.append("Missing status")


            if row["status"] and row["status"] not in valid_statuses:
                row_anomalies.append(f"Invalid status: {row['status']}")

            if row_anomalies:
                anomalies.append({
                    "booking_id": index,
                    "anomalies": row_anomalies,
                })

        anomalies_file = get_anomalies_path(context)
        directory = os.path.dirname(anomalies_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(anomalies_file, "w") as f:
            json.dump(anomalies, f, indent=4)

        print(f"Completed validation for {booking_path}. Anomalies found: {len(anomalies)}")
        print(f"Result written to {anomalies_file}")

    # Define task dependencies
    generate_bookings() >> quality_check() # Define dependencies between tasks: generate_bookings must run before quality_check

# Create an instance of the DAG (Airflow 3 will also detect it from the decorator call)
dag_instance = data_quality_pipeline() 

    # TODO: Create a data quality check task that reads bookings data and validates every record.
    # For every invalid record it should return a validation record that includes:
    # * A record position in an input file
    # * A list of identified violations
    #
    # Here is a list of validations it should perform:
    # * Check if each of the fields is missing
    # * Check if the "status" field has one of the valid values
    #
    # It should write all found anomalies into an input file.

    # TODO: Define dependencies between tasks

# TODO: Create an instance of the DAG
