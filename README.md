# CarNextAssignment
This repository contains four major components

1. Infrastructure: Dockerfile to containerize Hadoop, Airflow
2. ETL: Airflow to define DAGS and Pyspark for ETL
3. Driver Management
4. AWS Config Management

##Instructions to run this project  
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
--CREATE DATABASE carnext
DROP TABLE IF EXISTS make_model_damage;
CREATE TABLE IF NOT EXISTS make_model_damage (
  build_year int,
  country varchar(300),
  make varchar(300),
  model varchar(3000),
  avg_amount_damage float 
)
)
```

- Load Data from S3
```
COPY public.make_model_damage (build_year,country,make,model,avg_amount_damage) 
FROM 's3://carnext-assignment2/part-00000-882bbbc0-30ba-469f-86e9-aeecf47a2f27-c000.csv' 
CREDENTIALS 'aws_access_key_id=AKIA5IZR22OO3VADAW7R;aws_secret_access_key=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' 
CSV
DELIMITER ','
IGNOREHEADER 1;
```

- Create VIEW/Datamart to view top 10 make-model with high damages
```
DROP VIEW make_model_damage_top10_2016;

CREATE OR REPLACE VIEW make_model_damage_top10_2016 AS 
SELECT * FROM 
(SELECT build_year,
 country,
 make,
 model,
 avg_amount_damage,
 row_number() over (partition by country order by avg_amount_damage desc) as damage_rank_in_year_country
 FROM (Select * FROM make_model_damage where build_year='2016')t1
)t2 where damage_rank_in_year_country<=10;

```
