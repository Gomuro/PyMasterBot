from Handlers.exception_handler import handle_exception
from database.py_master_bot_database import PyMasterBotDatabase


def add_admin_function(bot, message):
    try:

        chat_id = message.chat.id
        user_id = message.from_user.id

        # Create an instance of the database
        bot_db = PyMasterBotDatabase()

        # Check if the user is an admin
        if not bot_db.is_admin(user_id):
            # Check if there are any existing admins
            if bot_db.get_admin_count() == 0:
                # There are no existing admins, so add the current user as an admin
                bot_db.add_admin_role(user_id)
                bot.send_message(chat_id, "You have been set as the first admin.")
            else:
                bot.send_message(chat_id, "You are not authorized to perform this action.")
            return

        # Ask the user for the user ID of the admin to be added
        bot.send_message(chat_id, "Enter the user ID of the admin:")
        bot.register_next_step_handler(message, process_admin_id, bot)

    except Exception as e:
        handle_exception(e, bot)


def process_admin_id(message, bot):
    try:

        chat_id = message.chat.id

        # Get the admin user ID from the user's message
        admin_id = message.text

        # Create an instance of the database
        bot_db = PyMasterBotDatabase()

        if not bot_db.check_user_exists(admin_id):
            bot.send_message(chat_id, "User does not exist.")
            return

        # Add the admin role to the user in the database
        bot_db.add_admin_role(admin_id)

        bot.send_message(chat_id, "Admin role added successfully.")

    except Exception as e:
        handle_exception(e, bot)
