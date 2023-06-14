"""
This block contains helper functions that will be used in various handlers
"""


def delete_previous_messages(message, telebot_instance):
    """This function helps to delete previous messages in order to prevent the bot
    from getting cluttered with unnecessary messages"""
    try:
        if telebot_instance:
            telebot_instance.delete_message(message.chat.id, message.message_id - 1)
    except Exception as e:
        print("An unexpected error occurred:", e)



