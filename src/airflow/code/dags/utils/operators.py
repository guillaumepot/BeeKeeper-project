#airflow/code/dags/tasks.py


# LIB
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.filesystem import FileSensor


import datetime
import os


"""
Airflow Functions
"""
def generate_task_file_sensor(dag: DAG,
                              task_id:str = "file_sensor",
                              filepath: str = ".",
                              poke_interval:int = 60,
                              timeout:int = 180,
                              mode:str = "reschedule",
                              trigger_rule:str = "all_done",
                              on_success_callback: callable = None,
                              on_failure_callback: callable = None,
                              doc_md:str = "") -> FileSensor:
    """
    Generate a FileSensor task to detect new files in a directory.

    Success Criteria:
    - Task will be successful if a new file is detected in the directory

    Failure Criteria:
    - Task will fail if no new files are detected in the directory after the timeout period

    Args:
    - dag: DAG object
    - task_id: str - Task ID
    - filepath: str - File path to detect new files
    - poke_interval: int - Interval in seconds to check for new files
    - timeout: int - Timeout in seconds for the sensor task
    - mode: str - Mode for the sensor task
    - trigger_rule: str - Trigger rule for the task
    - on_success_callback: callable - Callback function for task success
    - on_failure_callback: callable - Callback function for task failure
    - doc_md: str - Task documentation

    Returns:
    - FileSensor: FileSensor task
    """
    return FileSensor(
        dag = dag,
        task_id = task_id,
        fs_conn_id = "fs_default",
        filepath = filepath,
        poke_interval = poke_interval,
        timeout = timeout,
        mode = mode,
        trigger_rule = trigger_rule,
        on_success_callback = on_success_callback,
        on_failure_callback = on_failure_callback,
        doc_md = doc_md
    )




def generate_task_python_operator(dag: DAG,
                                  task_id:str = "python_operator",
                                  python_callable: callable = None,
                                  op_kwargs: dict = {},
                                  retries:int = 1,
                                  retry_delay:datetime.timedelta = datetime.timedelta(seconds = 300),
                                  trigger_rule:str = "all_done",
                                  on_success_callback: callable = None,
                                  on_failure_callback: callable = None,
                                  doc_md:str = "") -> PythonOperator:
    """
    Generate a PythonOperator task to execute a Python callable function.

    Args:
    - dag: DAG object
    - task_id: str - Task ID
    - python_callable: callable - Python function to execute
    - op_kwargs: dict - Function keyword arguments
    - retries: int - Number of retries for the task
    - retry_delay: timedelta - Delay between retries
    - trigger_rule: str - Trigger rule for the task
    - on_success_callback: callable - Callback function for task success
    - on_failure_callback: callable - Callback function for task failure
    - doc_md: str - Task documentation

    Returns:
    - FileSensor: FileSensor task
    """
    return PythonOperator(
        dag = dag,
        task_id = task_id,
        python_callable = python_callable,
        op_kwargs = op_kwargs,
        retries = retries,
        retry_delay = retry_delay,
        trigger_rule = trigger_rule,
        on_success_callback = on_success_callback,
        on_failure_callback = on_failure_callback,
        doc_md = doc_md
    )




def generate_task_bash_operator(dag: DAG,
                                task_id: str,
                                bash_command: str,
                                retries:int = 1,
                                retry_delay:datetime.timedelta = datetime.timedelta(seconds = 300),
                                trigger_rule:str = "all_done",
                                on_success_callback: callable = None,
                                on_failure_callback: callable = None,
                                doc_md:str = ""
                                ) -> BashOperator:
    """
    Generate a BashOperator task to execute a bash command.

    Args:
    - dag: DAG object
    - task_id: str - Task ID
    - bash_command: callable - Python function to execute
    - retries: int - Number of retries for the task
    - retries: int - Number of retries for the task
    - retry_delay: timedelta - Delay between retries
    - trigger_rule: str - Trigger rule for the task
    - on_success_callback: callable - Callback function for task success
    - on_failure_callback: callable - Callback function for task failure
    - doc_md: str - Task documentation

    Returns:
    - FileSensor: FileSensor task
    """
    return BashOperator(
        dag = dag,
        task_id = task_id,
        bash_command = bash_command,
        retries = retries,
        retry_delay = retry_delay,
        trigger_rule = trigger_rule,
        on_success_callback = on_success_callback,
        on_failure_callback = on_failure_callback,
        doc_md = doc_md
    )



def generate_task_trigger_dag_operator(dag: DAG,
                                        task_id: str,
                                        trigger_dag_id: str,
                                        retries:int = 1,
                                        retry_delay:datetime.timedelta = datetime.timedelta(seconds = 300),
                                        trigger_rule:str = "all_success",
                                        on_success_callback: callable = None,
                                        on_failure_callback: callable = None,
                                        doc_md:str = ""
                                        ) -> TriggerDagRunOperator:
    """
    Generate a TriggerDagRunOperator task to trigger a new DAG.

    Args:
    - dag: DAG object
    - task_id: str - Task ID
    - trigger_dag_id: str - DAG to trigger
    - retries: int - Number of retries for the task
    - retry_delay: timedelta - Delay between retries
    - trigger_rule: str - Trigger rule for the task
    - on_success_callback: callable - Callback function for task success
    - on_failure_callback: callable - Callback function for task failure
    - doc_md: str - Task documentation

    Returns:
    - TriggerDagRunOperator: TriggerDagRunOperator task
    """
    return TriggerDagRunOperator(dag = dag,
                                 task_id = task_id,
                                 trigger_dag_id = trigger_dag_id,   # Dag to trigger
                                 retries = retries,
                                 retry_delay = retry_delay,
                                 trigger_rule = trigger_rule,
                                 on_success_callback = on_success_callback,
                                 on_failure_callback = on_failure_callback,
                                 doc_md = doc_md
                                )