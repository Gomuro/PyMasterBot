
"""
This block contains helper functions that processes the input CSV file
"""
import os
import tempfile

from Handlers.exception_handler import handle_exception
from database.py_master_bot_database import PyMasterBotDatabase


def handle_csv_lessons(telebot_instance, message, document):
    try:

        user_id = message.from_user.id
        db = PyMasterBotDatabase()  # Create a database object

        # Check if the user has administrator permissions
        if not db.is_admin(user_id):
            telebot_instance.reply_to(message, "You don't have permission to upload the file.")
            return

        # Check if the message contains a CSV file
        if message.document.mime_type == 'text/csv':

            if document.file_name == "lessons.csv":
                file_extension = document.file_name.split('.')[-1]
                file_info = telebot_instance.get_file(document.file_id)
                downloaded_file = telebot_instance.download_file(file_info.file_path)

                with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as temp_file:
                    temp_filename = temp_file.name
                    temp_file.write(downloaded_file)

                # Processing a CSV file
                db.add_lessons_csv(temp_filename)

                os.remove(temp_filename)

                telebot_instance.reply_to(message, "CSV file has been processed successfully.")

    except Exception as e:
        handle_exception(e, telebot_instance)


def handle_csv_test_tasks(telebot_instance, message, document):
    try:

        user_id = message.from_user.id
        db = PyMasterBotDatabase()  # Create a database object

        # Check if the user has administrator permissions
        if not db.is_admin(user_id):
            telebot_instance.reply_to(message, "You don't have permission to upload the file.")
            return

        # Check if the message contains a CSV file
        if message.document.mime_type == 'text/csv':

            if document.file_name == "test_tasks.csv":
                file_extension = document.file_name.split('.')[-1]
                file_info = telebot_instance.get_file(document.file_id)
                downloaded_file = telebot_instance.download_file(file_info.file_path)

                with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as temp_file:
                    temp_filename = temp_file.name
                    temp_file.write(downloaded_file)

                # Processing a CSV file
                db.add_test_tasks_csv(temp_filename)

                os.remove(temp_filename)

                telebot_instance.reply_to(message, "CSV file has been processed successfully.")

    except Exception as e:
        handle_exception(e, telebot_instance)


def handle_csv_code_tasks(telebot_instance, message, document):
    try:

        user_id = message.from_user.id
        db = PyMasterBotDatabase()  # Create a database object

        # Check if the user has administrator permissions
        if not db.is_admin(user_id):
            telebot_instance.reply_to(message, "You don't have permission to upload the file.")
            return

        # Check if the message contains a CSV file
        if message.document.mime_type == 'text/csv':

            if document.file_name == "code_tasks.csv":
                file_extension = document.file_name.split('.')[-1]
                file_info = telebot_instance.get_file(document.file_id)
                downloaded_file = telebot_instance.download_file(file_info.file_path)

                with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as temp_file:
                    temp_filename = temp_file.name
                    temp_file.write(downloaded_file)

                # Processing a CSV file
                db.add_code_tasks_csv(temp_filename)

                os.remove(temp_filename)

                telebot_instance.reply_to(message, "CSV file has been processed successfully.")

    except Exception as e:
        handle_exception(e, telebot_instance)
