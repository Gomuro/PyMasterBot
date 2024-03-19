import subprocess

subprocess.run(["pip", "install", "g4f"], check=True)
from time import sleep
from random import randint
import g4f


# Define a function named get_available_models that retrieves the available models.
def get_available_models():
    try:
        # Attempt to retrieve all attributes of the 'g4f.models' module and return them.
        return dir(g4f.models)  # Get all module attributes
    except Exception as e:
        # If an exception occurs during the retrieval, print an error message indicating the issue.
        print(f"Помилка при отриманні списку доступних моделей: {e}")
        # Return an empty list to indicate failure.
        return []


# Define a function named ask_gpt that takes a prompt string as input and returns a string.
def ask_gpt(promt: str) -> str:
    # Set the default model to 'g4f.models.codellama_34b_instruct'
    default_model = g4f.models.codellama_34b_instruct
    # Check if the attribute 'last_model_success' is not present in the ask_gpt function object or is False
    if not getattr(ask_gpt, "last_model_success", False):
        try:
            # Attempt to generate a response using the default model and the provided prompt
            response = g4f.ChatCompletion.create(
                model=default_model,
                messages=[{"role": "user", "content": promt}]
            )
            # Indicate that the model has been successfully used by setting 'last_model_success' to True
            ask_gpt.last_model_success = True
            # Print a message indicating that the default model is working
            print("Model codellama_34b_instruct is working")
            # Return the generated response
            return response
        # Handle any exceptions that occur during the generation process
        except Exception as e:
            # Print an error message indicating the issue encountered while using the default model
            print(f"Помилка при використанні моделі за замовчуванням {default_model}: {e}")

    # Retrieve the available models by calling the get_available_models function
    available_models = get_available_models()
    # Iterate over each model name obtained from the available_models list
    for model_name in available_models:
        # Skip the default model ('codellama_34b_instruct') as it has already been tried
        if model_name == 'codellama_34b_instruct':  # Skip the default model, as we have already tried it
            continue
        try:
            # Get the model object using its name from the g4f.models module
            model = getattr(g4f.models, model_name)
            # Attempt to generate a response using the current model and the provided prompt
            response = g4f.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": promt}]
            )
            # Indicate that the model has been successfully used by setting 'last_model_success' to True
            ask_gpt.last_model_success = True
            # Print the name of the model being used
            print("Model: ", model.name)
            # Return the generated response
            return response
        # Handle any exceptions that occur during the generation process
        except Exception as e:
            # Print an error message indicating the issue encountered while using the current model
            print(f"Помилка при використанні моделі {model_name}: {e}")
            # Continue to the next model in case of an error
            continue

    # If none of the models works
    print("Не вдалося використати жодну з доступних моделей.")
    # Mark that none of the models works
    ask_gpt.last_model_success = False
    return None


# Check if the script is being run directly
if __name__ == '__main__':
    # Open the 'ai_test_tasks.csv' file in read mode and read its contents as lines
    with open("ai_test_tasks.csv", "r") as test_task_file:
        test_tasks = test_task_file.read().splitlines()

    # Open the 'ai_test_tasks.csv' file in read mode and count the number of records (lines)
    with open("ai_test_tasks.csv", "r") as response_file:
        record_count = sum(1 for _ in response_file)

    # Continue generating responses until the record count reaches 300
    while record_count < 300:
        # Generate responses using the ask_gpt function with a specific prompt
        responses = ask_gpt(f"Прочитай файл {test_tasks} і придумай по одному новому завданню з рівнем easy, middle,"
                            f"hard, нічого зайвого не писатию. Завдання мають бути унікальними."
                            f"Рівень постав у кінці строчки. Написати тільки ці три строчки і все в такому ж форматі. Кожне питання з нової строчки."
                            f"Всього три строчки! Не використовуй коми")

        if responses is None:
            # If the response is empty, print a message indicating that an empty response was received from the model
            print("Отримано порожню відповідь від моделі.")
            # Continue to the next iteration of the loop
            continue

        # Split the response into individual lines
        response_lines = responses.split("\n")

        # Create a set to store existing lines in the CSV file
        existing_lines = set()
        # Open the 'ai_test_tasks.csv' file in read mode and populate the set with its existing lines
        with open("ai_test_tasks.csv", "r") as response_file:
            for existing_line in response_file:
                existing_lines.add(existing_line.strip())

        # Open the 'ai_test_tasks.csv' file in append mode to add new responses
        with open("ai_test_tasks.csv", "a") as response_file:
            # Iterate over each line in the response
            for line in response_lines:
                # Split the line into fields using comma as delimiter
                field = line.split(",")
                # Check if the last field (level) is in the list of valid levels
                if field[-1] not in ["easy", "middle", "hard"]:
                    # If not, skip this line
                    continue
                # Check if the length of the first field (question) is greater than 3 characters
                if len(field[0]) > 3:
                    # If it is, break the loop (assuming the task is invalid)
                    break
                # Check if the line is already present in the existing lines
                if line.strip() in existing_lines:
                    # If it is, skip this line
                    continue

                print(responses)
                # Write the line to the CSV file
                response_file.write(line + "\n")
                # Flush the file buffer to ensure that data is written to disk before the delay
                response_file.flush()
                # Delay for a random number of seconds from 30 to 80
                random_delay = randint(30, 80)
                print(f"Затримка на {random_delay} секунд")
                sleep(random_delay)

    # Print a message indicating that enough records have been obtained and the program is ending
    print("Достатньо записів. Завершення програми.")




# if __name__ == '__main__':
#     with open("test_tasks.csv", "r") as test_task_file:
#         test_tasks = test_task_file.read().splitlines()
#         # print(test_tasks)
#
#     def ask_gpt(promt: str) -> str:
#         response = g4f.ChatCompletion.create(
#             model=g4f.models.codellama_34b_instruct,
#             messages=[{"role": "user", "content": promt}]
#         )
#         return response
    #
    #
    #
    # responses = (ask_gpt(f"Прочитай файл {test_tasks} і придумай по одному новому завданню з рівнем easy, middle,"
    #               f"hard, нічого зайвого не писатию. Завдання мають бути унікальними."
    #               f"Рівень постав у кінці строчки. Написати тільки ці три строчки і все в такому ж форматі. Кожне питання з нової строчки."
    #               f"Всього три строчки! Не використовуй коми"))
    #
    # print(responses)
    # each response will be a separate line in the response_lines list
    # response_lines = responses.split("\n")
    #
    # existing_lines = set()
    # with open("ai_test_tasks.csv", "r") as response_file:
    #     for existing_line in response_file:
    #         existing_lines.add(existing_line.strip())
    #
    # with open("ai_test_tasks.csv", "a") as response_file:
    #     if not existing_lines:
    #         # Додати перший рядок, якщо файл є порожнім
    #         response_file.write("Number,Topic,Question,Var1,Var2,Var3,Right_answer,Level_relation\n")
    #
    #     for line in response_lines:
    #         field = line.split(",")
    #
    #         # print(len(field), "lenFields")
    #         # if len(field) != 8:
    #         #     continue  # Неправильна кількість полів
    #         if field[-1] not in ["easy", "middle", "hard"]:
    #             continue  # Пропускаємо рядок, якщо останнє поле не є "easy", "middle" або "hard"
    #         if len(field[0]) > 3:
    #             break
    #         if line.strip() in existing_lines:
    #             continue  # Пропускаємо рядок, якщо він вже є у файлі
    #
    #         response_file.write(line + "\n")
