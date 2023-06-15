"""Imports"""
import logging
import os
import json
import datetime
import inspect

RELATIVE_PATH = "logs"
ABSOLUTE_PATH = os.path.abspath(RELATIVE_PATH)
LOG_FILE_NAME = "log.json"


def setup_logging():
    """Logger setup"""
    os.makedirs(ABSOLUTE_PATH, exist_ok=True)

    logger = logging.getLogger("PyMasterBot")
    logger.setLevel(logging.INFO)

    log_file = os.path.join(ABSOLUTE_PATH, LOG_FILE_NAME)
    file_handler = logging.FileHandler(log_file)

    logger.addHandler(file_handler)

    return logger


def log_message(message, command, user_input, text):
    """
    Logs the message details to a JSON log file.

    Args:
        message (Message): The message that triggered the logging.
        command (str): The command that triggered the logging.
        user_input (str): The input message.
        text (str): The text message to be logged.

    Returns:
        None
    """
    timestamp = datetime.datetime.now()
    frame = inspect.currentframe().f_back
    file_name = inspect.getframeinfo(frame).filename
    line_number = inspect.getframeinfo(frame).lineno

    log_data = {
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": message.chat.id,
        "username": message.from_user.username,
        "command": command,
        "input_message": user_input,
        "response": text,
        "source_file": file_name,
        "source_line": line_number,
    }

    log_file = os.path.join(ABSOLUTE_PATH, LOG_FILE_NAME)

    if not os.path.exists(ABSOLUTE_PATH):
        os.makedirs(ABSOLUTE_PATH)

    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as file:
            json.dump({"data": [log_data]}, file, ensure_ascii=False, indent=4)
    else:
        with open(log_file, "r", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {}

        existing_data.setdefault("data", []).append(log_data)

        with open(log_file, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
