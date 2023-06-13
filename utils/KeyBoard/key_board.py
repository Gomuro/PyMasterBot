from abc import ABC, abstractmethod
from telebot import types


class KeyboardFactory(ABC):
    """ Abstract factory for creating keyboards """

    @abstractmethod
    def create_keyboard(self):
        pass


class InlineKeyboardFactory(KeyboardFactory):
    """ Concrete factory for creating InlineKeyboard """

    def create_keyboard(self):
        return InlineKeyboard()


class Keyboard(ABC):
    """ Abstract base class for keyboards """

    @abstractmethod
    def get_keyboard(self):
        pass

    @abstractmethod
    def add_button(self, text, callback_data):
        pass


class InlineKeyboard(Keyboard):
    """ Implementation of InlineKeyboard """

    def __init__(self):
        self.inline_keyboard = types.InlineKeyboardMarkup()

    def get_keyboard(self):
        return self.inline_keyboard

    def add_button(self, text, callback_data):
        self.inline_keyboard.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))


