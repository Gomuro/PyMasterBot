# <span style="color:red">`documentation_handler.py` module</span>


### 🔴 Introduction:

The `documentation_handler.py` module provides functionality for searching and retrieving documentation using the
`inspect` library. It is designed to be used in a Telegram bot to provide users with easy access to documentation for
different Python modules, classes, functions, and methods.

This module contains the following main components:

    ♦️ `search_documentation` function: This function takes a user's input and searches for relevant documentation using
     the inspect library. It returns the documentation in a formatted manner.

    ♦️ `delete_previous_messages` function: This helper function is used to delete previous messages in order to keep
     the chat clean and prevent clutter.

The `documentation_handler.py` module serves as an intermediary between the Telegram bot and the `inspect` library,
enabling users to search for documentation directly within the bot's chat interface.


### 🟠 Installation:
To use the `documentation_handler.py` module, you need to follow these steps to set up and install the necessary
dependencies:
    Installation:

    To use the `documentation_handler.py` module, you need to follow these steps to set up and install the necessary
     dependencies:

   1. Make sure you have Python installed on your system (version 3 or above). You can download Python from the
    official website: https://www.python.org/downloads/

   2. Install the required dependencies. Open your command prompt or terminal and run the following command:
   pip install telebot

   This will install the Telebot library, which is used in the `documentation_handler.py` module.

   3. Once the dependencies are installed, you can import the `documentation_handler.py` module into your project and
    use the `search_documentation` function to search for documentation.

That's it! You have successfully set up the `documentation_handler.py` module and installed the necessary
dependencies.


### 🟡 Usage:
To search for documentation using the `documentation_handler.py` module, follow these steps:

    1. Import the `documentation_handler` module into your Python script or bot project:
       from documentation_handler import search_documentation

    2. Call the search_documentation function with "message" and "telebot_instance" parameters:
    search_documentation(message, telebot_instance)

        * "message" parameter represents the message that the bot receives from the user;
        * "telebot_instance" is a Telegram bot object created using the TeleBot class.

    From the message (that is received as a function argument) a keyword is generated to search for the documentation.

    3. The function will search for the documentation using the `inspect` library and retrieve the relevant information.

    4. The retrieved documentation will be sent as a message back to the user via the Telegram bot.

Here's an example of using the search_documentation function:
```bash
 # Assume message and telebot_instance are defined
search_documentation(message, telebot_instance)
```
Make sure to provide the appropriate user input and telebot instance when calling the function.


### 🟢 API Documentation:

The `documentation_handler.py` module provides access to the following APIs:

1. Inspect API:
`inspect.getdoc(module)`: This API retrieves the documentation for a given module. Example usage:
```bash
import inspect
doc = inspect.getdoc(module_name)
```
This API is used in the search_documentation function to fetch the documentation for the user's input.

2. Ast API:
 `ast.parse(user_input, mode="eval")`: This API module to convert an input expression into a node (an AST node) 
  and then compile it into a safe expression for execution. Example usage:
```bash
import ast
doc = inspect.getdoc(module_name)
```
This API is used in the search_documentation function to limit the possibility of executing unsafe code in an 
input expression.

3. Telebot API:
    `telebot_instance.send_message(chat_id, text)`: This API sends a text message to the specified chat ID.
Example usage:
```bash
telebot_instance.send_message(chat_id, text="print!")
```
This API is used in the search_documentation function to send the formatted documentation back to the user.

4. Telebot API (Delete Message):

    `telebot_instance.delete_message(chat_id, message_id)`: This API deletes a specific message in the chat.
    Example usage:
```bash
telebot_instance.delete_message(chat_id, message_id)
```
This API is used in the delete_previous_messages function to remove the previous messages before sending the
    documentation.

Please refer to the official documentation of the Inspect and Telebot libraries for more information on their
APIs and usage.


### 🔵 Problem-solving:
There are several possible problems and errors that may occur. Here are some tips and tricks to fix these problems:

    1. Unsatisfactory import: Ensure that all required modules and packages are imported correctly.
    2. Errors in reading the message: Make sure you are getting the message text from the "message.text"
    variable correctly.
    3. Bugs in error handling: The search_documentation function has an except block that catches any exceptions and
    outputs an error message.
    4. Checking the connection to the Telegram Bot API: Make sure you have a valid API token for your bot and that
    you have an active connection to the Telegram Bot API. Make sure the bot has the right to send messages and
    access the required functionality.


### 🟣 Contribution:

Contributions to the `documentation_handler.py` module are welcome! If you would like to enhance or improve
 the codebase, here are some guidelines to follow:

1. Fork the repository:
   Start by forking the repository to your GitHub account.

2. Create a new branch:
   Create a new branch for your contributions. It is recommended to use a descriptive branch name that reflects
    the nature of your changes.

3. Make your changes:
   Implement your changes, enhancements, or bug fixes in the `documentation_handler.py` module.

4. Test your changes:
   Before submitting a pull request, make sure to test your changes thoroughly.
    Verify that the functionality is working as expected and that no new issues are introduced.

5. Commit and push:
   Commit your changes and push them to your forked repository.

6. Submit a pull request:
   Submit a pull request from your branch to the main repository. Provide a clear and concise description of
    your changes, explaining the purpose and benefits.

7. Review and iterate:
   The code maintainers will review your pull request, provide feedback, and suggest any necessary improvements.
   Iterate on the changes until they are approved.

8. Contribution guidelines:
   Follow any specific contribution guidelines or coding standards set by the project.
   Ensure that your code is well-documented, follows best practices, and maintains code readability.
   If your contribution includes new functionality, consider adding corresponding unit tests.

Thank you for considering contributing to the `documentation_handler.py` module.
Your contributions are greatly appreciated!

