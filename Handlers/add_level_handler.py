from Handlers.exception_handler import handle_exception
from database.py_master_bot_database import PyMasterBotDatabase


def add_level_function(bot, message):
    try:

        chat_id = message.chat.id
        user_id = message.from_user.id

        # Create an instance of the database
        bot_db = PyMasterBotDatabase()

        # Check if the user is an admin
        if not bot_db.is_admin(user_id):
            bot.send_message(chat_id, "You are not an admin!")
            return

        # Ask the user for a name of the level
        bot.send_message(chat_id, "Enter a name for the level:")
        bot.register_next_step_handler(message, process_level_name, bot)  # Pass bot as an argument

    except Exception as e:
        handle_exception(e, bot)


def process_level_name(message, bot):  # Add bot as a parameter

    try:

        chat_id = message.chat.id
        # Get a name of the level from the user's message
        level_name = message.text

        if message.text == "cancel":
            bot.send_message(chat_id, "Cancelled.")
            return

        # Create an instance of the database
        bot_db = PyMasterBotDatabase()

        # Check if a level with this name already exists
        if bot_db.get_level_by_name(message.text):
            bot.send_message(chat_id, "This level already exists.")
            return

        # Level id definition
        level_id = bot_db.get_level_last_id() + 1

        # Add the level to the database
        bot_db.add_level(level_id=level_id, level_name=level_name)

        bot.send_message(chat_id, "Level added successfully.")

    except Exception as e:
        handle_exception(e, bot)
