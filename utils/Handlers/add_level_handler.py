from database.py_master_bot_database import PyMasterBotDatabase
from utils.Handlers.static_variables import static_levels


def add_static_levels_function():
    bot_db = PyMasterBotDatabase()

    # Checking if levels exist
    if bot_db.check_levels_exist():
        return

    for level in static_levels:
        bot_db.add_level(level_name=level)


def add_level_function(bot, message):
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


def process_level_name(message, bot):  # Add bot as a parameter
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

    # Add the lesson to the database with the provided status
    bot_db.add_level(level_name=level_name)

    bot.send_message(chat_id, "Level added successfully.")
