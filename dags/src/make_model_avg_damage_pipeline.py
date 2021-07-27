from utils.functions import *
from utils.spark_utils import get_aws_spark_session

spark=get_aws_spark_session("make_model_avg_damage")
urlpath='https://s3-eu-west-1.amazonaws.com/carnext-data-engineering-assignment/test_data/'
for num in range(1,8):
    filename = 'vehicle.csv000{0}_part_00.gz'.format(num)
    striped_filename=str.replace(filename,'.gz','')
    get_data_csv(urlpath+filename,'/home/swati.singh/test_data','/hdfs/carnext-data-engineering-assignment/raw/')
    hadoop_dir = '/hdfs/carnext-data-engineering-assignment/raw/test_data/{0}'.format(striped_filename)
raw_df = spark.read.csv(hadoop_dir,header=True,sep=',')
cleaned_df = deduplicate_data(spark,raw_df)
cleaned_df = clean_records_with_nulls(spark,20,cleaned_df)
cleaned_df = cleaned_df.filter(cleaned_df.make.isNotNull()).filter(cleaned_df.model.isNotNull())
cleaned_df = clean_strings(cleaned_df,['make','model'])
cleaned_df.orderBy(cleaned_df.make).show()

# #Write dataset to cleansed path
# s3_path='s3a://carnext-assignment-cleansed/make_model_damage_amount/{0}'.format(striped_filename)
# write_df_to_paruqet(spark,cleaned_df,s3_path)
#Write aggregated output
# s3_path='s3a://carnext-assignment-curated/make_model_damage_amount/{0}'.format(striped_filename)
result=calulate_avg_damage(spark,cleaned_df)
connectionProperties = {
  "user" : 'admin',
  "password" : 'AKIA5IZR22OOTKYBL7HM'
}
result.write.jdbc(url='jdbc:mysql://carnext.c6cbiuhhyix3.eu-west-1.rds.amazonaws.com:3306/carnext',
          table='carnext',properties=connectionProperties,mode='overwrite')

