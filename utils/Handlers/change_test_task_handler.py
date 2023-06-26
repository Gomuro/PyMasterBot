from telebot import types

from database.py_master_bot_database import PyMasterBotDatabase

from utils.Handlers.add_test_task_handler import process_topic


def change_test_task_function(bot, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    # Check if the user is an admin
    if not bot_db.is_admin(user_id):
        bot.send_message(chat_id, "You are not an admin!")
        return

    # Ask the user for the test_task ID
    bot.send_message(chat_id, f"Enter the <b>ID</b> number of the task you want to change:", parse_mode="HTML")
    bot.register_next_step_handler(message, process_test_task_id, bot)  # Pass bot as an argument


def process_test_task_id(message, bot):  # Add bot as a parameter
    chat_id = message.chat.id
    # Get the test_task ID from the user's message
    task_id = message.text

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    if not bot_db.get_test_task_by_id(task_id):
        bot.send_message(chat_id, f"Could not find the question with {task_id} ID. Cancelled")
        print(f"An error occurred while searching for a test task by ID {task_id}:")
        return

    # Check whether the user-entered test_task ID is in the database
    test_task = bot_db.get_test_task_by_id(task_id)

    # Create a keyboard with a selection of options 'yes' or 'no'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_yes = types.KeyboardButton("yes")
    btn_no = types.KeyboardButton("no")
    markup.add(btn_yes, btn_no)

    bot.send_message(chat_id, f"Do you really want to change the test task\n"
                              f"'{test_task.question}'\n\n of the level '{test_task.level_relation}'?",
                     reply_markup=markup)

    bot.register_next_step_handler(message, process_yes_or_no_answer, task_id, bot)  # Use the original_message


def process_yes_or_no_answer(message, task_id, bot):
    chat_id = message.chat.id

    if message.text in ("no", "cancel"):
        bot.send_message(chat_id, "Cancelled.")
        return

    elif message.text == "yes":
        # Ask the user for the test_task topic
        bot.send_message(chat_id, "Enter the test_task topic:")
        bot.register_next_step_handler(message, process_topic, task_id, bot)  # Pass bot as an argument

    else:
        bot.send_message(chat_id, f"Unrecognized command <b>{message.text}</b>. Cancelled.", parse_mode="HTML")
        return
