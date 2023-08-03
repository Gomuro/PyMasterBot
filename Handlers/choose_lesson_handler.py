import os

from Handlers.visual_lesson_representation_handler import progress_lesson_visual_round_repr_function, \
    progress_lesson_theory_tests_repr_function
from Handlers.visual_representation_handler import user_visual_repr_function
from database.py_master_bot_database import PyMasterBotDatabase
from Handlers.help_functions import create_start_markup, create_lessons_items_markup, \
    create_random_lessons_items_markup, create_learned_lessons_markup, create_lessons_topics_markup


def process_lesson_topic(message, bot):
    try:
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
            bot.send_message(chat_id, "Оберіть заняття: ", reply_markup=create_lessons_items_markup(chat_id,
                                                                                                    lesson_topic))
            bot.register_next_step_handler(message, process_lesson_item, bot)

        else:
            bot.reply_to(message, "Не знайдено занять за обраною темою.")
            return

    except Exception as e:
        error_message = str(e)
        bot.send_message(os.getenv('OWNER_CHAT_ID'), f"Помилка в боті:\n{error_message}")


def process_lesson_item(message, bot):

    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()
        input_text = message.text.strip()

        if input_text.lower() == "cancel":
            bot.send_message(chat_id, "Cancelled.", reply_markup=create_start_markup())
            return

        if "✅ LEARNED    " in input_text:
            lesson_item = input_text.split("✅ LEARNED    ")[1]
        else:
            lesson_item = input_text.split(f". ")[1].strip()

        lesson_by_item = bot_db.get_lessons_by_item(lesson_item)
        lesson_id = lesson_by_item.id

        if lesson_by_item:
            bot.send_message(chat_id, lesson_by_item.text, parse_mode="HTML",
                             reply_markup=create_learned_lessons_markup())
            bot.register_next_step_handler(message, handle_answer_lesson, lesson_item, lesson_id, bot)
        else:
            bot.send_message(chat_id, "Не знайдено заняття за обраною темою", reply_markup=create_start_markup())

    except Exception as e:
        error_message = str(e)
        bot.send_message(os.getenv('OWNER_CHAT_ID'), f"Помилка в боті:\n{error_message}")


def handle_answer_lesson(message, lesson_item, lesson_id, bot):

    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()

        if message.text.lower() == "cancel":
            bot.send_message(chat_id, "Cancelled.", reply_markup=create_start_markup())
            user_visual_repr_function(message, bot)
            progress_lesson_visual_round_repr_function(message, bot)
            progress_lesson_theory_tests_repr_function(message, bot)
            return

        elif message.text == "✅ Mark as learned":
            bot_db.add_lesson_to_progress_lesson(chat_id, lesson_id)
            bot.send_message(chat_id, f"Lesson <b>{lesson_item}</b> learned 🎉!",
                             parse_mode="HTML", reply_markup=create_lessons_topics_markup())

            user_visual_repr_function(message, bot)
            progress_lesson_visual_round_repr_function(message, bot)
            progress_lesson_theory_tests_repr_function(message, bot)
            # bot.send_message(chat_id, "", reply_markup=create_start_markup())

        elif message.text == "Return to lesson selection":
            bot.send_message(chat_id, "Choose the topic of the lesson: ",
                             parse_mode="HTML", reply_markup=create_lessons_topics_markup())

        else:
            bot.send_message(chat_id, f"Unrecognized command <b>{message.text}</b>. Cancelled.",
                             parse_mode="HTML", reply_markup=create_start_markup())
            return

    except Exception as e:
        error_message = str(e)
        bot.send_message(os.getenv('OWNER_CHAT_ID'), f"Помилка в боті:\n{error_message}")
