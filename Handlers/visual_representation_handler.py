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


def progress_level_visual_repr_function(message, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()

    # База даних з рівнями складності та значеннями
    user_testing_progress = bot_db.get_user_by_id(chat_id).progress_testing

    max_value = 20

    # Налаштування параметрів графіку
    colors = ['green', 'bisque']

    # Створення підграфіків
    fig, axes = plt.subplots(1, 3, figsize=(10, 4))

    # Побудова кругових діаграм для кожного рівня складності
    for i, (level, values) in enumerate(user_testing_progress.items()):
        ax = axes[i]  # Отримання активного підграфіка
        completed_tasks = len(values)
        remaining_tasks = max_value - completed_tasks
        sizes = [completed_tasks, (remaining_tasks if remaining_tasks > 0 else 0)]

        explode = [0.1] + [0] * (len(sizes) - 1)  # Підсвічування першого сегменту
        labels = [f'{level} ({completed_tasks}/{max_value})', ''] if completed_tasks < max_value else [
            f'{level} ({completed_tasks}/{max_value})', f'\n\n\n\n\n\n\n\n\n'
                                                        f'Виконано\nдостатньо\nзавдань\nрівня\n{level}']
        ax.pie(sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%')
        ax.set_title(level.capitalize(), fontsize=17)
        ax.tick_params(labelsize=16)  # Розмір шрифту підписів

    # Загальний заголовок
    fig.suptitle('Прогрес за рівнями складності', fontsize=18)

    # Збереження графіка в буфері
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Відправка графіка як фото у відповідь на команду
    bot.send_photo(message.chat.id, photo=buffer)

    # Очищення графіка
    plt.clf()
