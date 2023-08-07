from Handlers.exception_handler import handle_exception
from Handlers.help_functions import create_start_markup
from database.py_master_bot_database import PyMasterBotDatabase

import matplotlib.pyplot as plt
from io import BytesIO


def progress_lesson_visual_round_repr_function(message, bot):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()

        user_lesson_items_progress = bot_db.get_user_by_id(chat_id).progress_lessons

        # Get the total number of lessons from the 'lessons' table
        total_lessons = bot_db.get_total_lessons_count()

        # Get the number of lessons completed by the user
        completed_lessons = len(user_lesson_items_progress)

        # Setting up schedule options
        colors = ['yellow', 'purple']

        # Create a new shape with a colored background
        plt.figure(facecolor='lightblue')

        # Create the first schedule (total number of lessons)
        plt.subplot(1, 2, 1)
        x_total = ['Learned', '']
        y_total = [completed_lessons, total_lessons - completed_lessons]
        explode = [0.1, 0]  # Add an explode effect to the first slice
        plt.pie(y_total, labels=x_total, colors=colors, autopct='%1.0f%%', startangle=140, explode=explode)
        plt.title('Percentage of learned lessons', fontweight=True)

        # Create a second graph (number of lessons completed)
        plt.subplot(1, 2, 2)
        x_completed = ['Learned', 'Unlearned lessons']
        y_completed = [completed_lessons, total_lessons - completed_lessons]
        plt.bar(x_completed, y_completed, color=colors)

        for i, v in enumerate(y_completed):
            plt.text(x_completed[i], v, str(v), ha='center', va='bottom', fontweight='bold')
        plt.title('Lessons learned and those\nthat remain to be learned', fontweight=True)

        # Saving graphs to the buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Send graphs as photos in response to a command
        bot.send_photo(message.chat.id, photo=buffer)

        # Clean up schedules
        plt.clf()

    except Exception as e:
        handle_exception(e, bot)


def progress_lesson_theory_tests_repr_function(message, bot):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()

        user_lesson_items_progress = bot_db.get_user_by_id(chat_id).progress_lessons

        # Getting the total number of lessons from the 'lessons' table
        total_lessons = bot_db.get_total_lessons_count()

        # Get the number of lessons completed by the user
        completed_lessons = len(user_lesson_items_progress)

        percentage_relation = completed_lessons * 100 / total_lessons
        message_text = f"<b>You have learned {completed_lessons} from {total_lessons} lessons. \n " \
                       f"{percentage_relation}%</b>"

        message_text += f"\nYour rank by the number of learned lessons 💭 <b>{bot_db.check_rank(chat_id).upper()}</b>"

        bot.send_message(chat_id, message_text, parse_mode="HTML", reply_markup=create_start_markup())

    except Exception as e:
        handle_exception(e, bot)


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
        handle_exception(e, bot)
