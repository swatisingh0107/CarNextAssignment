import sys
import os
import datetime
import logging

import airflow
from airflow.models import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.bash_operator import BashOperator

DAG_ID = "avg_damage_vehicle_country"
DAG_DESCRIPTION = "Pipeline to calculate top 10 avg damage amount of vehicle per country"
DAG_ROOT_PATH = os.path.dirname(__file__)
if DAG_ROOT_PATH not in sys.path:
	sys.path.append(DAG_ROOT_PATH)

DAG_ARGS = {
	'owner': 'Swati Singh',
	'start_date': datetime.datetime(2021,7, 22),
	'provide_context': True,
	'depends_on_past': False,

}

dag = DAG(
    dag_id=DAG_ID,
    default_args=DAG_ARGS,
    description=DAG_DESCRIPTION,
    schedule_interval='* * * * 5',
    concurrency=1,
    max_active_runs=1,
    catchup=False

)

FLOW_START = DummyOperator(
        task_id="FLOW_START",
        dag=dag)

FLOW_END = DummyOperator(
        task_id="FLOW_END",
        trigger_rule=TriggerRule.ONE_SUCCESS,
        dag=dag)

cmd = "cd /usr/local/airflow/dags/ && python /usr/local/airflow/dags/src/tests/test_functions.py"
RUN_TESTS = BashOperator(
    task_id="RUN_TESTS",
    bash_command=cmd,
    dag=dag)

cmd = "cd /usr/local/airflow/dags/ && python /usr/local/airflow/dags/src/make_model_avg_damage_pipeline.py"

PROCESS_DF = BashOperator(
    task_id="RUN_JOB",
    bash_command=cmd,
    dag=dag)

FLOW_START >> RUN_TESTS>>PROCESS_DF >> FLOW_END
