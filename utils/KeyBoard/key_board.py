"""This module allows to implement inline keyboard into Telegram Bot """
from telebot import types


class Keyboard:
    """ This class creates an instance of InlineKeyboardMarkup """

    def __init__(self):
        self.inline_keyboard = types.InlineKeyboardMarkup()

     

        self.button_help = types.InlineKeyboardButton(text = 'Допомога',
                                                      callback_data = '/help')
        self.button_syntax_check = types.InlineKeyboardButton(text = 'Перевірити синтаксис',
                                                              callback_data = '/check_code')
        self.button_docs = types.InlineKeyboardButton(text = 'Документація',
                                                      callback_data = '/documentation')

        self.inline_keyboard.row(self.button_help,
                                 self.button_syntax_check,
                                 self.button_docs
                                 )

    def get_keyboard(self):
        """ This method returns keyboard"""
        return self.inline_keyboard


    def add_button(self, text, callback_data):
        """ This method adds a button to the keyboard"""
        self.inline_keyboard.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))

