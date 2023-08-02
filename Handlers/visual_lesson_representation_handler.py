import matplotlib.pyplot as plt

from io import BytesIO

from Handlers.help_functions import create_start_markup
from database.py_master_bot_database import PyMasterBotDatabase



import matplotlib.pyplot as plt
from io import BytesIO

def progress_lesson_visual_repr_function(message, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()

    user_lesson_items_progress = bot_db.get_user_by_id(chat_id).progress_lessons

    # Отримання загальної кількості уроків з таблиці 'lessons'
    total_lessons = bot_db.get_total_lessons_count()

    # Отримання кількості пройдених уроків користувачем
    completed_lessons = len(user_lesson_items_progress)

    # Налаштування параметрів графіку
    colors = ['gold', 'purple']

    # Створення графіка
    x = ['Пройдені уроки', 'Загальна кількість уроків']
    y = [completed_lessons, total_lessons]

    plt.bar(x, y, color=colors)

    # Відображення на осі Y тільки цілих чисел
    plt.yticks(range(0, int(max(y)) + 2, 2))

    # Додавання підписів значень до стовпчиків
    for i, v in enumerate(y):
        plt.text(x[i], v, str(v), ha='center', va='top', fontweight='bold')

    # Налаштування заголовка та підписів осей
    plt.title('Кількість пройдених items за уроками', fontweight=True)
    plt.xlabel('Назва уроку')
    plt.ylabel('Кількість пройдених items')

    # Збереження графіка в буфері
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Відправка графіка як фото у відповідь на команду
    bot.send_photo(message.chat.id, photo=buffer)

    # Очищення графіка
    plt.clf()
