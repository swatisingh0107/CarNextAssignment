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
    schedule_interval='30 6 * * *',
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

cmd = "ssh -o StrictHostKeyChecking=no -i /keys/emr.pem ec2-user@spar-ds-emr.ygroup.cloud " \
      "'cd spar && git pull' "

GET_CODE = BashOperator(
    task_id="GET_CODE",
    bash_command=cmd,
    dag=dag)

cmd = "ssh -o StrictHostKeyChecking=no -i /keys/emr.pem ec2-user@spar-ds-emr.ygroup.cloud " \
      "'python3.6 spar/notebooks/Dashboarding/create_output.py' "

RUN_JOB = BashOperator(
    task_id="RUN_JOB",
    bash_command=cmd,
    dag=dag)

FLOW_START >> GET_CODE >> RUN_JOB >> FLOW_END

