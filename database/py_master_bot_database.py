from abc import ABC, abstractmethod
import os
import sqlalchemy
from sqlalchemy import create_engine, func, Column, Integer, String, Date, JSON, BigInteger, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
from utils.Handlers.csv_importer import add_data_from_csv


Base = sqlalchemy.orm.declarative_base()

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    username = Column(String)
    status = Column(String)
    paid_until = Column(Date)
    score = Column(Integer, default=0)
    progress = Column(JSON, default=list)
    role = Column(String)


class Level(Base):
    __tablename__ = 'levels'

    id = Column(Integer)
    level_name = Column(String, primary_key=True)
    test_task = relationship('TestTask')  # connection with the 'test_tasks' table


class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    topic = Column(String)
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


class DatabaseFactory(ABC):
    @abstractmethod
    def create_database(self):
        pass


class PyMasterBotDatabaseFactory(DatabaseFactory):
    def create_database(self):
        return PyMasterBotDatabase()


class AbstractDatabase(ABC):
    @abstractmethod
    def add_lesson(self, topic, description, status):
        pass

    @abstractmethod
    def add_test_task(self, task_id, topic, question, var1, var2, var3, right_answer, level_relation):
        pass

    @abstractmethod
    def add_level(self, level_name):
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
    def add_user(self, user_id, name, username, status="не оплачено", paid_until=None, score=0, progress=[], role=None):
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
    def delete_lesson(self, lesson_id):
        pass

    @abstractmethod
    def delete_test_task(self, test_task_id):
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
    def get_test_task_by_question(self, question):
        pass

    @abstractmethod
    def get_test_task_last_id(self):
        pass

    @abstractmethod
    def get_level_by_name(self, level_name):
        pass

    @abstractmethod
    def get_all_levels(self):
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
    def add_data_from_csv(self, csv_filename):
        pass


class PyMasterBotDatabase(AbstractDatabase, ABC):
    def __init__(self):
        self.engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_lesson(self, topic, description, text, status):
        new_lesson = Lesson(topic=topic, description=description, text=text, status=status)
        self.session.add(new_lesson)
        self.session.commit()

    def add_test_task(self, task_id, topic, question, var1, var2, var3, right_answer, level_relation):
        new_test_task = TestTask(id=task_id, topic=topic, question=question, var1=var1, var2=var2, var3=var3,
                                 right_answer=right_answer, level_relation=level_relation)
        self.session.add(new_test_task)
        self.session.commit()

    def add_level(self, level_name):
        new_level = Level(level_name=level_name)
        self.session.add(new_level)
        self.session.commit()

    def add_lesson_progress(self, user_id, lesson_id):
        user = self.get_user_by_id(user_id)
        if user:
            if lesson_id not in user.progress:
                user.progress.append(lesson_id)
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

    def add_user(self, user_id, name, username, status="не оплачено", paid_until=None, score=0, progress=[],
                 role="user"):
        new_user = User(id=user_id, name=name, username=username, status=status, paid_until=paid_until)
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

    def get_test_task_by_question(self, question):
        test_task = self.session.query(TestTask).filter_by(question=question).first()
        return test_task

    def get_test_task_last_id(self):
        test_task_last_id = self.session.query(func.max(TestTask.id)).scalar() or 0
        return test_task_last_id

    def get_level_by_name(self, level_name):
        level = self.session.query(Level).filter_by(level_name=level_name).first()
        return level

    def get_all_levels(self):

        all_levels = self.session.query(Level).all()
        return [level.level_name for level in all_levels]

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

    def add_data_from_csv(self, csv_filename):
        add_data_from_csv(self.session, csv_filename, TestTask)
