from Handlers.help_functions import comment_range_button_markup
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
    user = bot_db.get_user_by_id(message.from_user.id)

    if user:
        name = user.name
        process_name(message, comment_id, name, bot)
    else:
        name = None
        bot.send_message(chat_id, "Enter your name:")
        bot.register_next_step_handler(message, process_name, comment_id, name, bot)  # Pass bot as an argument


def process_name(message, comment_id, name, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()
    user = bot_db.get_user_by_id(message.from_user.id)
    name = user.name

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return
    if name is None:
        name = message.text  # Assign the entered name to the variable

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

    if bot_db.get_comment_by_text(comment):
        bot.send_message(chat_id, "Comment with the same text already exists. Please try again with a different comment.")
        return

    # Add the comment to the database with the provided status
    bot_db.add_comment(comment_id, name, comment)

    bot.send_message(chat_id, "Comment added successfully.")


def view_comments(bot, message):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()
    comments = bot_db.get_all_comments()

    if len(comments) > 10:
        comments_to_display = comments[:10]  # Вибрати перші 10 коментарів
        all_comments_text = '\n\n'.join(comments_to_display)
        bot.send_message(chat_id, "First or Last 10 comments: \n\n", reply_markup=comment_range_button_markup())
    elif len(comments) > 0:
        comments_to_display = comments
        all_comments_text = '\n\n'.join(comments_to_display)
        bot.send_message(chat_id, "Comments: \n\n" + all_comments_text)
    else:
        bot.send_message(chat_id, "No comments available.")

    bot.register_next_step_handler(message, comment_range_markup, bot)
    return


def comment_range_markup(message, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()
    comments = bot_db.get_all_comments()
    message_text = message.text

    num_comments_per_page = 10
    start_index = 0
    end_index = start_index + num_comments_per_page

    if len(comments) > num_comments_per_page:
        if message_text == "Наступні 10":
            start_index += num_comments_per_page
            end_index += num_comments_per_page
            comments_to_display = comments[0:10]
            all_comments_text = '\n\n'.join(comments_to_display)
            bot.reply_to(message, f"prev_comments_'\n\n'{all_comments_text}")

        elif message_text == "Останні 10":
            start_index = max(0, len(comments) - num_comments_per_page)
            end_index = start_index + num_comments_per_page
            comments_to_display = comments[start_index:end_index]
            all_comments_text = '\n\n'.join(comments_to_display)
            bot.reply_to(message, f"prev_comments_'\n\n'{all_comments_text}")
    else:
        bot.send_message(chat_id, "No more comments available.")

    bot.send_message(chat_id, "First or Last 10 comments: \n\n", reply_markup=comment_range_button_markup())
