"""
This block contains helper functions that add CSV file into the Table in Database
"""
import csv
import sqlalchemy
from sqlalchemy import func, exc, and_, cast, JSON


def add_lessons_csv(session, csv_filename, Lesson):
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (headers)

        for row in reader:
            if not row:  # Skip empty rows
                continue

            number = row[0]
            if not number.isdigit():
                continue  # Skip rows without a numerical number

            topic = row[1]
            description = row[2]
            text = row[3]
            status = row[4]

            # Check if the row already exists in the database
            existing_row = session.query(Lesson).filter_by(
                topic=topic,
                description=description,
                text=text,
                status=status,
            ).first()

            if existing_row:
                continue  # Skip adding the row if it already exists

            # Get the maximum number from the database
            last_number = session.query(func.max(Lesson.id)).scalar() or 0

            try:
                # Create a new lesson in the database
                new_lesson = Lesson(
                    id=last_number + 1,  # Set the new number as the maximum + 1
                    topic=topic,
                    description=description,
                    text=text,
                    status=status,
                )
                session.add(new_lesson)
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                # Handle unique constraint violation
                session.rollback()
                existing_lesson = session.query(Lesson).filter_by(id=number).first()
                existing_lesson.topic = topic
                existing_lesson.description = description
                existing_lesson.text = text
                existing_lesson.status = status
                session.commit()


def add_test_tasks_csv(session, csv_filename, TestTask):
    pass
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (headers)

        for row in reader:
            if not row:  # Skip empty rows
                continue

            number = row[0]
            if not number.isdigit():
                continue  # Skip rows without a numerical number

            topic = row[1]
            question = row[2]
            var1 = row[3]
            var2 = row[4]
            var3 = row[5]
            right_answer = row[6]
            level_relation = row[7]

            # Check if the row already exists in the database
            existing_row = session.query(TestTask).filter_by(
                topic=topic,
                question=question,
                var1=var1,
                var2=var2,
                var3=var3,
                right_answer=right_answer,
                level_relation=level_relation
            ).first()

            if existing_row:
                continue  # Skip adding the row if it already exists

            # Get the maximum number from the database
            last_number = session.query(func.max(TestTask.id)).scalar() or 0

            try:
                # Create a new task in the database
                new_lesson = TestTask(
                    id=last_number + 1,  # Set the new number as the maximum + 1
                    topic=topic,
                    question=question,
                    var1=var1,
                    var2=var2,
                    var3=var3,
                    right_answer=right_answer,
                    level_relation=level_relation
                )
                session.add(new_lesson)
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                # Handle unique constraint violation
                session.rollback()
                existing_lesson = session.query(TestTask).filter_by(id=number).first()
                existing_lesson.topic = topic
                existing_lesson.description = question
                existing_lesson.text = var1
                existing_lesson.text = var2
                existing_lesson.text = var3
                existing_lesson.status = right_answer
                existing_lesson.status = level_relation
                session.commit()





