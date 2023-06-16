"""
This block contains helper functions that will be used in various handlers
"""


def delete_previous_messages(message, telebot_instance):
    """This function helps to delete previous message in order to prevent the bot from getting cluttered
    with unnecessary messages

    :param message: This is an object that represents the incoming message that the bot interacts with.
    :param telebot_instance: This is an object that represents your Telegram bot, created using the TeleBot class.
    :return: If the operation is successful, the function does not return a value. If an unexpected error occurs while
        deleting a message, an error message is printed using the print() function.
    """

    try:
        if telebot_instance:
            telebot_instance.delete_message(message.chat.id, message.message_id - 1)
    except Exception as e:
        print("An unexpected error occurred:", e)
