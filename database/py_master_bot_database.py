from abc import ABC, abstractmethod
import random

import os
import sqlalchemy
from sqlalchemy import create_engine, func, Column, Integer, String, Date, JSON, BigInteger, ForeignKey, text, update, \
    desc, inspect, MetaData
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
from Handlers.csv_importer import add_lessons_csv, add_test_tasks_csv, add_code_tasks_csv
from Handlers.static_variables import max_total_tasks, max_total_code_tasks

Base = sqlalchemy.orm.declarative_base()

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    username = Column(String)
    status = Column(String)
    paid_until = Column(Date)
    score = Column(Integer, default=0)
    progress = Column(JSON, default=list)
    progress_testing = Column(JSON)
    progress_coding = Column(JSON)
    progress_lessons = Column(JSON, default=list)
    role = Column(String)


class Level(Base):
    __tablename__ = 'levels'

    id = Column(Integer)
    level_name = Column(String, primary_key=True)
    test_task = relationship('TestTask')  # connection with the 'test_tasks' table


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    topic = Column(String)
    item = Column(String)
    description = Column(String)
    text = Column(String)
    status = Column(String)


class TestTask(Base):
    __tablename__ = 'test_tasks'

    id = Column(Integer, primary_key=True)
    topic = Column(String)
    question = Column(String)
    var1 = Column(String)
    var2 = Column(String)
    var3 = Column(String)
    right_answer = Column(String)
    level_relation = Column(String, ForeignKey('levels.level_name'))


class CodeTask(Base):
    __tablename__ = 'code_tasks'

    id = Column(Integer, primary_key=True)
    topic = Column(String)
    question = Column(String)
    var1 = Column(String)
    var2 = Column(String)
    var3 = Column(String)
    right_answer = Column(String)
    level_relation = Column(String, ForeignKey('levels.level_name'))


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    comment_from_user = Column(String)


class DatabaseFactory(ABC):
    @abstractmethod
    def create_database(self):
        pass


class PyMasterBotDatabaseFactory(DatabaseFactory):
    def create_database(self):
        return PyMasterBotDatabase()


