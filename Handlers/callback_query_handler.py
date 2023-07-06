"""This module allows using callback_query with pressing designated inline keyboard buttons"""
from Handlers.help_functions import create_levels_markup, comment_markup


def callback_query_handler(call, telebot_instance, inline_keyboard, reply_keyboard):
    """This method allows sending a designated message when the button is pressed"""

    telebot_instance.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == '/check_code':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Send the code you want to check.",
                                      reply_markup=inline_keyboard.get_keyboard())

    elif call.data == '/documentation':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Enter the name of the module, function, or class: ",
                                      reply_markup=inline_keyboard.get_keyboard())

    elif call.data == '/testing':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Choose the level of test complexity: ",
                                      reply_markup=create_levels_markup())

    elif call.data == '/comments':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Want to write a comment or view comments?: ",
                                      reply_markup=comment_markup())

    # Handle the "HELP" button separately
    elif call.data == '/help':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text=f"Enter your question or\n"
                                           "click <b>'Go to Python site'</b> button to visit the site",
                                      parse_mode="HTML",
                                      reply_markup=reply_keyboard.get_keyboard())

    else:
        telebot_instance.answer_callback_query(callback_query_id=call.id,
                                               text="This command does not exist!")
