from telebot import types

from Handlers.visual_representation_handler import progress_testing_visual_repr_function, \
    progress_level_visual_repr_function, user_visual_repr_function, progress_theory_tests_repr_function
from database.py_master_bot_database import PyMasterBotDatabase
from Handlers.help_functions import create_yes_or_no_markup, delete_previous_messages, \
    create_start_markup, create_premium_markup, create_tasks_topics_markup, create_lessons_items_markup, \
    create_random_lessons_items_markup, create_learned_lessons_markup, create_lessons_topics_markup
from Handlers.static_variables import premium_options

import random

'''
def process_test_task_level(message, bot):
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
            bot.send_message(chat_id, f"Ви отримаєте можливість проходити тестові завдання рівня <b>'{level_name}'</b> "
                                      f"за умови оплати 👑'Premium' доступу",
                             parse_mode="HTML", reply_markup=create_premium_markup())

    else:
        bot.reply_to(message, "Не знайдено тестових завдань за обраним рівнем.")
        return

'''

def process_lesson_topic(message, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()

    # Get the test_task topic from the user's message
    lesson_topic = message.text.strip()

    if lesson_topic.lower() == "cancel":
        bot.send_message(chat_id, "Cancelled.", reply_markup=create_start_markup())
        return

    elif lesson_topic == "Обрати заняття незалежно від теми":
        bot.send_message(chat_id, "Оберіть заняття: ", reply_markup=create_random_lessons_items_markup(chat_id))
        bot.register_next_step_handler(message, process_lesson_item, bot)

    elif lesson_topic in bot_db.get_lessons_topics():
        bot.send_message(chat_id, "Оберіть заняття: ", reply_markup=create_lessons_items_markup(chat_id, lesson_topic))
        bot.register_next_step_handler(message, process_lesson_item, bot)

    else:
        bot.reply_to(message, "Не знайдено занять за обраною темою.")
        return


def process_lesson_item(message, bot):

    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()
    input_text = message.text.strip()

    if "✅ LEARNED    " in input_text:
        lesson_item = message.text.strip().split("✅ LEARNED    ")[1]
    else:
        lesson_item = input_text

    if lesson_item.lower() == "cancel":
        bot.send_message(chat_id, "Cancelled.", reply_markup=create_start_markup())
        return

    lesson_by_item = bot_db.get_lessons_by_item(lesson_item)
    lesson_id = lesson_by_item.id

    if lesson_by_item:
        bot.send_message(chat_id, lesson_by_item.text, parse_mode="HTML", reply_markup=create_learned_lessons_markup())
        bot.register_next_step_handler(message, handle_answer_lesson, lesson_item, lesson_id, bot)
    else:
        bot.send_message(chat_id, "Не знайдено заняття за обраною темою", reply_markup=create_start_markup())


def handle_answer_lesson(message, lesson_item, lesson_id, bot):

    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()

    if message.text.lower() == "cancel":
        bot.send_message(chat_id, "Cancelled.", reply_markup=create_start_markup())
        return

    elif message.text == "✅ Mark as learned":
        bot_db.add_lesson_to_progress_lesson(chat_id, lesson_id)
        bot.send_message(chat_id, f"Lesson <b>{lesson_item}</b> learned 🎉!",
                         parse_mode="HTML", reply_markup=create_lessons_topics_markup())

    elif message.text == "Return to lesson selection":
        bot.send_message(chat_id, "Choose the topic of the lesson: ",
                         parse_mode="HTML", reply_markup=create_lessons_topics_markup())

    else:
        bot.send_message(chat_id, f"Unrecognized command <b>{message.text}</b>. Cancelled.", parse_mode="HTML")
        return


def handle_yes_or_no_answer(message, level_name, task_topic, bot):
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
