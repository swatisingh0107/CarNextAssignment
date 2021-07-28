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

The data is written to an S3 bucket which will serve as datalake for our datamart.

Spin a free tier redshift cluster to read the data in the mart

Steps to read data:
- Create table
```
CREATE TABLE IF NOT EXISTS make_model_damage (
  build_year varchar(300),
  country varchar(300),
  make varchar(300),
  model varchar(300),
  avg_amount_damage decimal(10,2) 
)
```

- Load Data from S3
```
COPY public.make_model_damage FROM 's3://carnext-assignment2/part-00000-865e0cd9-98e7-4003-9d16-e52ec3cfc0f3-c000.snappy.parquet' CREDENTIALS 'aws_access_key_id=AKIA5IZR22OO3VADAW7R;aws_secret_access_key=0LJz8329lbXOO1UL49vQsTf/KDXPo7curdmWGNC3' CSV DELIMITER',';
```

- Create VIEW/Datamart to view top 10 make-model with high damages
```
CREATE OR REPLACE VIEW make_model_damage_top10_2016 AS 
SELECT * FROM 
(SELECT build_year,
 country,
 make,
 model,
 avg_amount_damage,
 row_number() over (partition by country order by avg_amount_damage desc) as damage_rank
 FROM make_model_damage
)ranks where build_year='2016' and damage_rank<=10;

```