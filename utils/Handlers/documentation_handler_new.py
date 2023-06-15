"""search_documentation handler function"""
import pydoc

from utils.bot_logger import log_message
from utils.Handlers.help_functions import delete_previous_messages

DOCUMENTATION_COMMAND = "/documentation"


def search_documentation(message, telebot_instance):
    """
    Introduction:

    The `documentation_handler.py` module provides functionality for searching and retrieving documentation using the
     Pydoc library. It is designed to be used in a Telegram bot to provide users with easy access to documentation for
      different Python modules, classes, functions, and methods.

    This module contains the following main components:

    - `search_documentation` function: This function takes a user's input and searches for relevant documentation using
     the Pydoc library. It returns the documentation in a formatted manner.

    - `delete_previous_messages` function: This helper function is used to delete previous messages in order to keep
     the chat clean and prevent clutter.

    The `documentation_handler.py` module serves as an intermediary between the Telegram bot and the Pydoc library,
     enabling users to search for documentation directly within the bot's chat interface.

    """

    """
    Installation:
    To use the `documentation_handler.py` module, you need to follow these steps to set up and install the necessary
     dependencies:

    1. Make sure you have Python installed on your system (version 3 or above). You can download Python from the
     official website: https://www.python.org/downloads/

    2. Install the required dependencies. Open your command prompt or terminal and run the following command:
    pip install pydoc telebot

    This will install the Pydoc and Telebot libraries, which are used in the `documentation_handler.py` module.

    3. Once the dependencies are installed, you can import the `documentation_handler.py` module into your project and
     use the `search_documentation` function to search for documentation.

    That's it! You have successfully set up the `documentation_handler.py` module and installed the necessary
    dependencies.

    """

    """
    Usage:
    To search for documentation using the `documentation_handler.py` module, follow these steps:

    1. Import the `documentation_handler` module into your Python script or bot project:
       from documentation_handler import search_documentation
       
    2. Call the search_documentation function with the user's input as a parameter:
    search_documentation(user_input, telebot_instance)
    
    user_input (string): The user's input specifying the documentation to search for.
    telebot_instance (Telebot instance): The instance of the Telebot library used for sending messages.
    
    3. The function will search for the documentation using the Pydoc library and retrieve the relevant information.
    
    4. The retrieved documentation will be sent as a message back to the user via the Telegram bot.

    Here's an example of using the search_documentation function:
    # Assume user_input and telebot_instance are defined
    search_documentation(user_input, telebot_instance)
    
    Make sure to provide the appropriate user input and telebot instance when calling the function.

    """

    """
    API Documentation:
    The `documentation_handler.py` module provides access to the following APIs:

    1. Pydoc API:
    
       `pydoc.render_doc(module)`: This API retrieves the documentation for a given module.

       Example usage:
       import pydoc
       doc = pydoc.render_doc(module_name)
       
    This API is used in the search_documentation function to fetch the documentation for the user's input.

    2. Telebot API:

    telebot_instance.send_message(chat_id, text): This API sends a text message to the specified chat ID.
    
    Example usage:
        telebot_instance.send_message(chat_id, text="print!")
    
    This API is used in the search_documentation function to send the formatted documentation back to the user.

    3. Telebot API (Delete Message):

    telebot_instance.delete_message(chat_id, message_id): This API deletes a specific message in the chat.
    
    Example usage:
    telebot_instance.delete_message(chat_id, message_id)
    
    This API is used in the delete_previous_messages function to remove the previous messages before sending the
    documentation.

    Please refer to the official documentation of the Pydoc and Telebot libraries for more information on their
    APIs and usage.

    """



    delete_previous_messages(message, telebot_instance)

    user_input = message.text.strip()
    if user_input.find("documentation") != -1:
        user_input = message.text.strip()
        user_input = user_input[len(DOCUMENTATION_COMMAND):].strip()

    if not user_input:
        text = "Будь ласка, введіть ключове слово для пошуку документації."
        # log_message(message, DOCUMENTATION_COMMAND, user_input, text)
        telebot_instance.send_message(message.chat.id, text=text)
        return  # Вирівняти з блоком if

    try:
        # Use pydoc to get the documentation
        doc = pydoc.render_doc(user_input)

        if not doc:
            text = "На жаль, не знайдено документації для даного запиту."
            # log_message(message, DOCUMENTATION_COMMAND, user_input, text)
            telebot_instance.send_message(message.chat.id,
                                          text=text
                                          )
            return

        # Remove the content after (...)
        index = doc.find("(...)")
        if index != -1:
            doc = doc[index + len("(...)"):]

        # Format the documentation
        formatted_doc = f"<b>{user_input} Documentation:</b>\n\n{doc}"
        # log_message(message, DOCUMENTATION_COMMAND, message.text, formatted_doc)
        telebot_instance.send_message(message.chat.id, formatted_doc, parse_mode = "HTML")
    except Exception as err:  # rewrite the error exception
        text = "Виникла помилка при пошуку\n" \
               "або перекладі документації."
        # log_message(message, DOCUMENTATION_COMMAND, user_input, text)
        telebot_instance.send_message(message.chat.id,
                                      text=text)
        print(f"Error: {str(err)}")
