from database.py_master_bot_database import PyMasterBotDatabase


def add_lesson_function(bot, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    # Check if the user is an admin
    if not bot_db.is_admin(user_id):
        bot.send_message(chat_id, "You are not an admin!")
        return

    # Ask the user for the lesson topic
    bot.send_message(chat_id, "Enter the lesson topic:")
    bot.register_next_step_handler(message, process_topic, bot)  # Pass bot as an argument


def process_topic(message, bot):  # Add bot as a parameter
    topic = message.text
    bot_db = PyMasterBotDatabase()
    chat_id = message.chat.id
    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Get the lesson topic from the user's message

    if bot_db.get_lessons_by_topic(message.text):
        bot.send_message(chat_id, "This topic has already been added.")
        return
    # Ask the user for the lesson description
    bot.send_message(chat_id, "Enter the lesson description:")
    bot.register_next_step_handler(message, process_description, topic, bot)  # Use the original_message


def process_description(message, topic, bot):
    chat_id = message.chat.id

    # Get the lesson description from the user's message
    description = message.text
    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return
    # Ask the user for the lesson text
    bot.send_message(chat_id, "Enter the lesson text:")
    bot.register_next_step_handler(message, process_text, topic, description, bot)


def process_text(message, topic, description, bot):
    chat_id = message.chat.id

    # Get the text from the user's message
    text = message.text

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Ask the user for the lesson status
    bot.send_message(chat_id, "Enter the lesson status (free/paid/bonus):")
    bot.register_next_step_handler(message, process_status, topic, description, text, bot)


def process_status(message, topic, description, text, bot):
    chat_id = message.chat.id

    # Get the lesson status from the user's message
    status = message.text.lower()

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Check if the provided status is valid
    if status not in ["free", "paid", "bonus"]:
        bot.send_message(chat_id, "Invalid status. Please enter either 'free', 'paid', or 'bonus'.")
        return

    # Add the lesson to the database with the provided status
    bot_db.add_lesson(topic, description, text, status)

    bot.send_message(chat_id, "Lesson added successfully.")
