from Handlers.exception_handler import handle_exception
from Handlers.help_functions import comment_range_button_markup, create_start_markup
from database.py_master_bot_database import PyMasterBotDatabase


def process_comments(bot, message):
    try:
        if message.text.find("write a comment") != -1:
            process_comments_handler(bot, message)
        if message.text.find("view comments") != -1:
            view_comments(bot, message)

    except Exception as e:
        handle_exception(e, bot)


def process_comments_handler(bot, message):
    try:
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

    except Exception as e:
        handle_exception(e, bot)


def process_name(message, comment_id, name, bot):
    try:

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

    except Exception as e:
        handle_exception(e, bot)


def process_comment(message, comment_id, name, bot):
    try:
        chat_id = message.chat.id
        # Get the comment from the user's message
        comment = message.text

        if message.text == "cancel":
            bot.send_message(chat_id, "Cancelled.")
            return

        # Create an instance of the database
        bot_db = PyMasterBotDatabase()

        if bot_db.get_comment_by_text(comment):
            bot.send_message(chat_id, "Comment with the same text already exists. "
                                      "Please try again with a different comment.")
            return

        # Add the comment to the database with the provided status
        bot_db.add_comment(comment_id, name, comment)

        bot.send_message(chat_id, "Comment added successfully.")

    except Exception as e:
        handle_exception(e, bot)


def view_comments(bot, message):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()
        comments = bot_db.get_all_comments()

        if len(comments) >= 1:
            bot.send_message(chat_id, "View comments:", reply_markup=comment_range_button_markup())
            bot.register_next_step_handler(message, next_comments_markup, bot)
        else:
            bot.send_message(chat_id, "No comments available.")

    except Exception as e:
        handle_exception(e, bot)


def next_comments_markup(message, bot):
    try:

        chat_id = message.chat.id
        bot_db = PyMasterBotDatabase()

        user_name = bot_db.get_user_by_id(message.from_user.id)

        count = getattr(next_comments_markup, 'count', 0) + 1
        setattr(next_comments_markup, 'count', count)

        comments = bot_db.get_all_comments()

        message_text = message.text

        num_comments_per_page = 10

        if message_text == "cancel":
            bot.send_message(chat_id, "Cancelled.", reply_markup=create_start_markup())
            return

        elif message_text == "First and following comments":
            start_index = getattr(next_comments_markup, 'start_index', 0)
            end_index = start_index + num_comments_per_page
            comments_to_display = comments[start_index:end_index]
            all_comments_text = '\n\n'.join(comments_to_display)
            bot.reply_to(message, f"First comments. If there are comments available, "
                                  f"click 'First and following comments' "
                                  f"button again to view them:\n\n{all_comments_text}")

            if end_index >= len(comments):
                bot.send_message(chat_id, "No more comments available.")
                setattr(next_comments_markup, 'count', 0)
                setattr(next_comments_markup, 'start_index', 0)
                view_comments(bot, message)
            else:
                setattr(next_comments_markup, 'start_index', end_index)
                bot.register_next_step_handler(message, next_comments_markup, bot)

            return

        if message_text == "Recent comments":
            start_index = max(0, len(comments) - num_comments_per_page)
            end_index = start_index + num_comments_per_page
            comments_to_display = comments[start_index:end_index]
            all_comments_text = '\n\n'.join(comments_to_display)
            bot.reply_to(message, f"Previous comments:\n\n{all_comments_text}")
            bot.register_next_step_handler(message, next_comments_markup, bot)

            return

        if message_text == "My comments":
            comments_by_user = bot_db.get_own_comments_by_name(user_name)  # Get comments of the specific user

            all_comments_text = '\n\n'.join(comments_by_user)
            bot.send_message(chat_id, f"All your comments:\n\n{all_comments_text}")
        else:
            bot.send_message(chat_id, "You have no comments.")

            return

        bot.register_next_step_handler(message, next_comments_markup, bot)

    except Exception as e:
        handle_exception(e, bot)
