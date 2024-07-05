from __future__ import print_function
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 6:
        print("""
        Usage: nyc_aggregations.py <s3_input_path> <s3_output_path> <dag_name> <task_id> <correlation_id>
        """, file=sys.stderr)
        sys.exit(-1)

    # Extract input arguments
    # The spark-submit command runs the script /home/hadoop/nyc_aggregations.py and passes additional arguments to it.
    # Inside the script, sys.argv is used to access these arguments, starting at position 0 with script script
    # Therefore, input_path = sys.argv[1] correctly refers to the first argument after the script name, which is the S3 input path.

    input_path = sys.argv[1] # Input S3 path
    output_path = sys.argv[2] # Output S3 path
    dag_task_name = sys.argv[3] + "." + sys.argv[4] # DAG name and task ID combined
    correlation_id = dag_task_name + " " + sys.argv[5] # Correlation ID combining DAG name, task ID, and provided ID

    # Initialize SparkSession
    # Set the application name as the correlation ID
    spark = SparkSession\
        .builder\
        .appName(correlation_id)\
        .getOrCreate()

    # Get Spark context
    sc = spark.sparkContext
    
    # Initialize logger
    log4jLogger = sc._jvm.org.apache.log4j
    logger = log4jLogger.LogManager.getLogger(dag_task_name)
    logger.info("Spark session started: " + correlation_id)

    # Read input data from Parquet files
    df = spark.read.parquet(input_path)
    df.printSchema # Print the schema of the DataFrame

    # Perform data aggregation
    df_out = df.groupBy('pulocationid', 'trip_type', 'payment_type').agg(sum('fare_amount').alias('total_fare_amount'))

    # Write the aggregated data to Parquet files, overwriting if output files already exist
    df_out.write.mode('overwrite').parquet(output_path)
    
    # Log Spark session stop and stop spark
    logger.info("Stopping Spark session: " + correlation_id)
    spark.stop()

