"""
This block contains helper functions that add CSV file into the Table in Database
"""

import csv
import sqlalchemy
from sqlalchemy import func, exc

def add_csv_to_database(session, csv_filename, TaskModel, data_func):
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (headers)

        for row in reader:
            if len(row) > 8 or len(row) < 6:
                continue  # Skip rows with less than 6 and more than 8 elements

            if not row:  # Skip empty rows
                continue

            number = row[0]
            if not number.isdigit():
                continue  # Skip rows without a numerical number

            data = data_func(row)
            if data is None:
                continue  # Skip invalid rows

            record_data = data.copy()
            del record_data['id']  # Remove 'id' from data

            # Check if all required fields are present in the data
            required_fields = set(TaskModel.__table__.columns.keys()) - {'id'}  # Exclude 'id' field
            if not required_fields.issubset(record_data.keys()):
                # Skip the row if any required field is missing
                continue

            existing_row = session.query(TaskModel).filter_by(**record_data).first()
            if existing_row:
                continue  # Skip adding the row if it already exists

            last_number = session.query(func.max(TaskModel.id)).scalar() or 0

            try:
                # Create a new record in the database
                new_record = TaskModel(id=last_number + 1, **record_data)
                session.add(new_record)
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                session.rollback()
                existing_record = session.query(TaskModel).filter_by(id=number).first()
                for key, value in record_data.items():
                    setattr(existing_record, key, value)
                session.commit()


def extract_lesson_data(row):
    return {
        'id': row[0],
        'topic': row[1],
        'item': row[2],
        'description': row[3],
        'text': row[4],
        'status': row[5]
    }


def extract_task_data(row):
    if len(row) < 8:
        return None

    level_relation = row[7]
    # Перевірка, чи значення level_relation існує у таблиці levels
    if level_relation not in ["easy", "middle", "hard"]:
        # Обробка відсутнього значення або виведення повідомлення про помилку
        return None

    return {
        'id': row[0],
        'topic': row[1],
        'question': row[2],
        'var1': row[3],
        'var2': row[4],
        'var3': row[5],
        'right_answer': row[6],
        'level_relation': level_relation
    }


# def add_ai_test_tasks_csv(session, csv_filename, AITestTask):
#     add_csv_to_database(session, csv_filename, AITestTask, extract_task_data)
def add_ai_test_tasks_csv(session, csv_filename, TestTask):
    add_csv_to_database(session, csv_filename, TestTask, extract_task_data)

def add_ai_code_tasks_csv(session, csv_filename, CodeTask):
    add_csv_to_database(session, csv_filename, CodeTask, extract_task_data)

def add_ai_lessons_csv(session, csv_filename, Lesson):
    add_csv_to_database(session, csv_filename, Lesson, extract_lesson_data)

def add_test_tasks_csv(session, csv_filename, TestTask):
    add_csv_to_database(session, csv_filename, TestTask, extract_task_data)

def add_code_tasks_csv(session, csv_filename, CodeTask):
    add_csv_to_database(session, csv_filename, CodeTask, extract_task_data)

def add_lessons_csv(session, csv_filename, Lesson):
    add_csv_to_database(session, csv_filename, Lesson, extract_lesson_data)





# def add_lessons_csv(session, csv_filename, Lesson):
#     with open(csv_filename, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the first row (headers)
#
#         for row in reader:
#             if not row:  # Skip empty rows
#                 continue
#
#             number = row[0]
#             if not number.isdigit():
#                 continue  # Skip rows without a numerical number
#
#             topic = row[1]
#             item = row[2]
#             description = row[3]
#             text = row[4]
#             status = row[5]
#
#             # Check if the row already exists in the database
#             existing_row = session.query(Lesson).filter_by(
#                 topic=topic,
#                 item=item,
#                 description=description,
#                 text=text,
#                 status=status,
#             ).first()
#
#             if existing_row:
#                 continue  # Skip adding the row if it already exists
#
#             # Get the maximum number from the database
#             last_number = session.query(func.max(Lesson.id)).scalar() or 0
#
#             try:
#                 # Create a new lesson in the database
#                 new_lesson = Lesson(
#                     id=last_number + 1,  # Set the new number as the maximum + 1
#                     topic=topic,
#                     item=item,
#                     description=description,
#                     text=text,
#                     status=status,
#                 )
#                 session.add(new_lesson)
#                 session.commit()
#             except sqlalchemy.exc.IntegrityError:
#                 # Handle unique constraint violation
#                 session.rollback()
#                 existing_lesson = session.query(Lesson).filter_by(id=number).first()
#                 existing_lesson.topic = topic
#                 existing_lesson.item = item
#                 existing_lesson.description = description
#                 existing_lesson.text = text
#                 existing_lesson.status = status
#                 session.commit()



# def add_csv_to_database(session, csv_filename, TaskModel, data_func):
#     with open(csv_filename, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the first row (headers)
#
#         for row in reader:
#             if not row:  # Skip empty rows
#                 continue
#
#             number = row[0]
#             if not number.isdigit():
#                 continue  # Skip rows without a numerical number
#
#             data = data_func(row)
#             record_data = data.copy()
#             del record_data['id']  # Remove 'id' from data
#
#             existing_row = session.query(TaskModel).filter_by(**record_data).first()
#             if existing_row:
#                 continue  # Skip adding the row if it already exists
#
#             last_number = session.query(func.max(TaskModel.id)).scalar() or 0
#
#             try:
#                 new_record = TaskModel(id=last_number + 1, **data)
#                 session.add(new_record)
#                 session.commit()
#             except sqlalchemy.exc.IntegrityError:
#                 session.rollback()
#                 existing_record = session.query(TaskModel).filter_by(id=number).first()
#                 for key, value in record_data.items():
#                     setattr(existing_record, key, value)
#                 session.commit()