class AbstractDatabase(ABC):
    @abstractmethod
    def add_lesson(self, lesson_id, topic, item, description, text, status):
        pass

    @abstractmethod
    def add_test_task(self, task_id, topic, question, var1, var2, var3, right_answer, level_relation):
        pass

    @abstractmethod
    def add_code_task(self, code_task_id, topic, question, var1, var2, var3, right_answer, level_relation):
        pass

    @abstractmethod
    def add_level(self, level_id, level_name):
        pass

    @abstractmethod
    def add_lesson_progress(self, user_id, lesson_id):
        pass

    @abstractmethod
    def add_points(self, user_id, points):
        pass

    @abstractmethod
    def add_admin_role(self, user_id):
        pass

    @abstractmethod
    def add_user(
        self,
        user_id,
        name,
        username,
        status="не оплачено",
        paid_until=None,
        score=0,
        progress=[],
        progress_testing={},
        progress_coding={},
        progress_lessons=[],
        role=None,
    ):
        pass

    @abstractmethod
    def check_lesson_exists(self, lesson_id):
        pass

    @abstractmethod
    def check_user_exists(self, user_id):
        pass

    @abstractmethod
    def check_levels_exist(self):
        pass

    @abstractmethod
    def check_status_premium(self, user_id):
        pass

    @abstractmethod
    def delete_lesson(self, lesson_id):
        pass

    @abstractmethod
    def delete_test_task(self, test_task_id):
        pass

    @abstractmethod
    def delete_code_task(self, code_task_id):
        pass

    @abstractmethod
    def delete_level(self, level_name):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def get_leaderboard(self):
        pass

    @abstractmethod
    def get_lessons_by_status(self, status):
        pass

    @abstractmethod
    def get_lessons_by_topic(self, topic):
        pass

    @abstractmethod
    def get_lessons_by_item(self, item):
        pass

    @abstractmethod
    def get_lessons_topics(self):
        pass

    @abstractmethod
    def get_lessons_items(self, topic):
        pass

    @abstractmethod
    def get_random_lessons_items(self):
        pass

    @abstractmethod
    def get_lesson_last_id(self):
        pass

    @abstractmethod
    def get_test_task_by_question(self, question):
        pass

    @abstractmethod
    def get_test_task_last_id(self):
        pass

    @abstractmethod
    def get_test_task_by_id(self, test_task_id):
        pass

    @abstractmethod
    def get_code_task_by_question(self, question):
        pass

    @abstractmethod
    def get_code_task_last_id(self):
        pass

    @abstractmethod
    def get_code_task_by_id(self, code_task_id):
        pass

    @abstractmethod
    def get_level_by_name(self, level_name):
        pass

    @abstractmethod
    def get_all_levels(self):
        pass

    @abstractmethod
    def get_level_last_id(self):
        pass

    @abstractmethod
    def get_all_comments(self):
        pass

    @abstractmethod
    def get_comment_by_id(self, comment_id):
        pass

    @abstractmethod
    def get_comment_by_text(self, comment):
        pass

    @abstractmethod
    def get_comment_last_id(self):
        pass

    @abstractmethod
    def get_own_comments_by_name(self, user_name):
        pass

    @abstractmethod
    def get_total_lessons_count(self):
        pass

    @abstractmethod
    def get_total_users_count(self):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def get_users_by_score(self, score):
        pass

    @abstractmethod
    def get_users_by_status(self, status):
        pass

    @abstractmethod
    def get_admin_count(self):
        pass

    @abstractmethod
    def get_test_tasks_topics_by_level(self, level):
        pass

    @abstractmethod
    def get_code_tasks_topics_by_level(self, level):
        pass

    @abstractmethod
    def is_admin(self, user_id):
        pass

    @abstractmethod
    def update_user_paid_until(self, user_id, paid_until):
        pass

    @abstractmethod
    def update_user_scores(self, score_threshold, increment):
        pass

    @abstractmethod
    def update_user_status(self, user_id, status):
        pass

    def update_user_role(self, user_id, role):
        pass

    @abstractmethod
    def add_lessons_csv(self, csv_filename):
        pass

    @abstractmethod
    def add_test_tasks_csv(self, csv_filename):
        pass

    @abstractmethod
    def get_all_tables(self):
        pass

    @abstractmethod
    def get_table_by_name(self, table_name):
        pass

    @abstractmethod
    def get_test_tasks_by_level(self, level):
        pass

    @abstractmethod
    def get_test_tasks_by_level_and_topic(self, level_name, topic):
        pass

    @abstractmethod
    def get_code_tasks_by_level(self, level):
        pass

    @abstractmethod
    def get_code_tasks_by_level_and_topic(self, level_name, topic):
        pass

    @abstractmethod
    def get_user_progress_testing_level(self, user_id, level_name):
        pass

    @abstractmethod
    def get_uncompleted_test_tasks_by_level(self, user_id, level_name):
        pass

    @abstractmethod
    def get_uncompleted_code_tasks_by_level(self, user_id, level_name):
        pass

    @abstractmethod
    def add_task_to_progress_testing(self, user_id, task_id, level_name):
        pass

    @abstractmethod
    def add_lesson_to_progress_lesson(self, user_id, lesson_id):
        pass

    @abstractmethod
    def check_this_level_task_exists(self, level_name):
        pass

    @abstractmethod
    def add_code_task_to_progress_coding(self, user_id, code_task_id, level_name):
        pass

    @abstractmethod
    def check_this_level_code_task_exists(self, level_name):
        pass

    @abstractmethod
    def get_level_count(self, level_name):
        pass

    @abstractmethod
    def is_task_in_progress_testing(self, user_id, task_id, level_name):
        pass

    @abstractmethod
    def is_code_task_in_progress_coding(self, user_id, code_task_id, level_name):
        pass

    @abstractmethod
    def check_rank(self, user_id):
        pass

    @abstractmethod
    def check_coding_rank(self, user_id):
        pass

    @abstractmethod
    def check_lessons_rank(self, user_id):
        pass

    @abstractmethod
    def top_users_by_score(self, top_number):
        pass

    @abstractmethod
    def rank_user_score(self, user_id):
        pass

    @abstractmethod
    def check_code_rank(self, user_id):
        pass

    @abstractmethod
    def get_code_level_count(self, level_name):
        pass

    @abstractmethod
    def get_user_progress_coding_level(self, user_id, level_name):
        pass


