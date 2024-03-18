from time import sleep
from random import randint
import g4f


if __name__ == '__main__':
    with open("ai_test_tasks.csv", "r") as test_task_file:
        test_tasks = test_task_file.read().splitlines()
        # print(test_tasks)

    def ask_gpt(promt: str) -> str:
        response = g4f.ChatCompletion.create(
            model=g4f.models.codellama_34b_instruct,
            messages=[{"role": "user", "content": promt}]
        )
        return response

    with open("ai_test_tasks.csv", "r") as response_file:
        record_count = sum(1 for _ in response_file)

    while record_count < 200:

        responses = (ask_gpt(f"Прочитай файл {test_tasks} і придумай по одному новому завданню з рівнем easy, middle,"
                  f"hard, нічого зайвого не писатию. Завдання мають бути унікальними."
                  f"Рівень постав у кінці строчки. Написати тільки ці три строчки і все в такому ж форматі. Кожне питання з нової строчки."
                  f"Всього три строчки! Не використовуй коми"))

        print(responses)
        # each response will be a separate line in the response_lines list
        response_lines = responses.split("\n")

        existing_lines = set()
        with open("ai_test_tasks.csv", "r") as response_file:
            for existing_line in response_file:
                existing_lines.add(existing_line.strip())

        with open("ai_test_tasks.csv", "a") as response_file:
            for line in response_lines:
                field = line.split(",")
                if field[-1] not in ["easy", "middle", "hard"]:
                    continue
                if len(field[0]) > 3:
                    break
                if line.strip() in existing_lines:
                    continue

                response_file.write(line + "\n")

                response_file.flush()  # Забезпечити запис даних на диск перед затримкою

                # sleep(120)  # Затримка на 2 хвилини для кожного циклу
                # Затримка на випадкову кількість секунд від 60 до 120
                random_delay = randint(30, 80)
                print(f"Затримка на {random_delay} секунд")

                # Затримка
                sleep(random_delay)
                print(random_delay)

        with open("ai_test_tasks.csv", "r") as response_file:
            record_count = sum(1 for _ in response_file)

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
