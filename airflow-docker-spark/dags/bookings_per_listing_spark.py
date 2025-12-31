from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Join listings and bookings, compute bookings per listing"
    )
    parser.add_argument(
        "--listings_file",
        required=True,
        help="Path to the monthly listings file (CSV or CSV.GZ)",
    )
    parser.add_argument(
        "--bookings_file",
        required=True,
        help="Path to the hourly bookings file (CSV)",
    )
    parser.add_argument(
        "--output_path",
        required=True,
        help="Output directory for the aggregated results",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"Reading listings from {args.listings_file}")
    print(f"Reading bookings from {args.bookings_file}")

    spark = (
        SparkSession.builder
        .appName("ListingsBookingsJoin")
        .getOrCreate()
    )

    # Read listings
    listings = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .option("sep", ",")
        .option("quote", '"')
        .option("escape", '"')
        .option("multiLine", "true")
        .option("mode", "PERMISSIVE")
        .csv(args.listings_file)
    )

    # Read bookings
    bookings = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(args.bookings_file)
    )

    print("Listings schema:")
    listings.printSchema()
    print("Bookings schema:")
    bookings.printSchema()

    # Join on listing_id (listings.id -> bookings.listing_id)
    aggregated = (
        listings
        .join(
            bookings,
            listings["id"] == bookings["listing_id"],
            how="inner",
        )
        .groupBy("listing_id", "name", "price")
        .agg(
            F.count("booking_id").alias("booking_count"),
        )
    )

    # Write output as CSV with header (to a directory)
    (
        aggregated
        .coalesce(1)  # optional, single file for convenience
        .write
        .mode("overwrite")
        .option("header", "true")
        .csv(args.output_path)
    )

    print(f"Aggregated results written to {args.output_path}")
    spark.stop()


if __name__ == "__main__":
    main()