class PyMasterBotDatabase(AbstractDatabase, ABC):
    def __init__(self):
        self.engine = create_engine(
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_lesson(self, lesson_id, topic, item, description, text, status):
        new_lesson = Lesson(
            id=lesson_id, topic=topic, item=item, description=description, text=text, status=status
        )
        self.session.add(new_lesson)
        self.session.commit()

    def add_test_task(self, task_id, topic, question, var1, var2, var3, right_answer, level_relation):
        new_test_task = TestTask(id=task_id, topic=topic, question=question, var1=var1, var2=var2, var3=var3,
                                 right_answer=right_answer, level_relation=level_relation)
        self.session.add(new_test_task)
        self.session.commit()

    def add_code_task(self, code_task_id, topic, question, var1, var2, var3, right_answer, level_relation):
        new_test_task = TestTask(id=code_task_id, topic=topic, question=question, var1=var1, var2=var2, var3=var3,
                                 right_answer=right_answer, level_relation=level_relation)
        self.session.add(new_test_task)
        self.session.commit()

    def add_comment(self, comment_id, name, comment):
        new_comment = Comment(id=comment_id, name=name, comment_from_user=comment)
        self.session.add(new_comment)
        self.session.commit()

    def add_level(self, level_id, level_name):
        new_level = Level(id=level_id, level_name=level_name)
        self.session.add(new_level)
        self.session.commit()

    def add_lesson_progress(self, user_id, lesson_id):
        user = self.get_user_by_id(user_id)
        if user:
            print(user)
            if lesson_id not in user.progress_lessons:
                user.progress_lessons.append(lesson_id)
                self.session.commit()

    def add_points(self, user_id, points):
        user = self.get_user_by_id(user_id)
        if user:
            user.score += points
            self.session.commit()

    def add_admin_role(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            user.role = "admin"
            self.session.commit()

    def add_user(
        self,
        user_id,
        name,
        username,
        status="не оплачено",
        paid_until=None,
        score=0,
        progress=[],
        progress_testing={},
        progress_coding={},
        progress_lessons=[],
        role="user",
    ):
        new_user = User(
            id=user_id,
            name=name,
            username=username,
            status=status,
            paid_until=paid_until,
            progress_testing=dict.fromkeys([level for level in self.get_all_levels()], []),
            progress_coding=dict.fromkeys([level for level in self.get_all_levels()], [])
        )

        self.session.add(new_user)
        self.session.commit()

    def check_lesson_exists(self, lesson_id):
        lesson = self.session.query(Lesson).filter_by(id=lesson_id).first()
        if lesson:
            return True
        return False

    def check_user_exists(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            return True
        return False

    def check_levels_exist(self):
        levels = self.session.query(Level).exists()
        if levels:
            return True
        return False

    def check_status_premium(self, user_id):
        user = self.get_user_by_id(user_id)
        if user.status == 'premium':
            return True
        return False

    def delete_lesson(self, lesson_id):
        lesson = self.session.query(Lesson).filter_by(id=lesson_id).first()
        if lesson:
            self.session.delete(lesson)
            self.session.commit()

    def delete_test_task(self, test_task_id):
        test_task = self.session.query(TestTask).filter_by(id=test_task_id).first()
        if test_task:
            self.session.delete(test_task)
            self.session.commit()

    def delete_code_task(self, code_task_id):
        code_task = self.session.query(CodeTask).filter_by(id=code_task_id).first()
        if code_task:
            self.session.delete(code_task)
            self.session.commit()

    def delete_comment(self, comment_id):
        comment = self.session.query(Comment).filter_by(id=comment_id).first()
        if comment:
            self.session.delete(comment)
            self.session.commit()

    def delete_level(self, level_name):
        level = self.session.query(Level).filter_by(level_name=level_name).first()
        if level:
            self.session.delete(level)
            self.session.commit()

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()

    def get_leaderboard(self):
        leaderboard = self.session.query(User).order_by(User.score.desc()).all()
        return leaderboard

    def get_lessons_by_status(self, status):
        lessons = self.session.query(Lesson).filter_by(status=status).all()
        return lessons

    def get_lessons_by_topic(self, topic):
        lessons = self.session.query(Lesson).filter_by(topic=topic).all()
        return lessons

    def get_lessons_by_item(self, item):
        lesson = self.session.query(Lesson).filter_by(item=item).first()
        return lesson

    def get_lessons_topics(self):
        lessons = self.session.query(Lesson).all()
        topics = sorted(list(set([lesson.topic for lesson in lessons])))
        return topics

    def get_lessons_items(self, topic):
        # Get all lesson items by topic
        items_by_topic = self.session.query(Lesson).filter(Lesson.topic == topic).all()

        # Retrieve and sort all lesson items
        lesson_items = sorted([lesson.item for lesson in items_by_topic])
        return lesson_items

    def get_random_lessons_items(self):
        # Get all lesson items
        all_lessons_items = [lesson.item for lesson in self.session.query(Lesson).all()]
        random.shuffle(all_lessons_items)
        return all_lessons_items[:5]

    def get_lesson_last_id(self):
        lesson_last_id = self.session.query(func.max(Lesson.id)).scalar() or 0
        return lesson_last_id

    def get_test_task_by_question(self, question):
        test_task = self.session.query(TestTask).filter_by(question=question).first()
        return test_task

    def get_test_task_last_id(self):
        test_task_last_id = self.session.query(func.max(TestTask.id)).scalar() or 0
        return test_task_last_id

    def get_test_task_by_id(self, test_task_id):
        test_task = self.session.query(TestTask).filter_by(id=test_task_id).first()
        return test_task

    def get_code_task_by_question(self, question):
        code_task = self.session.query(CodeTask).filter_by(question=question).first()
        return code_task

    def get_code_task_last_id(self):
        code_task_last_id = self.session.query(func.max(CodeTask.id)).scalar() or 0
        return code_task_last_id

    def get_code_task_by_id(self, code_task_id):
        code_task = self.session.query(CodeTask).filter_by(id=code_task_id).first()
        return code_task

    def get_level_by_name(self, level_name):
        level = self.session.query(Level).filter_by(level_name=level_name).first()
        return level

    def get_all_levels(self):

        all_levels = self.session.query(Level).all()
        return [level.level_name for level in all_levels]

    def get_level_last_id(self):
        level_last_id = self.session.query(func.max(Level.id)).scalar() or 0
        return level_last_id

    def get_all_comments(self):
        comments = []
        for comment in self.session.query(Comment).all():
            comments.append(f"{comment.name}: {comment.comment_from_user}")
        return comments

    def get_comment_by_id(self, comment_id):
        comment = self.session.query(Comment).filter_by(id=comment_id).first()
        return comment

    def get_comment_by_text(self, comment_text):
        comment = self.session.query(Comment).filter_by(comment_from_user=comment_text).first()
        return comment

    def get_comment_last_id(self):
        comment_last_id = self.session.query(func.max(Comment.id)).scalar() or 0
        return comment_last_id

    def get_own_comments_by_name(self, user_name):
        comment_by_name = []
        for comment in self.session.query(Comment).filter_by(name=user_name.name).all():
            comment_by_name.append(f"{comment.name}: {comment.comment_from_user}")
        return comment_by_name

    def get_total_lessons_count(self):
        count = self.session.query(Lesson).count()
        return count

    def get_total_users_count(self):
        count = self.session.query(User).count()
        return count

    def get_user_by_id(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user

    def get_users_by_score(self, score):
        users = self.session.query(User).filter_by(score=score).all()
        return users

    def get_users_by_status(self, status):
        users = self.session.query(User).filter_by(status=status).all()
        return users

    def get_admin_count(self):
        count = self.session.query(User).filter_by(role="admin").count()
        return count

    def get_test_tasks_topics_by_level(self, level):
        # Get all tasks of the level
        tasks_by_level = self.get_test_tasks_by_level(level)

        # Retrieve and sort all topics of level
        topics = sorted(list(set([task.topic for task in tasks_by_level])))
        return topics

    def get_code_tasks_topics_by_level(self, level):
        # Get all code_tasks of the level
        code_tasks_by_level = self.get_code_tasks_by_level(level)

        # Retrieve and sort all topics of level
        topics = sorted(list(set([code_task.topic for code_task in code_tasks_by_level])))
        return topics

    def is_admin(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            return user.role == "admin"

    def update_user_paid_until(self, user_id, paid_until):
        user = self.get_user_by_id(user_id)
        if user:
            user.paid_until = paid_until
            self.session.commit()

    def update_user_scores(self, score_threshold, increment):
        users = self.session.query(User).filter(User.score >= score_threshold).all()
        for user in users:
            user.score += increment
        self.session.commit()

    def update_user_status(self, user_id, status):
        user = self.get_user_by_id(user_id)
        if user:
            user.status = status
            self.session.commit()

    def update_user_role(self, user_id, role):
        user = self.get_user_by_id(user_id)
        if user:
            user.role = role
            self.session.commit()

    def add_lessons_csv(self, csv_filename):
        add_lessons_csv(self.session, csv_filename, Lesson)

    def add_test_tasks_csv(self, csv_filename):
        add_test_tasks_csv(self.session, csv_filename, TestTask)

    def add_code_tasks_csv(self, csv_filename):
        add_code_tasks_csv(self.session, csv_filename, CodeTask)

    def get_all_tables(self):
        metadata = MetaData(bind=self.engine)
        metadata.reflect()
        table_names = metadata.tables.keys()
        return table_names

    def get_table_by_name(self, table_name):
        metadata = MetaData(bind=self.engine)
        metadata.reflect()

        if table_name in metadata.tables:
            return metadata.tables[table_name]
        else:
            return None

    def get_test_tasks_by_level(self, level):
        test_tasks = self.session.query(TestTask).join(Level).filter(Level.level_name == level).all()
        return test_tasks

    def get_code_tasks_by_level(self, level):
        code_tasks = self.session.query(CodeTask).join(Level).filter(Level.level_name == level).all()
        return code_tasks

    def get_test_tasks_by_level_and_topic(self, level_name, topic):
        test_tasks_by_level_and_topic = self.session.query(TestTask).\
            filter(TestTask.level_relation == level_name, TestTask.topic == topic).all()
        return test_tasks_by_level_and_topic

    def get_code_tasks_by_level_and_topic(self, level_name, topic):
        code_tasks_by_level_and_topic = self.session.query(CodeTask).\
            filter(CodeTask.level_relation == level_name, CodeTask.topic == topic).all()
        return code_tasks_by_level_and_topic

    def get_user_progress_testing_level(self, user_id, level_name):
        user_progress_testing_level = self.session.query(User).\
            filter(func.json_array_length(User.progress_testing[f'{level_name}']) > 0).all()

        return user_progress_testing_level

    def get_user_progress_coding_level(self, user_id, level_name):
        user_progress_coding_level = self.session.query(User).\
            filter(func.json_array_length(User.progress_coding[f'{level_name}']) > 0).all()

        return user_progress_coding_level

    def get_uncompleted_test_tasks_by_level(self, user_id, level_name):
        # Get all tasks of the level
        all_tasks_by_level = self.get_test_tasks_by_level(level_name)
        set_tasks_by_level = set(task.id for task in all_tasks_by_level)

        # create a set of tasks of a certain level that the user has already completed
        user_testing_progress = self.get_user_by_id(user_id).progress_testing
        tests_done_by_user = set(value for value in user_testing_progress[level_name])

        # create a list of tasks of a certain level on the specified topic that the user has not yet done
        uncompleted_tasks_id = list(set_tasks_by_level.difference(tests_done_by_user))

        uncompleted_tasks = []

        for task_id in uncompleted_tasks_id:
            uncompleted_tasks.append(self.get_test_task_by_id(task_id))

        return uncompleted_tasks

    def add_task_to_progress_testing(self, user_id, task_id, level_name):
        # Додавання нового значення до списку в JSON-стовпці за ключем

        # Отримати рядок з бази даних
        row = self.get_user_by_id(user_id)

        # Отримати поточне значення JSON-стовпця
        progress_testing = row.progress_testing

        # Додати нове значення до списку під вказаним ключем
        if level_name in progress_testing and isinstance(progress_testing[level_name], list):
            progress_testing[level_name].append(task_id)
        elif level_name in progress_testing:
            progress_testing[level_name] = [progress_testing[level_name], task_id]
        else:
            progress_testing[level_name] = [task_id]

        # Оновити рядок з оновленим значенням JSON-стовпця
        updating = update(User).where(User.id == user_id).values(progress_testing=progress_testing)
        self.session.execute(updating)
        self.session.commit()

    def add_lesson_to_progress_lesson(self, user_id, lesson_id):

        # Отримати рядок з бази даних
        user = self.get_user_by_id(user_id)

        # Отримати поточне значення стовпця
        progress_lessons_ = user.progress_lessons

        if lesson_id not in progress_lessons_:
            # Додати нове значення до списку
            progress_lessons_.append(lesson_id)

        # Оновити рядок з оновленим значенням JSON-стовпця
        updating = update(User).where(User.id == user_id).values(progress_lessons=progress_lessons_)
        self.session.execute(updating)
        self.session.commit()

    def check_this_level_task_exists(self, level_name):
        task = self.session.query(TestTask).filter_by(level_relation=level_name).first()
        if task:
            return True
        return False

    def get_uncompleted_code_tasks_by_level(self, user_id, level_name):
        # Get all code_tasks of the level
        all_code_tasks_by_level = self.get_code_tasks_by_level(level_name)
        set_code_tasks_by_level = set(code_task.id for code_task in all_code_tasks_by_level)

        # create a set of code_tasks of a certain level that the user has already completed
        user_coding_progress = self.get_user_by_id(user_id).progress_coding
        code_tests_done_by_user = set()

        if user_coding_progress and level_name in user_coding_progress:
            code_tests_done_by_user = set(value for value in user_coding_progress[level_name])

        # create a list of code_tasks of a certain level on the specified topic that the user has not yet done
        uncompleted_code_tasks_id = list(set_code_tasks_by_level.difference(code_tests_done_by_user))

        uncompleted_code_tasks = []

        for code_task_id in uncompleted_code_tasks_id:
            uncompleted_code_tasks.append(self.get_code_task_by_id(code_task_id))

        return uncompleted_code_tasks

    def add_code_task_to_progress_coding(self, user_id, code_task_id, level_name):
        # Додавання нового значення до списку в JSON-стовпці за ключем

        # Отримати рядок з бази даних
        row = self.get_user_by_id(user_id)

        # Отримати поточне значення JSON-стовпця
        progress_coding = row.progress_coding

        # Додати нове значення до списку під вказаним ключем
        if level_name in progress_coding and isinstance(progress_coding[level_name], list):
            progress_coding[level_name].append(code_task_id)
        elif level_name in progress_coding:
            progress_coding[level_name] = [progress_coding[level_name], code_task_id]
        else:
            progress_coding[level_name] = [code_task_id]

        # Оновити рядок з оновленим значенням JSON-стовпця
        updating = update(User).where(User.id == user_id).values(progress_coding=progress_coding)
        self.session.execute(updating)
        self.session.commit()

    def check_this_level_code_task_exists(self, level_name):
        code_task = self.session.query(CodeTask).filter_by(level_relation=level_name).first()
        if code_task:
            return True
        return False

    def get_level_count(self, level_name):
        # Зробити запит для отримання значень для заданого рівня
        values = self.session.query(User.progress_testing[level_name]).filter(
            User.progress_testing[level_name].isnot(None)).first()

        count = len(values[0]) if values and values[0] else 0

        if count == -1 or count is None:
            return 0

        if count > 0:
            return count

        return 0

    def get_code_level_count(self, level_name):
        # Зробити запит для отримання значень для заданого рівня
        values = self.session.query(User.progress_coding[level_name]).filter(
            User.progress_coding[level_name].isnot(None)).first()

        count = len(values[0]) if values and values[0] else 0

        if count == -1 or count is None:
            return 0

        if count > 0:
            return count

        return 0

    def is_task_in_progress_testing(self, user_id, task_id, level_name):
        # Отримати рядок з бази даних
        row = self.get_user_by_id(user_id)

        # Отримати поточне значення JSON-стовпця
        progress_testing = row.progress_testing

        # Перевірити наявність рівня у JSON-стовпці
        if level_name in progress_testing and isinstance(progress_testing[level_name], list):
            # Перевірити наявність завдання з вказаним ID у списку завдань рівня
            if task_id in progress_testing[level_name]:
                return True

        return False

    def is_code_task_in_progress_coding(self, user_id, code_task_id, level_name):
        # Отримати рядок з бази даних
        row = self.get_user_by_id(user_id)

        # Отримати поточне значення JSON-стовпця
        progress_coding = row.progress_coding

        # Перевірити наявність рівня у JSON-стовпці
        if level_name in progress_coding and isinstance(progress_coding[level_name], list):
            # Перевірити наявність завдання з вказаним ID у списку завдань рівня
            if code_task_id in progress_coding[level_name]:
                return True

        return False

    def check_rank(self, user_id):
        # Отримати рядок з бази даних
        row = self.get_user_by_id(user_id)

        # Отримати поточне значення JSON-стовпця
        progress_testing = row.progress_testing

        # Отримати загальну кількість виконаних завдань
        total_tasks = sum(len(values) for values in progress_testing.values())

        # Визначити відсоткове відношення виконаних завдань до максимальної кількості завдань для досягнення рангу
        percentage_relation = total_tasks * 100 / max_total_tasks

        # Повернути назву рангу в залежності від кількості виконаних завдань
        if percentage_relation <= 33:
            return "Beginner"
        elif 33 < percentage_relation <= 66:
            return "Advanced"
        elif 66 < percentage_relation < 100:
            return "Professional"
        else:
            return "Guru"

    def check_coding_rank(self, user_id):
        # Отримати рядок з бази даних
        row = self.get_user_by_id(user_id)

        # Отримати поточне значення JSON-стовпця
        progress_coding = row.progress_coding

        # Отримати загальну кількість виконаних завдань
        total_code_tasks = sum(len(values) for values in progress_coding.values())

        # Визначити відсоткове відношення виконаних завдань до максимальної кількості завдань для досягнення рангу
        percentage_relation = total_code_tasks * 100 / max_total_code_tasks

        # Повернути назву рангу в залежності від кількості виконаних завдань
        if percentage_relation <= 33:
            return "Beginner"
        elif 33 < percentage_relation <= 66:
            return "Advanced"
        elif 66 < percentage_relation < 100:
            return "Professional"
        else:
            return "Guru"

    def check_lessons_rank(self, user_id):
        # Отримати рядок з бази даних
        row = self.get_user_by_id(user_id)

        # Отримати поточне значення JSON-стовпця
        progress_lessons = row.progress_lessons

        # Отримати загальну кількість вивчених уроків
        completed_lessons = len(progress_lessons)

        # Визначити відсоткове відношення вивчених уроків до максимальної кількості уроків для досягнення рангу
        percentage_relation = progress_lessons * 100 / max_total_code_tasks

        # Повернути назву рангу в залежності від кількості вивчених уроків
        if percentage_relation <= 33:
            return "Beginner"
        elif 33 < percentage_relation <= 66:
            return "Advanced"
        elif 66 < percentage_relation < 100:
            return "Professional"
        else:
            return "Guru"

    def check_code_rank(self, user_id):
        # Отримати рядок з бази даних
        row = self.get_user_by_id(user_id)

        # Отримати поточне значення JSON-стовпця
        progress_coding = row.progress_coding

        # Отримати загальну кількість виконаних завдань
        total_code_tasks = sum(len(values) for values in progress_coding.values())

        # Визначити відсоткове відношення виконаних завдань до максимальної кількості завдань для досягнення рангу
        percentage_relation = total_code_tasks * 100 / max_total_tasks

        # Повернути назву рангу в залежності від кількості виконаних завдань
        if percentage_relation <= 33:
            return "Beginner"
        elif 33 < percentage_relation <= 66:
            return "Advanced"
        elif 66 < percentage_relation < 100:
            return "Professional"
        else:
            return "Guru"

    def top_users_by_score(self, top_number):
        top_users_by_score = self.session.query(User).order_by(desc(User.score)).limit(top_number).all()
        return top_users_by_score

    def rank_user_score(self, user_id):
        user_score = self.session.query(User.score).filter(User.id == user_id).scalar()
        rank = self.session.query(func.count(User.score)).filter(User.score > user_score).scalar() + 1
        return rank
