"""
This block contains helper functions that processes the input CSV file
"""
import os
import tempfile
import uuid
from database.py_master_bot_database import PyMasterBotDatabase


def handle_csv_file(telebot_instance, message, document):
    user_id = message.from_user.id
    db = PyMasterBotDatabase()  # Створення об'єкту бази даних

    # Перевірка, чи користувач є адміністратором
    if not db.is_admin(user_id):
        telebot_instance.reply_to(message, "У вас немає доступу для завантаження файлу.")
        return

    # Перевірка, чи повідомлення містить файл CSV
    if message.document.mime_type == 'text/csv':

        # Отримання списку назв таблиць
        table_names = db.get_all_tables()

    if document.file_name == "test_tasks.csv":
        selected_table = "test_tasks"  # Збереження обраної таблиці
        file_extension = document.file_name.split('.')[-1]
        unique_filename = f"{str(uuid.uuid4())}.{file_extension}"  # Генерація унікального імені файлу
        file_info = telebot_instance.get_file(document.file_id)
        downloaded_file = telebot_instance.download_file(file_info.file_path)

        with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as temp_file:
            temp_filename = temp_file.name
            temp_file.write(downloaded_file)

        # Обробка файлу CSV
        db.add_data_from_csv(temp_filename)

        os.remove(temp_filename)

        telebot_instance.reply_to(message, "Файл CSV оброблено успішно.")
    else:
        telebot_instance.send_message(message.chat.id, "Будь ласка, відправте файл у форматі CSV з такою самою назвою"
                                                       " як нава таблиці в Базі Даннх.")

