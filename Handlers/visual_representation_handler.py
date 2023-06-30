import matplotlib.pyplot as plt

from io import BytesIO
from database.py_master_bot_database import PyMasterBotDatabase


def progress_testing_visual_repr_function(message, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()

    user_testing_progress = bot_db.get_user_by_id(chat_id).progress_testing

    # Створення графіка
    x = [key for key in user_testing_progress.keys()]
    y = [len(value) for value in user_testing_progress.values()]

    plt.bar(x, y)
    # Налаштування заголовка та підписів осей
    plt.title('Кількість успішно складених тестів за рівнями', fontweight=True)
    plt.xlabel('Назва рівня')
    plt.ylabel('Кількість тестів')

    # Збереження графіка в буфері
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Відправка графіка як фото у відповідь на команду
    bot.send_photo(message.chat.id, photo=buffer)

    # Очищення графіка
    plt.clf()
