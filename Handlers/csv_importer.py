"""
This block contains helper functions that add CSV file into the Table in Database
"""
import csv
import sqlalchemy
from sqlalchemy import func, exc


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
            item = row[2]
            description = row[3]
            text = row[4]
            status = row[5]

            # Check if the row already exists in the database
            existing_row = session.query(Lesson).filter_by(
                topic=topic,
                item=item,
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
                    item=item,
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
                existing_lesson.item = item
                existing_lesson.description = description
                existing_lesson.text = text
                existing_lesson.status = status
                session.commit()


def add_test_tasks_csv(session, csv_filename, TestTask):
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
                existing_lesson.question = question
                existing_lesson.var1 = var1
                existing_lesson.var2 = var2
                existing_lesson.var3 = var3
                existing_lesson.right_answer = right_answer
                existing_lesson.level_relation = level_relation
                session.commit()


def add_code_tasks_csv(session, csv_filename, CodeTask):
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
            existing_row = session.query(CodeTask).filter_by(
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
            last_number = session.query(func.max(CodeTask.id)).scalar() or 0

            try:
                # Create a new task in the database
                new_lesson = CodeTask(
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
                existing_lesson = session.query(CodeTask).filter_by(id=number).first()
                existing_lesson.topic = topic
                existing_lesson.question = question
                existing_lesson.var1 = var1
                existing_lesson.var2 = var2
                existing_lesson.var3 = var3
                existing_lesson.right_answer = right_answer
                existing_lesson.level_relation = level_relation
                session.commit()
