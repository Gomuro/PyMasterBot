"""
This handler adds test_task by level
"""
from database.py_master_bot_database import PyMasterBotDatabase
from Handlers.help_functions import create_levels_markup

def add_easy_test_task_function(bot, message):
    """
    This function adds a test_task to the easy level.
    """
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    # Check if the user is an admin
    if not bot_db.is_admin(user_id):
        bot.send_message(chat_id, "You are not an admin!")
        return

    # Task id definition
    last_number = bot_db.get_test_task_last_id()
    task_id = last_number + 1

    # Ask the user for the test_task topic
    bot.send_message(chat_id, "Enter the test_task topic:")
    bot.register_next_step_handler(message, process_topic, task_id, "easy", bot)  #Pass "easy" as the level argument

def add_middle_test_task_function(bot, message):
    """
        This function adds a test_task to the middle level.
        """
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    # Check if the user is an admin
    if not bot_db.is_admin(user_id):
        bot.send_message(chat_id, "You are not an admin!")
        return

    # Task id definition
    last_number = bot_db.get_test_task_last_id()
    task_id = last_number + 1

    # Ask the user for the test_task topic
    bot.send_message(chat_id, "Enter the test_task topic:")
    bot.register_next_step_handler(message, process_topic, task_id, "middle", bot)  #Pass "middle" as the level argument

def add_hard_test_task_function(bot, message):
    """
        This function adds a test_task to the hard level.
        """
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    # Check if the user is an admin
    if not bot_db.is_admin(user_id):
        bot.send_message(chat_id, "You are not an admin!")
        return

    # Task id definition
    last_number = bot_db.get_test_task_last_id()
    task_id = last_number + 1

    # Ask the user for the test_task topic
    bot.send_message(chat_id, "Enter the test_task topic:")
    bot.register_next_step_handler(message, process_topic, task_id, "hard", bot)  #Pass "hard" as the level argument


def process_topic(message, task_id, level, bot):
    chat_id = message.chat.id
    # Get the test_task topic from the user's message
    topic = message.text

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Ask the user for the test_task description
    bot.send_message(chat_id, "Enter the test_task question:")
    bot.register_next_step_handler(message, process_question, task_id, topic, level, bot)  # Pass the level argument


def process_question(message, task_id, topic, level, bot):
    chat_id = message.chat.id

    # Get the test_task question from the user's message
    question = message.text

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()
    # Checking the existence of a test_task with such a question
    if bot_db.get_test_task_by_question(message.text):
        bot.send_message(chat_id, "This question has already been added.")
        return

    # Ask the user for the first answer option
    bot.send_message(chat_id, "Enter the first answer option:")
    bot.register_next_step_handler(message, process_first_answer, task_id, topic, question, level, bot)


def process_first_answer(message, task_id, topic, question, level, bot):
    chat_id = message.chat.id

    # Get the first_answer text from the user's message
    first_answer = message.text

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Ask the user for the second answer option
    bot.send_message(chat_id, "Enter the second answer option:")
    bot.register_next_step_handler(message, process_second_answer, task_id, topic, question, first_answer, level, bot)


def process_second_answer(message, task_id, topic, question, first_answer, level, bot):
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
    bot.register_next_step_handler(message, process_third_answer, task_id, topic, question,
                                   first_answer, second_answer, level, bot)


def process_third_answer(message, task_id, topic, question, first_answer, second_answer, level, bot):
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
    bot.register_next_step_handler(message, process_right_answer, task_id, topic, question,
                                   first_answer, second_answer, third_answer, level, bot)


def process_right_answer(message, task_id, topic, question, first_answer, second_answer, third_answer, level, bot):
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

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    # Delete a test task with the same number to prevent a conflict
    bot_db.delete_test_task(task_id)

    # Add the test_task to the specified level
    bot_db.add_test_task(task_id, topic, question, first_answer, second_answer,
                         third_answer, right_answer, level)

    bot.send_message(chat_id, f"Test_task added to the easy {level} successfully.")
