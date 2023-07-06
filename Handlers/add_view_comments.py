from database.py_master_bot_database import PyMasterBotDatabase


def process_comments(bot, message):
    if message.text.find("write a comment") != -1:
        process_comments_handler(bot, message)
    if message.text.find("view comments") != -1:
        view_comments(bot, message)


def process_comments_handler(bot, message):
    chat_id = message.chat.id

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    # comment id definition
    last_number = bot_db.get_comment_last_id()
    comment_id = last_number + 1

    bot.send_message(chat_id, "Enter your name:")
    bot.register_next_step_handler(message, process_name, comment_id, bot)  # Pass bot as an argument

def process_name(message, comment_id, bot):
    chat_id = message.chat.id
    # Get the name from the user's message
    name = message.text

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Ask the user for the comment
    bot.send_message(chat_id, "Enter the comment:")
    bot.register_next_step_handler(message, process_comment, comment_id, name, bot)  # Use the original_message


def process_comment(message, comment_id, name, bot):
    chat_id = message.chat.id
    # Get the comment from the user's message
    comment = message.text

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    # Delete a comment with the same number to prevent a conflict
    bot_db.delete_comment(comment_id)

    # Add the comment to the database with the provided status
    bot_db.add_comment(comment_id, name, comment)

    bot.send_message(chat_id, "Comment added successfully.")



def view_comments(bot, message):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()
    comments = bot_db.get_all_comments()
    all_comments_text = '\n\n'.join(comments)
    bot.send_message(chat_id, "All comments: \n\n" + all_comments_text)

    return
