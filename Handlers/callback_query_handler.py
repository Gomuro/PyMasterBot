"""This module allows using callback_query with pressing designated inline keyboard buttons"""
from Handlers.help_functions import create_levels_markup, create_premium_markup, comment_markup, \
    create_account_markup, create_lessons_topics_markup
from Handlers.visual_representation_handler import user_visual_repr_function


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

    elif call.data == '/lesson':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Choose the topic of the lesson: ",
                                      reply_markup=create_lessons_topics_markup())

    elif call.data == '/testing':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Choose the level of test complexity: ",
                                      reply_markup=create_levels_markup())

    elif call.data == '/account':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        user_visual_repr_function(message=call.message, bot=telebot_instance)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text=f"For detailed information click on the "
                                           f"'Account statistics' button or click 'Cancel' to exit",
                                      reply_markup=create_account_markup())

    elif call.data == '/coding':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Choose the level of test code complexity: ",
                                      reply_markup=create_levels_markup())

    elif call.data == '/comments':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Want to write a comment or view comments?: ",
                                      reply_markup=comment_markup())

    elif call.data == '/premium':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Discover many exciting\n"
                                           "opportunities with 'Premium' access!\n\n"
                                           "Select the option: ",
                                      reply_markup=create_premium_markup())

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
