"""
This block contains helper functions that processes the input CSV file
"""
import os
import tempfile
import uuid
from database.py_master_bot_database import PyMasterBotDatabase
from telebot import TeleBot


def handle_csv_file(telebot_instance: TeleBot, message):
    user_id = message.from_user.id
    db = PyMasterBotDatabase()

    # a block that allows only the administrator to add csv files to tables in the database
    if not db.is_admin(user_id):
        telebot_instance.reply_to(message, "У вас немає доступу для завантаження файлу CSV.")
        return

    if message.document.mime_type == 'text/csv':
        file = message.document
        file_extension = file.file_name.split('.')[-1]
        unique_filename = f"{str(uuid.uuid4())}.{file_extension}"  # Generate a unique filename
        file_info = telebot_instance.get_file(file.file_id)
        downloaded_file = telebot_instance.download_file(file_info.file_path)

        with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as temp_file:
            temp_filename = temp_file.name
            temp_file.write(downloaded_file)

        # Обробка файлу CSV
        db.add_data_from_csv(temp_filename)

        os.remove(temp_filename)

        telebot_instance.reply_to(message, "Файл CSV оброблено успішно.")
    else:
        telebot_instance.send_message(message.chat.id, "Будь ласка, відправте CSV файл.")



