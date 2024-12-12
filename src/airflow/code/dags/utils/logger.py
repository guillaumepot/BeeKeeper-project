#airflow/code/dags/logger.py

import logging


# Text formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


# Logging config
basic_logger = logging.getLogger('basic_logger')
basic_logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

basic_logger.addHandler(console_handler)