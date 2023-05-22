""" This module allows to run check_syntax function"""
import subprocess
import re


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
            telebot_instance.send_message(message.chat.id, "Будь ласка, вкажіть код для перевірки.")
            return

    # Create a temporary file and write the code into it
    with open('tmp.py', 'w', encoding='utf-8') as checked_file:
        checked_file.write(code + "\n")

    # Check syntax
    syntax_errors = check_syntax('tmp.py')

    # Check PEP8 style
    pep8_output = check_style('tmp.py')

    result = ""

    if syntax_errors:
        result += f"У вашому коді є синтаксична помилка:\n{syntax_errors}\n"
    else:
        result += "Код не має синтаксичних помилок.\n"

    if pep8_output:
        cleaned_output = re.sub(r'\*.*?\*\* Module tmp\ntmp.py:\d+:\d+: ', '', pep8_output)
        result += f"\nУ вашому коді помилка PEP-8:\n{cleaned_output}"
    else:
        result += "\nКод не має помилок PEP-8."

    telebot_instance.send_message(message.chat.id, result)


def check_style(file_path):
    """
    This method checks PEP8 style
    :param file_path:
    :return:
    """
    result = subprocess.run(['pylint', file_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=False)  # check=False to not raise an exception
    output = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
    return output if output else None


def check_syntax(file_path):
    """
    This method checks syntax
    :param file_path:
    :return:
    """
    try:
        # Create a subprocess to run the python command with the file
        process = subprocess.Popen(['python', file_path],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=False)
        # Write the code to the subprocess stdin and close it
        _, error = process.communicate()

        # If there is an error, send it as a message to the user
        if error:
            # Remove unnecessary information from the error message
            error = error.decode().split('\n')[-2]
            return error

    except subprocess.CalledProcessError as check_syntax_error:
        # If there is an error while running the subprocess, send it as a message to the user
        return f"Виникла помилка при перевірці синтаксису:\n{check_syntax_error}"

    # Return None if no errors occurred
    return None
