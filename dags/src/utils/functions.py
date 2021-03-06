import errno
import os
import subprocess
import pyspark.sql.functions as F
from pyspark.sql.types import StringType,DoubleType
import wget
from pyspark.sql import Window



def run_cmd(args_list):
    """
    run linux commands
    """
    # import subprocess
    print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return =  proc.returncode
    return s_return, s_output, s_err


def get_data_csv(path,output_dir,hadoop_dir):
    #This function is to download the .gz compressed file from given url and decompress it
    #The decompressed file is then copied to Hadoop distributed file system
    try:
        os.makedirs(output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    try:
        download=wget.download(path,output_dir)
        filename=download.split('/')[-1]
        print('Downloaded file:'+filename)
        #Decompress file
        run_cmd(["gzip","-d",output_dir+'/'+filename])
        #Copy to Hadoop System
        run_cmd(["hadoop","fs","-copyFromLocal",output_dir,hadoop_dir])
        #Remove the downloaded file
        run_cmd(["rm","-rf",output_dir])

    except Exception as error:
        print('File path not found:'+filename)

def deduplicate_data(spark,df):
    df_count=df.count()
    print("Read {0} records".format(df.count()))
    df_deduplicated=df.dropDuplicates()
    df_deduplicated_records = df_deduplicated.count()
    print("Removed {0} duplicate records".format(df_count-df_deduplicated_records))
    return df_deduplicated


def clean_records_with_nulls(spark,null_threshhold,df):
    #Remove records if null values is greater than null_threshhold for each record
    df = df.withColumn('numNulls', sum(df[col].isNull().cast('int') for col in df.columns)).orderBy(
        F.desc('numNulls'))
    df=df.filter(df.numNulls<=null_threshhold)
    return df

def write_df_to_paruqet(df,write_path):
    df.repartition(1).write.parquet(write_path, mode='overwrite')
    print('Wrote to cleansed bucket')

def clean_strings(df,cols):
    #Function to convert string columns to lower case and remove extra whitespaces
    def remove_extra_whitespaces(str1):
        if str1 is not None:
            str1=str1.strip().replace('.',' ')

            return "".join(str1.split(' '))
        else:
            return str1

    convertUDF = F.udf(lambda z: remove_extra_whitespaces(z), StringType())
    for col in cols:
        df=df.withColumn(col,F.lower(convertUDF(F.col(col))))
        df=df.withColumn(col,F.regexp_replace(F.col(col),'[^A-Za-z0-9\\s+]+',''))
    return df

def calulate_avg_damage(spark,df,curated_path=''):
    df=df.withColumn('amount_damage',df['amount_damage'].cast(DoubleType()))
    df=df.fillna({'amount_damage':0})
    window=Window.partitionBy('country').orderBy(F.desc('avg_amount_damage'))
    df=df.groupBy(df.build_year,df.country,df.make,df.model).agg(F.avg(df.amount_damage).alias('avg_amount_damage'))
    # df = df.select(F.col('*'), F.row_number().over(window).alias('row_number')).where(F.col('row_number') <= 10)
    df.show()
    return df


def write_to_csv(df,path):
    df.repartition(1).write.csv(path,header=True,sep=',',mode='overwrite')

# def write_to_db(result):
#     url='jdbc:redshift//carnext.cxrqdodkuag3.us-east-2.redshift.amazonaws.com:5439/carnext?user=admin&password=??'
#     result.write.mode('overwrite').option('driver','com.amazon.redshift.jdbc4.Driver').jdbc(url=url,table='public.make_model_damage')



