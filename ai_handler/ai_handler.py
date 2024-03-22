import subprocess
subprocess.run(["pip", "install", "g4f"], check=True)
from time import sleep
from random import randint
import g4f


'''
This module generates educational content for the bot using chat gpt with the g4f library. It saves information in 
csv files. 
'''

# Глобальна змінна для зберігання списку доступних моделей
available_models = []


# Функція для отримання доступних моделей
def get_available_models():
    global available_models
    try:
        # Отримання всіх атрибутів модуля 'g4f.models'
        available_models = dir(g4f.models)
    except Exception as e:
        print(f"Помилка при отриманні списку доступних моделей: {e}")
        available_models = []


# Функція для вибору і використання моделі
def ask_gpt(prompt: str) -> str:
    global available_models
    # Перевірка наявності доступних моделей
    if not available_models:
        # Якщо список доступних моделей порожній, повертаємо None
        print("Список доступних моделей порожній.")
        return None

    # Ітеруємось по доступних моделях
    for model_name in available_models:
        try:
            # Отримуємо модель за її ім'ям
            model = getattr(g4f.models, model_name)
            # Генерація відповіді за допомогою поточної моделі
            response = g4f.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            print(f"Модель {model} працює.")
            # Повертаємо згенеровану відповідь
            return response
        except Exception as e:
            # Якщо виникає помилка, переходимо до наступної моделі
            print(f"Помилка при використанні моделі {model_name}: {e}")
            continue

    # Якщо жодна з моделей не працює
    print("Не вдалося використати жодну з доступних моделей.")
    return None


