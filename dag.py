import itertools
import json
import os
from datetime import date, datetime, timedelta
from pprint import pprint

from airflow import DAG
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['vikramtheone1@gmail.com'],
    'dataflow_default_options': {
        'runner':
        'DataflowRunner',
        'extra_package':
        '/home/airflow/gcs/dags/dataflow/vikram/dist/Common-1.0.0.tar.gz',
        'setup_file':
        '/home/airflow/gcs/dags/dataflow/vikram/setup.py',
        'requirements_file':
        '/home/airflow/gcs/dags/dataflow/vikram/requirements.txt',
        'start_date':
        '2018-01-01',
        'end_date':
        '2018-01-02'
    }
}

dag = DAG('etl_dataflow', default_args=default_args, schedule_interval='@once')

START = DataFlowPythonOperator(
    task_id='init',
    py_file='/home/airflow/gcs/dags/dataflow/vikram/etl.py',
    dag=dag)
