from main.functions import deduplicate_data
from setup.spark_utils import get_spark_session
spark=get_spark_session('functional_tests')
RAW_TESTDATA = spark.createDataFrame([(1, 2, 3),(4, 5, 6), (7, 8, 9),(1, 2, 3)],schema=['a', 'b', 'c'])


def test_deduplicate_data():
    try:
        deduplicate_data(spark,RAW_TESTDATA,True).count()==3
        print('De-duplicate unit tests passed')
    except:
        raise
RAW_TESTDATA.show()