if __name__ == '__main__':

    '''
    Create test tasks 
    '''
    # # uncomment to create test tasks in ai_test_tasks_csv

    # # Отримання списку доступних моделей
    # get_available_models()
    #
    #
    # # Open the 'ai_test_tasks.csv' file in read mode and read its contents as lines
    # with open("ai_test_tasks.csv", "r") as test_task_file:
    #     test_tasks = test_task_file.read().splitlines()
    #
    # # Open the 'ai_test_tasks.csv' file in read mode and count the number of records (lines)
    # with open("ai_test_tasks.csv", "r") as response_file:
    #     record_count = sum(1 for _ in response_file)
    #
    # # Define the prompt for generating responses
    # prompt_test_tasks = f"Прочитай файл {test_tasks} і придумай по одному новому завданню з рівнем easy, middle," \
    #          f"hard, нічого зайвого не писатию. Завдання мають бути унікальними." \
    #          f"Рівень постав у кінці строчки. Написати тільки ці три строчки і все в такому ж форматі. Кожне питання з нової строчки." \
    #          f"Всього три строчки! Можеш додавати інщі теми але тільки по мові програмування python і в такому самому форматі як у файлі. Не використовуй коми"
    #
    # # Continue generating responses until the record count reaches 300
    # while record_count < 300:
    #     # Generate responses using the ask_gpt function with a specific prompt
    #     responses = ask_gpt(prompt_test_tasks)
    #
    #     if responses is None:
    #         # If the response is empty, print a message indicating that an empty response was received from the model
    #         print("Отримано порожню відповідь від моделі.")
    #         # Continue to the next iteration of the loop
    #         continue
    #
    #     # Split the response into individual lines
    #     response_lines = responses.split("\n")
    #
    #     # Create a set to store existing lines in the CSV file
    #     existing_lines = set()
    #     # Open the 'ai_test_tasks.csv' file in read mode and populate the set with its existing lines
    #     with open("ai_test_tasks.csv", "r") as response_file:
    #         for existing_line in response_file:
    #             existing_lines.add(existing_line.strip())
    #
    #     # Open the 'ai_test_tasks.csv' file in append mode to add new responses
    #     with open("ai_test_tasks.csv", "a") as response_file:
    #         # Iterate over each line in the response
    #         for line in response_lines:
    #             # Split the line into fields using comma as delimiter
    #             field = line.split(",")
    #             # Check if the last field (level) is in the list of valid levels
    #             if field[-1] not in ["easy", "middle", "hard"]:
    #                 # If not, skip this line
    #                 continue
    #             # Check if the length of the first field (question) is greater than 3 characters
    #             if len(field[0]) > 3:
    #                 # If it is, break the loop (assuming the task is invalid)
    #                 break
    #             # Check if the line is already present in the existing lines
    #             if line.strip() in existing_lines:
    #                 # If it is, skip this line
    #                 continue
    #
    #             print(responses)
    #             # Write the line to the CSV file
    #             response_file.write(line + "\n")
    #             # Flush the file buffer to ensure that data is written to disk before the delay
    #             response_file.flush()
    #             # Delay for a random number of seconds from 30 to 80
    #             random_delay = randint(30, 80)
    #             print(f"Затримка на {random_delay} секунд")
    #             sleep(random_delay)
    #
    #     # Open the 'ai_code_tasks.csv' file in read mode and count the number of records (lines)
    #     with open("ai_test_tasks.csv", "r") as response_file:
    #         record_count = sum(1 for _ in response_file)
    #
    # # Print a message indicating that enough records have been obtained and the program is ending
    # print("Достатньо записів. Завершення програми.")

    '''
    Create code tasks 
    '''
    # # uncomment to create code tasks in ai_code_tasks_csv



    # # Open the 'code_tasks_file.csv' file in read mode and read its contents as lines
    # with open("code_tasks.csv", "r") as code_tasks_file:
    #     code_tasks = code_tasks_file.read().splitlines()
    #
    # # Check if 'ai_code_tasks.csv' exists
    # try:
    #     # Open the 'ai_code_tasks.csv' file in read mode and count the number of records (lines)
    #     with open("ai_code_tasks.csv", "r") as response_file:
    #         record_count = sum(1 for _ in response_file)
    # except FileNotFoundError:
    #     # If the file doesn't exist, create it
    #     with open("ai_code_tasks.csv", "w") as response_file:
    #         pass  # Writing an empty file
    #
    # # Define the prompt for generating responses
    # prompt_code_tasks = f"Прочитай файл {code_tasks} і придумай по одному новому завданню з рівнем easy, middle," \
    #          f"hard, нічого зайвого не писатию. Завдання мають бути унікальними." \
    #          f"Рівень постав у кінці строчки. Написати тільки ці три строчки і все в такому ж форматі. Кожне питання з нової строчки." \
    #          f"Всього три строчки! Можеш додавати інщі теми але тільки по мові програмування python і в такому самому форматі як у файлі. Зверни увагу що кожне поле виділено подвійними кавичками"
    #
    # # Continue generating responses until the record count reaches 300
    # while record_count <= 89:
    #     # Generate responses using the ask_gpt function with a specific prompt
    #     responses = ask_gpt(prompt_code_tasks)
    #
    #     if responses is None:
    #         # If the response is empty, print a message indicating that an empty response was received from the model
    #         print("Отримано порожню відповідь від моделі.")
    #         # Continue to the next iteration of the loop
    #         continue
    #
    #     # Split the response into individual lines
    #     response_lines = responses.split("\n")
    #
    #     # Create a set to store existing lines in the CSV file
    #     existing_lines = set()
    #     # Open the 'ai_code_tasks.csv' file in read mode and populate the set with its existing lines
    #     with open("ai_code_tasks.csv", "r") as response_file:
    #         for existing_line in response_file:
    #             existing_lines.add(existing_line.strip())
    #
    #     # Open the 'ai_code_tasks.csv' file in append mode to add new responses
    #     with open("ai_code_tasks.csv", "a") as response_file:
    #         if not existing_lines:
    #             # Add the first line if the file is empty
    #             response_file.write("Number,Topic,Question,Var1,Var2,Var3,Right_answer,Level_relation\n")
    #         # Iterate over each line in the response
    #         for line in response_lines:
    #             # # Split the line into fields using comma as delimiter
    #             field = line.split(",")
    #             # # Check if the last field (level) is in the list of valid levels
    #             # if field[-1] not in ["easy", "middle", "hard"]:
    #             #     # If not, skip this line
    #             #     continue
    #             if not any(line.endswith(level) for level in ["easy", "middle", "hard"]):
    #                 # If none of the valid levels is found at the end of the line, skip this line
    #                 continue
    #             # Check if the length of the first field (question) is greater than 3 characters
    #             if len(field[0]) > 3:
    #                 # If it is, break the loop (assuming the task is invalid)
    #                 break
    #             # Check if the line is already present in the existing lines
    #             if line.strip() in existing_lines:
    #                 # If it is, skip this line
    #                 continue
    #
    #             # Write the line to the CSV file
    #             response_file.write(line + "\n")
    #             # Flush the file buffer to ensure that data is written to disk before the delay
    #             response_file.flush()
    #             # Delay for a random number of seconds from 30 to 80
    #             random_delay = randint(30, 80)
    #             print(responses)
    #             print(f"Затримка на {random_delay} секунд")
    #             sleep(random_delay)
    #
    #     # Open the 'ai_code_tasks.csv' file in read mode and count the number of records (lines)
    #     with open("ai_code_tasks.csv", "r") as response_file:
    #         record_count = sum(1 for _ in response_file)
    #
    # # Print a message indicating that enough records have been obtained and the program is ending
    # print("Достатньо записів. Завершення програми.")



