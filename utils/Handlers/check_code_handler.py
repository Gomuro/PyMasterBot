""" This module allows to run check_syntax function"""
import subprocess
import re

from utils.bot_logger import log_message

TMP_FILE = 'tmp.py'


def check_code(message, telebot_instance):
    """
    :param telebot_instance: instance of telebot
    :param message: create a temporary file and write the code into it
    :return: send message to user
    """
    code = message.text.strip()
    if code.startswith("/check_code"):
        try:
            code = message.text.split(maxsplit=1)[1].strip()
        except IndexError:

            text = 'Будь ласка, вкажіть код для перевірки.'
            log_message('/check_code', "", text)
            telebot_instance.send_message(message.chat.id, text = text)
            return

    # Create a temporary file and write the code into it
    with open(TMP_FILE, 'w', encoding = 'utf-8') as checked_file:
        checked_file.write(code + "\n")

    pep8_output = check_style()
    syntax_errors = check_syntax()

    result = ""

    if syntax_errors:
        result += f"У вашому коді є синтаксична помилка:\n{syntax_errors}\n"
    else:
        result += "Код не має синтаксичних помилок.\n"

    if pep8_output:
        cleaned_output = re.sub(r'\*.*?\*\* Module tmp\ntmp.py:\d+:\d+: ', '', pep8_output)
        cleaned_output = re.sub(r'tmp.py:\d+:\d+: ', '', cleaned_output)

        pep8_errors = re.findall(r'\w+:\s.*', cleaned_output)
        if pep8_errors:
            result += "\nУ вашому коді помилки PEP-8:\n"
            result += '\n'.join(pep8_errors)
        else:
            result += "\nКод не має помилок PEP-8."

    log_message('/check_code', code, result)

    telebot_instance.send_message(message.chat.id, result)


def check_style():
    """Compare this snippet from data/bot_token.txt:"""
    result = subprocess.run(['pylint', TMP_FILE],
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            check = False)  # check=False to not raise an exception
    output = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
    cleaned_output = output.replace(
        '------------------------------------------------------------------', '')

    return cleaned_output.strip() if cleaned_output else None


def check_syntax():
    """Compare this snippet from tmp.py:"""
    # create a subprocess to run python command with the file
    with subprocess.Popen(['python', TMP_FILE], stdin = subprocess.PIPE,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.PIPE,
                          shell = False) as process:
        # write the code to the subprocess stdin and close it
        error = process.communicate()
    # if there is an error, send it as a message to the user
    if error[1]:
        # remove the unnecessary from the error message
        error = error[1].decode().split('\n')[-2]
        return error
    return None
