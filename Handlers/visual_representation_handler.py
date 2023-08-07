import matplotlib.pyplot as plt

from io import BytesIO

from Handlers.exception_handler import handle_exception
from Handlers.help_functions import create_start_markup
from database.py_master_bot_database import PyMasterBotDatabase


def progress_testing_visual_repr_function(message, bot):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()

        user_testing_progress = bot_db.get_user_by_id(chat_id).progress_testing

        # Setting up schedule options
        colors = ['green', 'orange', 'red']

        # Create a new shape with a colored background
        plt.figure(facecolor='pink')

        # Creating a schedule
        x = [key for key in user_testing_progress.keys()]
        y = [len(value) for value in user_testing_progress.values()]

        plt.bar(x, y, color=colors)

        # Displaying only integers on the y-axis
        plt.yticks(range(0, int(max(y)) + 2, 2))

        # Add value labels to columns
        for i, v in enumerate(y):
            plt.text(x[i], v, str(v), ha='center', va='top', fontweight='bold')

        # Customize the axis title and labels
        plt.title('Number of successfully passed tests (THEORY) by levels', fontweight=True)
        plt.xlabel('Level name')
        plt.ylabel('Number of tests')

        # Saving a graph to a buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Send a graph as a photo in response to a command
        bot.send_photo(message.chat.id, photo=buffer)

        # Cleaning up the schedule
        plt.clf()

    except Exception as e:
        handle_exception(e, bot)


def progress_level_visual_repr_function(message, bot):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()

        # Database with difficulty levels and values
        user_testing_progress = bot_db.get_user_by_id(chat_id).progress_testing

        max_value = 20

        # Setting up schedule options
        colors = ['green', 'orange', 'red', 'bisque']

        # Create a new shape with a colored background
        plt.subplots(facecolor='lightblue')

        # Creating sub-graphs
        fig, axes = plt.subplots(1, 3, figsize=(10, 4), facecolor='lightblue')

        # Building pie charts for each level of complexity
        for i, (level, values) in enumerate(user_testing_progress.items()):
            ax = axes[i]  # Getting an active subgraph
            completed_tasks = len(values)
            remaining_tasks = max_value - completed_tasks
            sizes = [completed_tasks, (remaining_tasks if remaining_tasks > 0 else 0)]

            explode = [0.1] + [0] * (len(sizes) - 1)  # Highlighting the first segment

            def form_labels():
                if completed_tasks == 0:
                    return f'No\ncompleted\ntasks\nof the\n{level}\nlevel', ''
                elif completed_tasks < max_value:
                    return f'{level} ({completed_tasks}/{max_value})', ''
                else:
                    return f'{level} ({completed_tasks}/{max_value})', f'\n\n\n\n\n\n\n\n\n' \
                                                                       f'Completed\nenough\ntasks\nof the\n' \
                                                                       f'{level}\nlevel'

            ax.pie(sizes, labels=form_labels(), colors=(colors[i], colors[-1]), explode=explode, autopct='%1.1f%%')
            ax.set_title(level.capitalize(), fontsize=17)
            ax.tick_params(labelsize=16)  # Font size of captions

        # General title
        fig.suptitle('Testing progress (THEORY) by difficulty levels', fontsize=18)

        # Saving a graph to a buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Send a graph as a photo in response to a command
        bot.send_photo(message.chat.id, photo=buffer)

        # Cleaning up the schedule
        plt.clf()

    except Exception as e:
        handle_exception(e, bot)


def progress_theory_tests_repr_function(message, bot):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()

        user_testing_progress = bot_db.get_user_by_id(chat_id).progress_testing

        total_value = sum(len(value) for value in user_testing_progress.values())

        message_text = f"<b>You have succeeded in completing {total_value} tasks. </b>"

        if total_value != 0:
            message_text += " Among them:\n"
            for key, value in user_testing_progress.items():
                message_text += f"at the {key} level: {len(value)},    " \
                                f"{'{:.2f}%'.format(len(value) / total_value * 100)}\n"

        message_text += f"\nYour rank by the number of completed THEORY tests 💭 " \
                        f"<b>{bot_db.check_rank(chat_id).upper()}</b>"

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
