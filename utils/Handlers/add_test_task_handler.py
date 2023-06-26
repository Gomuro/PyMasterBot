from telebot import types

from database.py_master_bot_database import PyMasterBotDatabase


def add_test_task_function(bot, message):
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
    bot.register_next_step_handler(message, process_topic, task_id, bot)  # Pass bot as an argument


def process_topic(message, task_id, bot):  # Add bot as a parameter
    chat_id = message.chat.id
    # Get the test_task topic from the user's message
    topic = message.text

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Ask the user for the test_task description
    bot.send_message(chat_id, "Enter the test_task question:")
    bot.register_next_step_handler(message, process_question, task_id, topic, bot)  # Use the original_message


def process_question(message, task_id, topic, bot):
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
    bot.register_next_step_handler(message, process_first_answer, task_id, topic, question, bot)


def process_first_answer(message, task_id, topic, question, bot):
    chat_id = message.chat.id

    # Get the first_answer text from the user's message
    first_answer = message.text

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Ask the user for the second answer option
    bot.send_message(chat_id, "Enter the second answer option:")
    bot.register_next_step_handler(message, process_second_answer, task_id, topic, question, first_answer, bot)


def process_second_answer(message, task_id, topic, question, first_answer, bot):
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
    bot.register_next_step_handler(message, process_third_answer, task_id, topic, question, first_answer, second_answer, bot)


def process_third_answer(message, task_id, topic, question, first_answer, second_answer, bot):
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
                                   first_answer, second_answer, third_answer, bot)


def process_right_answer(message, task_id, topic, question, first_answer, second_answer, third_answer, bot):
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
    levels = bot_db.get_all_levels()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for level in levels:
        btn = types.KeyboardButton(f"{level}")
        markup.add(btn)

    # Ask the user for the level of task complexity
    bot.send_message(chat_id, "Choose the level of task complexity\n"
                              "or write 'cancel' to cancel the task addition:",
                     reply_markup=markup)

    bot.register_next_step_handler(message, process_level_relation, task_id, topic, question,
                                   first_answer, second_answer, third_answer, right_answer, bot)


def process_level_relation(message, task_id, topic, question, first_answer, second_answer, third_answer,
                           right_answer, bot):
    chat_id = message.chat.id

    # Get the level of task complexity from the user's message
    level_relation = message.text

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    # Delete a test task with the same number to prevent a conflict
    bot_db.delete_test_task(task_id)

    # Add the test_task to the database with the provided status
    bot_db.add_test_task(task_id, topic, question, first_answer, second_answer,
                         third_answer, right_answer, level_relation)

    bot.send_message(chat_id, "Test_task added successfully.")