'''
Create lessons 
'''
# # uncomment to create lessons in ai_lesson_tasks_csv


    # # Open the 'lesson_tasks_file.csv' file in read mode and read its contents as lines
    # with open("lessons.csv", "r") as lesson_tasks_file:
    #     lesson_tasks = lesson_tasks_file.read().splitlines()
    #
    # # Check if 'ai_lesson_tasks.csv' exists
    # try:
    #     # Open the 'ai_lesson_tasks.csv' file in read mode and count the number of records (lines)
    #     with open("ai_lesson_tasks.csv", "r") as response_file:
    #         record_count = sum(1 for _ in response_file)
    # except FileNotFoundError:
    #     # If the file doesn't exist, create it
    #     with open("ai_lesson_tasks.csv", "w") as response_file:
    #         response_file.write("Number,Topic,Item,Description,text,status\n")  # Write the header
    #     record_count = 0  # Initialize record count
    #
    # # Define the prompt for generating responses
    # prompt_lesson_tasks = (f"Прочитай файл {lesson_tasks}, в ньому знаходиться три приклади уроків, напиши схожий урок"
    #                        f"на тему по програмуванню мови python. Уроки мають бути унікальними."
    #                        f"free постав у кінці строчки як в прикладах. Написати в такому ж форматі, щоб можна було"
    #                        f"легко зберегти в csv файл.  Зверни увагу що кожне поле виділено подвійними кавичками")
    #
    # # Continue generating responses until the record count reaches 2000
    # while record_count <= 2000:
    #     # Generate responses using the ask_gpt function with a specific prompt
    #     responses = ask_gpt(prompt_lesson_tasks)
    #
    #     if responses is None:
    #         # If the response is empty, print a message indicating that an empty response was received from the model
    #         print("Отримано порожню відповідь від моделі.")
    #         # Continue to the next iteration of the loop
    #         continue
    #
    #     # Split the response into individual lessons based on the format provided
    #     lessons = responses.strip().split("\n\n")
    #
    #     # Open the 'ai_lesson_tasks.csv' file in append mode to add new responses
    #     with open("ai_lesson_tasks.csv", "a") as response_file:
    #         for lesson in lessons:
    #             # Check if the lesson already exists in the file
    #             if lesson.strip() in open("ai_lesson_tasks.csv", "r").read():
    #                 continue  # Skip if the lesson already exists
    #
    #             # Split the lesson into fields using comma as delimiter
    #             fields = lesson.strip().split(",")
    #
    #             # Check if the last field (status) is 'free'
    #             if fields[-1].strip() != "free":
    #                 continue  # Skip if the last field is not 'free'
    #
    #             # Check if the length of the first field (number) is greater than 3 characters
    #             if len(fields[0]) > 3:
    #                 continue  # Skip if the number exceeds 3 characters
    #
    #             # Write the lesson to the CSV file
    #             response_file.write(lesson.strip() + "\n")  # Write the lesson
    #             response_file.flush()  # Flush the buffer
    #
    #             # Delay for a random number of seconds from 30 to 80
    #             random_delay = randint(30, 80)
    #             print(lesson)
    #             print(f"Затримка на {random_delay} секунд")
    #             sleep(random_delay)
    #
    #             # Increment the record count
    #             record_count += 1
    #
    # # Print a message indicating that enough records have been obtained and the program is ending
    # print("Достатньо записів. Завершення програми.")
