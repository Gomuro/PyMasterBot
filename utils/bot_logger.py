"""Imports"""
import logging
import os
import json
import datetime


RELATIVE_PATH = 'data/logs'
ABSOLUTE_PATH = os.path.abspath(RELATIVE_PATH)
LOG_FILE_FORMAT = '%Y-%m-%d.json'


def setup_logging():
    """Logger setup"""
    os.makedirs(ABSOLUTE_PATH, exist_ok = True)

    logger = logging.getLogger('PyMasterBot')
    logger.setLevel(logging.INFO)

    current_date = datetime.datetime.now().strftime(LOG_FILE_FORMAT)
    log_file = os.path.join(ABSOLUTE_PATH, current_date)
    file_handler = logging.FileHandler(log_file)

    logger.addHandler(file_handler)

    return logger


def log_message(command, code, text):
    """
    Logs the message details to a JSON log file.

    Args:
        command (str): The command that triggered the logging.
        code (str): The code associated with the log message.
        text (str): The text message to be logged.

    Returns:
        None
    """
    timestamp = datetime.datetime.now()

    log_data = {
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'command': command,
        'code': code,
        'response': text,
    }

    log_file = os.path.join(ABSOLUTE_PATH, datetime.datetime.now().strftime(LOG_FILE_FORMAT))

    if not os.path.exists(log_file):
        with open(log_file, 'w', encoding = 'utf-8') as file:
            json.dump({'data': [log_data]}, file, ensure_ascii = False, indent = 4)
    else:
        with open(log_file, 'r', encoding = 'utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {}

        existing_data.setdefault('data', []).append(log_data)

        with open(log_file, 'w', encoding = 'utf-8') as file:
            json.dump(existing_data, file, ensure_ascii = False, indent = 4)
