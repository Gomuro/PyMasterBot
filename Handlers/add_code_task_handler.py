from database.py_master_bot_database import PyMasterBotDatabase
from Handlers.exception_handler import handle_exception
from Handlers.help_functions import create_levels_markup


def add_code_task_function(bot, message):
    try:

        chat_id = message.chat.id
        user_id = message.from_user.id

        # Create an instance of the database
        bot_db = PyMasterBotDatabase()

        # Check if the user is an admin
        if not bot_db.is_admin(user_id):
            bot.send_message(chat_id, "You are not an admin!")
            return

        # code_task id definition
        last_number = bot_db.get_code_task_last_id()
        code_task_id = last_number + 1

        # Ask the user for the code_task topic
        bot.send_message(chat_id, "Enter the test_task topic:")
        bot.register_next_step_handler(message, process_topic, code_task_id, bot)  # Pass bot as an argument

    except Exception as e:
        handle_exception(e, bot)


def process_topic(message, code_task_id, bot):  # Add bot as a parameter

    try:

        chat_id = message.chat.id
        # Get the code_task topic from the user's message
        topic = message.text

        if message.text == "cancel":
            bot.send_message(chat_id, "Cancelled.")
            return

        # Ask the user for the code_task description
        bot.send_message(chat_id, "Enter the code_task question:")
        bot.register_next_step_handler(message, process_question, code_task_id, topic, bot)  # Use the original_message

    except Exception as e:
        handle_exception(e, bot)


def process_question(message, code_task_id, topic, bot):

    try:

        chat_id = message.chat.id

        # Get the code_task question from the user's message
        question = message.text

        if message.text == "cancel":
            bot.send_message(chat_id, "Cancelled.")
            return

        # Create an instance of the database
        bot_db = PyMasterBotDatabase()
        # Checking the existence of a code_task with such a question
        if bot_db.get_code_task_by_question(message.text):
            bot.send_message(chat_id, "This question has already been added.")
            return

        # Ask the user for the first answer option
        bot.send_message(chat_id, "Enter the first answer option:")
        bot.register_next_step_handler(message, process_first_answer, code_task_id, topic, question, bot)

    except Exception as e:
        handle_exception(e, bot)


def process_first_answer(message, code_task_id, topic, question, bot):

    try:
        chat_id = message.chat.id

        # Get the first_answer text from the user's message
        first_answer = message.text

        if message.text == "cancel":
            bot.send_message(chat_id, "Cancelled.")
            return

        # Ask the user for the second answer option
        bot.send_message(chat_id, "Enter the second answer option:")
        bot.register_next_step_handler(message, process_second_answer, code_task_id, topic, question, first_answer, bot)

    except Exception as e:
        handle_exception(e, bot)


def process_second_answer(message, code_task_id, topic, question, first_answer, bot):

    try:
        chat_id = message.chat.id

        # Get the second_answer text from the user's message
        second_answer = message.text

        if message.text == "cancel":
            bot.send_message(chat_id, "Cancelled.")
            return

        if second_answer == first_answer:
            bot.send_message(chat_id, "The same answers are entered. Cancelled.")
            return

        # Ask the user for the third answer option
        bot.send_message(chat_id, "Enter the third answer option:")
        bot.register_next_step_handler(message, process_third_answer, code_task_id, topic, question,
                                       first_answer, second_answer, bot)

    except Exception as e:
        handle_exception(e, bot)


def process_third_answer(message, code_task_id, topic, question, first_answer, second_answer, bot):

    try:

        chat_id = message.chat.id

        # Get the third_answer text from the user's message
        third_answer = message.text

        if message.text == "cancel":
            bot.send_message(chat_id, "Cancelled.")
            return

        if third_answer in (first_answer, second_answer):
            bot.send_message(chat_id, "The same answers are entered. Cancelled.")
            return

        # Ask the user for the right answer
        bot.send_message(chat_id, "Enter the right answer:")
        bot.register_next_step_handler(message, process_right_answer, code_task_id, topic, question,
                                       first_answer, second_answer, third_answer, bot)

    except Exception as e:
        handle_exception(e, bot)


def process_right_answer(message, code_task_id, topic, question, first_answer, second_answer, third_answer, bot):

    try:

        chat_id = message.chat.id

        # Get the right_answer text from the user's message
        right_answer = message.text

        if message.text == "cancel":
            bot.send_message(chat_id, "Cancelled.")
            return

        # Check if the provided right_answer is valid
        if right_answer not in [first_answer, second_answer, third_answer]:
            bot.send_message(chat_id, f"There is no such answer option among the given ones.\nCancelled.")
            return

        # Ask the user for the level of code_task complexity
        bot.send_message(chat_id, "Choose the level of code task complexity\n"
                                  "or write 'cancel' to cancel the task addition:",
                         reply_markup=create_levels_markup())

        bot.register_next_step_handler(message, process_level_relation, code_task_id, topic, question,
                                       first_answer, second_answer, third_answer, right_answer, bot)

    except Exception as e:
        handle_exception(e, bot)


def process_level_relation(message, code_task_id, topic, question, first_answer, second_answer, third_answer,
                           right_answer, bot):

    try:

        chat_id = message.chat.id

        # Get the level of code_task complexity from the user's message
        level_relation = message.text

        if message.text == "cancel":
            bot.send_message(chat_id, "Cancelled.")
            return

        # Create an instance of the database
        bot_db = PyMasterBotDatabase()

        # Delete a code task with the same number to prevent a conflict
        bot_db.delete_test_task(code_task_id)

        # Add the test_task to the database with the provided status
        bot_db.add_code_task(code_task_id, topic, question, first_answer, second_answer,
                             third_answer, right_answer, level_relation)

        bot.send_message(chat_id, "Code_task added successfully.")

    except Exception as e:
        handle_exception(e, bot)
