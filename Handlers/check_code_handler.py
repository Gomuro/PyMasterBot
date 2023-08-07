""" This module allows to run check_syntax function"""
import subprocess
import re

from Handlers.exception_handler import handle_exception
from Handlers.help_functions import delete_previous_messages
from utils.bot_logger import log_message

TMP_FILE = 'tmp.py'
CHECK_CODE_COMMAND = '/check_code'

callback_btn_are_exist = True


def check_code(message, telebot_instance):
    """
    This method allows to send designated message when the button been pressed
    """
    try:

        global callback_btn_are_exist

        if not callback_btn_are_exist:  # Check if callback buttons disappear
            delete_previous_messages(message, telebot_instance)  # Delete previous 2 messages

        if callback_btn_are_exist:  # Check if callback buttons are exists
            telebot_instance.delete_message(message.chat.id, message.message_id - 1)  # Delete previous  message

        callback_btn_are_exist = False

        user_input = message.text.strip()
        if user_input.startswith(CHECK_CODE_COMMAND):
            try:
                user_input = message.text.split(maxsplit=1)[1].strip()
            except IndexError:
                text = "Please enter the code for verification."
                log_message(message, CHECK_CODE_COMMAND, user_input, text)
                telebot_instance.send_message(message.chat.id, text=text)
                return

        # Create a temporary file and write the code into it
        with open(TMP_FILE, 'w', encoding='utf-8') as checked_file:
            checked_file.write(user_input + "\n")

        pep8_output = check_style()
        syntax_errors = check_syntax()

        result = ""

        if syntax_errors:
            result += f"There is a syntax error in your code:\n{syntax_errors}\n"
        else:
            result += "The code has no syntax errors.\n"

        if pep8_output:
            cleaned_output = re.sub(
                r"\*.*?\*\* Module tmp\ntmp.py:\d+:\d+: ", "", pep8_output
            )
            cleaned_output = re.sub(r"tmp.py:\d+:\d+: ", "", cleaned_output)

            pep8_errors = re.findall(r"\w+:\s.*", cleaned_output)
            if pep8_errors:
                result += "\nPEP-8 errors in your code:\n"
                result += "\n".join(pep8_errors)
            else:
                result += "\nCode has no PEP-8 errors."

        log_message(message, CHECK_CODE_COMMAND, user_input, result)

        telebot_instance.send_message(message.chat.id, result)

    except Exception as e:
        handle_exception(e, telebot_instance)


def check_style():
    """Compare this snippet from data/bot_token.txt:"""

    result = subprocess.run(
        ["pylint", TMP_FILE],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )  # check=False to not raise an exception
    output = result.stdout.decode("utf-8") + result.stderr.decode("utf-8")
    cleaned_output = output.replace(
        "------------------------------------------------------------------", ""
    )

    return cleaned_output.strip() if cleaned_output else None


def check_syntax():
    """Compare this snippet from data/bot_token.txt:"""
    # create a subprocess to run python command with the file
    with subprocess.Popen(
        ["python", TMP_FILE],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    ) as process:
        # write the code to the subprocess stdin and close it
        error = process.communicate()
    # if there is an error, send it as a message to the user
    if error[1]:
        # remove the unnecessary from the error message
        error = error[1].decode().split("\n")[-2]
        return error
    return None
