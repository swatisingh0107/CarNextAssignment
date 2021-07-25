import configparser
import os
from pyspark import SparkConf
from pyspark.sql import SparkSession
from definitions import CONFIG_PATH
def get_spark_app_config():
    spark_conf=SparkConf()
    config=configparser.ConfigParser()

    config.read(os.path.abspath("setup/spark.conf"))
    config.read(CONFIG_PATH)
    print(CONFIG_PATH)

    for key,value in config.items("SPARK_APP_CONFIGS"):
        spark_conf.set(key,value)

    return spark_conf

def get_spark_session(app_name):
    conf = get_spark_app_config()
    spark_session = SparkSession \
        .builder \
        .appName(app_name) \
        .config(conf=conf) \
        .getOrCreate()
    return spark_session


