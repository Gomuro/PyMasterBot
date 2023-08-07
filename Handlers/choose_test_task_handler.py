import html
from telebot import types

from Handlers.exception_handler import handle_exception
from Handlers.visual_representation_handler import progress_testing_visual_repr_function, \
    progress_level_visual_repr_function, user_visual_repr_function, progress_theory_tests_repr_function
from database.py_master_bot_database import PyMasterBotDatabase
from Handlers.help_functions import create_yes_or_no_markup, delete_previous_messages, \
    create_start_markup, create_premium_markup, create_tasks_topics_markup
from Handlers.static_variables import premium_options

import random


def process_test_task_level(message, bot):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()
        level_name = message.text.strip()

        if bot_db.check_this_level_task_exists(level_name=level_name):
            message_text = f"Select a test topic of level <b>'{level_name}'</b>" \
                           f"or click the button <b>'Cancel'</b> to exit.\n\n" \
                           f"If only option 'Cancel' is available - congratulations - " \
                           f"you have passed all <b>{level_name}</b> level tests!"

            if level_name not in premium_options:
                bot.send_message(chat_id, message_text, parse_mode="HTML",
                                 reply_markup=create_tasks_topics_markup(chat_id, level_name))
                bot.register_next_step_handler(message, process_task_topic, level_name, bot)  # Pass bot as an argument
            elif level_name in premium_options and bot_db.check_status_premium(user_id=chat_id):
                bot.send_message(chat_id, message_text, parse_mode="HTML",
                                 reply_markup=create_tasks_topics_markup(chat_id, level_name))
                bot.register_next_step_handler(message, process_task_topic, level_name, bot)  # Pass bot as an argument
            elif level_name in premium_options and not bot_db.check_status_premium(user_id=chat_id):
                bot.send_message(chat_id, f"You will have the opportunity to take test tasks of the level "
                                          f"<b>'{level_name}'</b> "
                                          f"if you'll get 👑'Premium' access",
                                 parse_mode="HTML", reply_markup=create_premium_markup())

        else:
            bot.reply_to(message, "No tests found at the selected level.")
            return

    except Exception as e:
        handle_exception(e, bot)


def process_task_topic(message, level_name, bot):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()

        # Get the test_task topic from the user's message
        task_topic = message.text.strip()

        if task_topic.lower() == "cancel":
            bot.send_message(chat_id, "Cancelled.", reply_markup=create_start_markup())
            return

        elif task_topic in bot_db.get_test_tasks_topics_by_level(level_name) or \
                task_topic == "Choose tasks on any topic":
            choose_test_task_function(message, level_name, task_topic, bot)

        else:
            bot.reply_to(message, "No test tasks were found for the selected topic")
            return

    except Exception as e:
        handle_exception(e, bot)


def choose_test_task_function(message, level_name, task_topic, bot):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()

        def tasks_by_topic(level, topic_task):
            if task_topic == "Choose tasks on any topic":
                test_tasks_by_level_and_topic = bot_db.get_test_tasks_by_level(level)
            else:
                test_tasks_by_level_and_topic = bot_db.get_test_tasks_by_level_and_topic(level, topic_task)
            return test_tasks_by_level_and_topic

        # create a set of tasks of a certain level on the specified topic
        test_tasks_id = set(task.id for task in tasks_by_topic(level_name, task_topic))

        # create a set of tasks of a certain level on the specified topic that the user has already completed
        user_testing_progress = bot_db.get_user_by_id(chat_id).progress_testing
        tests_done_by_user = set(value for value in user_testing_progress[level_name])

        # create a list of tasks of a certain level on the specified topic that the user has not yet done
        test_tasks_id = list(test_tasks_id.difference(tests_done_by_user))

        if len(test_tasks_id) == 0:
            bot.send_message(chat_id, f"You have already passed all tests of <b>'{level_name}'</b> level "
                                      f"on the topic <b>'{task_topic}'</b>.",
                             parse_mode="HTML", reply_markup=create_start_markup())

        else:
            # Shuffle the list of test tasks
            random.shuffle(test_tasks_id)

            test_task = bot_db.get_test_task_by_id(test_tasks_id[0])

            task_id = test_task.id
            topic = test_task.topic
            question = test_task.question
            var1 = test_task.var1
            var2 = test_task.var2
            var3 = test_task.var3
            right_answer = test_task.right_answer

            response = f"({topic})\n{question}\n\n1. {var1}\n2. {var2}\n3. {var3}"
            bot.send_message(chat_id, response)

            var1 = html.unescape(var1)
            var2 = html.unescape(var2)
            var3 = html.unescape(var3)
            right_answer = html.unescape(right_answer)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn_var1 = types.KeyboardButton(var1)
            btn_var2 = types.KeyboardButton(var2)
            btn_var3 = types.KeyboardButton(var3)
            markup.add(btn_var1, btn_var2, btn_var3)

            bot.send_message(chat_id, f"Choose the right answer\n", reply_markup=markup)
            bot.register_next_step_handler(message, handle_answer, task_id, right_answer, level_name, task_topic, bot)

    except Exception as e:
        handle_exception(e, bot)


def handle_answer(message, task_id, right_answer, level_name, task_topic, bot):
    try:

        chat_id = message.chat.id

        count = getattr(handle_answer, 'count', 0) + 1  # Get counter value or set to 0
        setattr(handle_answer, 'count', count)  # Save counter value

        if message.text == "cancel":
            bot.send_message(chat_id, "Cancelled.")
            return

        elif message.text == right_answer:
            bot_db = PyMasterBotDatabase()
            bot_db.add_task_to_progress_testing(chat_id, task_id, level_name)
            points = 0
            if level_name == "easy":
                points += 1
            elif level_name == "middle":
                points += 5
            elif level_name == "hard":
                points += 10
            bot_db.add_points(user_id=chat_id, points=points)

            bot.reply_to(message, "You're right!")

        else:
            bot.reply_to(message, f"Wrong answer!\n\nThe right answer is\n'{right_answer}'")

        if count < 1:
            choose_test_task_function(message, level_name, task_topic, bot)
        else:
            setattr(handle_answer, 'count', 0)
            bot.send_message(chat_id, f"Continue testing by level <b>'{level_name}'</b>?\nSelect:",
                             parse_mode="HTML", reply_markup=create_yes_or_no_markup())
            bot.register_next_step_handler(message, handle_yes_or_no_answer, level_name, task_topic, bot)

    except Exception as e:
        handle_exception(e, bot)


def handle_yes_or_no_answer(message, level_name, task_topic, bot):
    try:

        delete_previous_messages(message=message, telebot_instance=bot)
        chat_id = message.chat.id

        if message.text in ("no", "cancel"):
            bot.send_message(chat_id, "Cancelled.")

            user_visual_repr_function(message, bot)
            progress_level_visual_repr_function(message, bot)
            progress_testing_visual_repr_function(message, bot)
            progress_theory_tests_repr_function(message, bot)

            return

        elif message.text == "yes":
            # Continue testing by level
            choose_test_task_function(message, level_name, task_topic, bot)

        else:
            bot.send_message(chat_id, f"Unrecognized command <b>{message.text}</b>. Cancelled.", parse_mode="HTML")
            return

    except Exception as e:
        handle_exception(e, bot)
