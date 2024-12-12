ARG PYTHON_VERSION=3.12
FROM apache/airflow:slim-latest-python${PYTHON_VERSION}


USER airflow

# Install packages specified in requirements.txt
COPY ./requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt
RUN rm /opt/airflow/requirements.txt


# Install Airflow additional packages
RUN pip install 'apache-airflow[postgres]'
RUN pip install 'apache-airflow[celery]'