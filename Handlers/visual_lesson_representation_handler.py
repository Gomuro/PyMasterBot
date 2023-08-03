import os

from Handlers.help_functions import create_start_markup
from database.py_master_bot_database import PyMasterBotDatabase

import matplotlib.pyplot as plt
from io import BytesIO


def progress_lesson_visual_round_repr_function(message, bot):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()

        user_lesson_items_progress = bot_db.get_user_by_id(chat_id).progress_lessons

        # Отримання загальної кількості уроків з таблиці 'lessons'
        total_lessons = bot_db.get_total_lessons_count()

        # Отримання кількості пройдених уроків користувачем
        completed_lessons = len(user_lesson_items_progress)

        # Налаштування параметрів графіку
        colors = ['yellow', 'purple']

        # Створення нової фігури з кольоровим фоном
        plt.figure(facecolor='lightblue')

        # Створення першого графіка (загальна кількість уроків)
        plt.subplot(1, 2, 1)
        x_total = ['Пройдені', '']
        y_total = [completed_lessons, total_lessons - completed_lessons]
        plt.pie(y_total, labels=x_total, colors=colors, autopct='%1.0f%%', startangle=140)
        plt.title('Кількість пройдених уроків', fontweight=True)

        # Створення другого графіка (кількість пройдених уроків)
        plt.subplot(1, 2, 2)
        x_completed = ['Пройдені', 'Не пройдені уроки']
        y_completed = [completed_lessons, total_lessons - completed_lessons]
        plt.bar(x_completed, y_completed, color=colors)
        for i, v in enumerate(y_completed):
            plt.text(x_completed[i], v, str(v), ha='center', va='bottom', fontweight='bold')
        plt.title('Пройдені уроки та ті, що залишились', fontweight=True)

        # Збереження графіків в буфері
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Відправка графіків як фото у відповідь на команду
        bot.send_photo(message.chat.id, photo=buffer)

        # Очищення графіків
        plt.clf()

    except Exception as e:
        error_message = str(e)
        bot.send_message(os.getenv('OWNER_CHAT_ID'), f"Помилка в боті:\n{error_message}")


def progress_lesson_theory_tests_repr_function(message, bot):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()

        user_lesson_items_progress = bot_db.get_user_by_id(chat_id).progress_lessons

        # Отримання загальної кількості уроків з таблиці 'lessons'
        total_lessons = bot_db.get_total_lessons_count()

        # Отримання кількості пройдених уроків користувачем
        completed_lessons = len(user_lesson_items_progress)

        percentage_relation = completed_lessons * 100 / total_lessons
        message_text = f"<b>Ви вивчили {completed_lessons} з {total_lessons} уроків. \n " \
                       f"{percentage_relation}%</b>"

        message_text += f"\nВаш ранг за кількістю вивчених уроків 💭 <b>{bot_db.check_rank(chat_id).upper()}</b>"

        bot.send_message(chat_id, message_text, parse_mode="HTML", reply_markup=create_start_markup())

    except Exception as e:
        error_message = str(e)
        bot.send_message(os.getenv('OWNER_CHAT_ID'), f"Помилка в боті:\n{error_message}")


def user_visual_repr_function(message, bot):
    try:

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
                                  f"{current_user.paid_until if current_user.paid_until else 'the moment of payment'}."
                                  f"\n\n"
                                  f"{message.chat.first_name}, your total score is <b>{current_user.score} pts</b>.\n"
                                  f"You take <b>{user_score_position} place</b> in the overall rating.\n\n"
                                  f"TOP-{counter} 🏆:\n {top_users}", parse_mode="HTML")

    except Exception as e:
        error_message = str(e)
        bot.send_message(os.getenv('OWNER_CHAT_ID'), f"Помилка в боті:\n{error_message}")
