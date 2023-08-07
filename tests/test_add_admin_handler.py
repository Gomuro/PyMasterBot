import unittest
from unittest.mock import MagicMock, patch

from Handlers.add_admin_handler import add_admin_function


class TestAddAdminHandler(unittest.TestCase):
    def test_add_admin_function(self):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123
        message.from_user.id = 456

        # Mock the PyMasterBotDatabase class
        bot_db = MagicMock()
        bot_db.is_admin.return_value = False
        bot_db.get_admin_count.return_value = 0
        bot_db.check_user_exists.return_value = True
        bot_db.add_admin_role.return_value = None

        # Mock the PyMasterBotDatabase instance creation
        PyMasterBotDatabase = MagicMock(return_value=bot_db)

        with patch("add_admin_handler.PyMasterBotDatabase", PyMasterBotDatabase):
            add_admin_function(bot, message)

        bot_db.is_admin.assert_called_with(456)
        bot_db.get_admin_count.assert_called_once()
        bot_db.add_admin_role.assert_called_with(456)
        bot.send_message.assert_called_with(
            123, "You have been set as the first admin."
        )


if __name__ == "__main__":
    unittest.main()
