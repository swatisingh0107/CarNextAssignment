from pyspark.sql import SparkSession
import os
def get_aws_spark_session(app_name):
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.amazonaws:aws-java-sdk-pom:1.10.34,org.apache.hadoop:hadoop-aws:2.7.2,mysql:mysql-connector-java:8.0.16 pyspark-shell'
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    #Change me for AWS authentication
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", "AKIA5IZR22OO3VADAW7R")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "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")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.eu-west-1.amazonaws.com")
    return spark



print(get_aws_spark_session('test'))