from src.utils.functions import *
from src.utils.spark_utils import get_aws_spark_session
spark=get_aws_spark_session('functional_tests')
RAW_TESTDATA = spark.createDataFrame([(1, 2, 3),(2,3,None),(4, 5, 6), (7, 8, 9),(1, 2, 3)],schema=['a', 'b', 'c'])

def test_deduplicate_data():
    try:
        deduplicate_data(spark,RAW_TESTDATA).count()==3
        print('De-duplicate unit tests passed')
    except:
        raise

def test_remove_nulls():
    try:
        clean_records_with_nulls(spark,1,RAW_TESTDATA).count()==4
        print('Remove-nulls unit tests passed')

    except:
        raise
test_deduplicate_data()
test_remove_nulls()