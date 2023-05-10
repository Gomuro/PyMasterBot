"""
import  telebot module
"""
import telebot


class Keyboard:
    """
    A class for creating custom keyboards for a Telegram bot.

    :param row_width: the number of buttons per row (default 3)
    :param resize_keyboard: whether the keyboard should be resized to fit the user's screen
     (default True)
    """

    def __init__(self, row_width=3, resize_keyboard=True):
        self.keyboard = telebot.types.ReplyKeyboardMarkup(
            row_width=row_width, resize_keyboard=resize_keyboard)

    def add_button(self, text):
        """
        Add a single button to the keyboard.

        :param text: the text displayed on the button
        """
        button = telebot.types.KeyboardButton(text=text)
        self.keyboard.add(button)

    def add_buttons(self, buttons):
        """
        Add multiple buttons to the keyboard.

        :param buttons: a list of dictionaries representing the buttons,
        where each dictionary contains the 'text' key
        with the text displayed on the button
        """
        for button in buttons:
            self.add_button(button['text'])

    def clear(self):
        """
        Remove the keyboard.
        """
        self.keyboard = telebot.types.ReplyKeyboardRemove()

    def get_keyboard(self):
        """
        Get the keyboard.

        :return: the keyboard
        """
        return self.keyboard


def create_keyboard():
    """
    Creates and returns a custom keyboard with four buttons for the Telegram bot.

    Returns:
    telebot.types.ReplyKeyboardMarkup: A custom keyboard with four buttons.
    """
    keyboard = Keyboard()

    # Define the text for each button
    buttons = [
        {'text': 'Пошук по документації'},
        {'text': 'Перевірка синтаксису коду'},
        {'text': 'Запит на підказку'},
        {'text': 'Допомога по боту'},
    ]

    # Add each button to the keyboard
    keyboard.add_buttons(buttons)

    # Return the keyboard for use in the bot
    return keyboard.get_keyboard()
