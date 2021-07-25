#!/usr/bin/env bash
echo "Setting spark home"
export SPARK_HOME=/usr/hdp/3.0.1.0-187/spark2
echo $SPARK_HOME
export PYSPARK_PYTHON=python3.7
echo $PYSPARK_PYTHON
export PYSPARK_DRIVER_PYTHON=python3.7
export PYTHONPATH=/usr/hdp/3.0.1.0-187/spark2/python:/usr/hdp/3.0.1.0-187/spark2/python/lib/py4j-0.10.7-src.zip
echo $PYTHONPATH
