import matplotlib.pyplot as plt

from io import BytesIO

from Handlers.help_functions import create_start_markup
from database.py_master_bot_database import PyMasterBotDatabase


def progress_code_testing_visual_repr_function(message, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()

    user_coding_progress = bot_db.get_user_by_id(chat_id).progress_coding

    # Налаштування параметрів графіку
    colors = ['pink', 'purple', 'green']

    # Створення графіка
    x = [key for key in user_coding_progress.keys()]
    y = [len(value) for value in user_coding_progress.values()]

    plt.bar(x, y, color=colors)

    # Відображення на осі У тільки цілих чисел
    plt.yticks(range(0, int(max(y)) + 2, 2))

    # Додавання підписів значень до стовпців
    for i, v in enumerate(y):
        plt.text(x[i], v, str(v), ha='center', va='top', fontweight='bold')

    # Налаштування заголовка та підписів осей
    plt.title('Кількість успішно складених тестів (CODDING) за рівнями', fontweight=True)
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


def progress_code_level_visual_repr_function(message, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()

    # База даних з рівнями складності та значеннями
    user_coding_progress = bot_db.get_user_by_id(chat_id).progress_coding

    max_value = 20

    # Налаштування параметрів графіку
    colors = ['yellow', 'purple', 'green', 'pink']

    # Створення підграфіків
    fig, axes = plt.subplots(1, 3, figsize=(10, 4))

    # Побудова кругових діаграм для кожного рівня складності
    for i, (level, values) in enumerate(user_coding_progress.items()):
        ax = axes[i]  # Отримання активного підграфіка
        completed_code_tasks = len(values)
        remaining_code_tasks = max_value - completed_code_tasks
        sizes = [completed_code_tasks, (remaining_code_tasks if remaining_code_tasks > 0 else 0)]

        explode = [0.1] + [0] * (len(sizes) - 1)  # Підсвічування першого сегменту
        '''
        labels = [f'{level} ({completed_tasks}/{max_value})', ''] if completed_tasks < max_value else [
            f'{level} ({completed_tasks}/{max_value})', f'\n\n\n\n\n\n\n\n\n'
                                                        f'Виконано\nдостатньо\nзавдань\nрівня\n{level}']
        '''
        def form_labels():
            if completed_code_tasks == 0:
                return f'Немає\nвиконаних\nзавдань\nрівня\n{level}', ''
            elif completed_code_tasks < max_value:
                return f'{level} ({completed_code_tasks}/{max_value})', ''
            else:
                return f'{level} ({completed_code_tasks}/{max_value})', f'\n\n\n\n\n\n\n\n\n' \
                                                                   f'Виконано\nдостатньо\nзавдань\nрівня\n{level}'

        ax.pie(sizes, labels=form_labels(), colors=(colors[i], colors[-1]), explode=explode, autopct='%1.1f%%')
        ax.set_title(level.capitalize(), fontsize=17)
        ax.tick_params(labelsize=16)  # Розмір шрифту підписів

    # Загальний заголовок
    fig.suptitle('Прогрес тестування (ТЕОРІЯ) за рівнями складності', fontsize=18)

    # Збереження графіка в буфері
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Відправка графіка як фото у відповідь на команду
    bot.send_photo(message.chat.id, photo=buffer)

    # Очищення графіка
    plt.clf()


def progress_code_theory_tests_repr_function(message, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()

    user_coding_progress = bot_db.get_user_by_id(chat_id).progress_coding

    total_value = sum(len(value) for value in user_coding_progress.values())

    message_text = f"<b>Ви досягли успіху у виконанні {total_value} завдань. </b>"

    if total_value != 0:
        message_text += " З них:\n"
        for key, value in user_coding_progress.items():
            message_text += f"на рівні {key}: {len(value)},    {'{:.2f}%'.format(len(value) / total_value * 100)}\n"

    message_text += f"\nВаш ранг за кількістю виконаних тестів 💭 <b>{bot_db.check_rank(chat_id).upper()}</b>"

    bot.send_message(chat_id, message_text, parse_mode="HTML", reply_markup=create_start_markup())


def user_visual_code_repr_function(message, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()
    current_user = bot_db.get_user_by_id(chat_id)

    top_users = ""  # create a rating for display
    counter = 0

    top_users_by_score = [(user.id, user.name, user.username, user.score)
                          for user in bot_db.top_users_by_score(top_number=5)]  # number of persons in the rating
    if top_users_by_score:

        for user in top_users_by_score:
            counter += 1
            if user[0] == current_user.id:
                top_users += f"<b>{counter}. {user[1]}({user[2]}) - {user[3]} pts</b> (THIS IS YOU!)\n"
            else:
                top_users += f"{counter}. {user[1]}({user[2]}) - {user[3]} pts\n"

    user_score_position = bot_db.rank_user_score(user_id=chat_id)

    bot.send_message(chat_id, f"You have <b>{current_user.status}</b> status until "
                              f"{current_user.paid_until if current_user.paid_until else 'the moment of payment'}.\n\n"
                              f"{message.chat.first_name}, your total score is <b>{current_user.score} pts</b>.\n"
                              f"You take <b>{user_score_position} place</b> in the overall rating.\n\n"
                              f"TOP-{counter} 🏆:\n {top_users}", parse_mode="HTML")
