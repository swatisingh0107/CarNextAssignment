# CarNextAssignment
This repository contains four major components

1. Infrastructure: Dockerfile to containerize Hadoop, Airflow
2. ETL: Airflow to define DAGS and Pyspark for ETL
3. Driver Management
4. AWS Config Management

##**Instructions to run this project**
####Prerequisites:
- Git
- Docker

Clone this repository in your instance/local machine.

```
cd CarNextAssignment
docker-compose up -d
```

The docker image is built to setup the environment and airflow is deployed
The pipeline DAG can be executed from the Airflow Webserver Interface

```
http://localhost:8080/admin/
```

Docker/Dockerfile builds Airflow, Java, Hadoop and Spark required to execute this project.
Edit the dags/utils/spark_utils file to add AWS Access Key and Secret
```
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", <your-key-id>)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", <your-key-secret>)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", <your-s3 endpoint>)
    
```
 
Save the changes and trigger the dag from Airflow interface
