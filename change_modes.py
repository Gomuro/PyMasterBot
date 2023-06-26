class BotProcessor:
    """This class can change, get or delete the current mode"""

    MODE_MAIN_MENU = "main_menu"
    MODE_DOCUMENTATION = "documentation"
    MODE_CHECK_CODE = "check_code"
    MODE_LESSON = "lesson"
    MODE_HELP = "help"

    def __init__(self):
        """By default current mode set to main menu"""
        self.current_mode = self.MODE_MAIN_MENU

    def change_mode(self, mode):
        """Changing the current mode"""
        self.current_mode = mode

    def get_current_mode(self):
        """Getting the current mode"""
        return self.current_mode

    def is_mode_main_menu(self):
        """Checking if current mode is equal to main menu"""
        return self.current_mode == self.MODE_MAIN_MENU

    def is_mode_documentation(self):
        """Checking if current mode is equal to documentation"""
        return self.current_mode == self.MODE_DOCUMENTATION

    def is_mode_check_code(self):
        """Checking if current mode is equal to check code"""
        return self.current_mode == self.MODE_CHECK_CODE

    def is_mode_lesson(self):
        """Checking if current mode is equal to lesson"""
        return self.current_mode == self.MODE_LESSON

    def is_mode_help(self):
        """Checking if current mode is equal to main help"""
        return self.current_mode == self.MODE_HELP

    def message_handler(self, call):
        """The function which get the checked call data and set the current mode to it"""
        if call.data.find(self.MODE_DOCUMENTATION) == 1:
            self.change_mode(mode=self.MODE_DOCUMENTATION)
            print("New mode set: MODE_DOCUMENTATION")
        elif call.data.find(self.MODE_CHECK_CODE):
            self.change_mode(mode=self.MODE_CHECK_CODE)
            print("New mode set: MODE_CHECK_CODE")
        elif call.data.find(self.MODE_LESSON):
            self.change_mode(mode=self.MODE_LESSON)
            print("New mode set: MODE_LESSON")
        elif call.data.find(self.MODE_HELP):
            self.change_mode(mode=self.MODE_HELP)
            print("New mode set: MODE_HELP")
