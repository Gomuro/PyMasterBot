"""
This block contains helper functions that will be used in various handlers
"""


def delete_previous_messages(message, telebot_instance):
    """This function helps to delete previous messages in order to prevent the bot
    from getting cluttered with unnecessary messages"""
    try:
        if telebot_instance:
            for index in range(1, 3):
                telebot_instance.delete_message(message.chat.id, message.message_id - index)

    except Exception as e:
        print("An unexpected error occurred:", e)



