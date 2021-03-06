from src.utils.spark_utils import get_aws_spark_session
from pyspark.sql.types import IntegerType
from src.utils.functions import write_df_to_paruqet, get_data_csv, deduplicate_data, \
    clean_records_with_nulls, clean_strings, calulate_avg_damage, write_to_csv

urlpath = 'https://s3-eu-west-1.amazonaws.com/carnext-data-engineering-assignment/test_data/'
hadoop_dir = '/hdfs/carnext-data-engineering-assignment/raw/test_data/'
cleansed_path = '/hdfs/carnext-data-engineering-assignment/cleansed/damage_report'


def run_app(app_name):
    spark=get_aws_spark_session("make_model_avg_damage")
    if app_name == "Get_data":
        for num in range(1,8):
            filename = 'vehicle.csv000{0}_part_00.gz'.format(num)
            striped_filename=str.replace(filename,'.gz','')
            get_data_csv(urlpath+filename,'/home/swati.singh/test_data','/hdfs/carnext-data-engineering-assignment/raw/')
    elif app_name=='clean_data':
        raw_df = spark.read.csv(hadoop_dir,header=True,sep=',')
        #Apply cleaning functions to dataframe
        cleaned_df = deduplicate_data(spark,raw_df)
        cleaned_df = clean_records_with_nulls(spark,20,cleaned_df)
        cleaned_df = clean_strings(cleaned_df,['make','model'])
        cleaned_df = cleaned_df.filter(cleaned_df.make!='').filter(cleaned_df.model!='').filter(cleaned_df.build_year!='')
        cleaned_df=cleaned_df.withColumn('build_year',cleaned_df['build_year'].cast(IntegerType()))
        cleaned_df=cleaned_df.filter(cleaned_df.build_year>=1990)
        print("Records in cleaned df:"+str(cleaned_df.count()))
        write_df_to_paruqet(cleaned_df, cleansed_path)

    elif app_name=='write_data':
        #Write aggregated output
        s3_path='s3a://carnext-assignment/agg_result'
        cleaned_df=spark.read.parquet(cleansed_path)
        result=calulate_avg_damage(spark,cleaned_df)
        write_to_csv(result,s3_path)
        # result.show()


import argparse
parser =argparse.ArgumentParser()
parser.add_argument("app_name", help= "Name of the app to execute" )
args=parser.parse_args()

run_app(args.app_name)

