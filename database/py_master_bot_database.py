from abc import ABC, abstractmethod
from sqlalchemy import create_engine, Column, Integer, String, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    status = Column(String)
    paid_until = Column(Date)
    score = Column(Integer, default=0)
    progress = Column(JSON, default=list)
    role = Column(String)


class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    topic = Column(String)
    description = Column(String)
    text = Column(String)
    status = Column(String)


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

    def add_lesson_progress(self, user_id, lesson_id):
        pass

    @abstractmethod
    def add_points(self, user_id, points):
        pass

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
    def delete_lesson(self, lesson_id):
        pass

    @abstractmethod
    def delete_lessons_with_status(self, status):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def delete_users_with_status(self, status):
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
    def get_lessons_grouped_by_topic(self):
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
    def remove_admin_role(self, user_id):
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


class PyMasterBotDatabase(AbstractDatabase, ABC):
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:753951456Yra@localhost:3000/PyMasterBotDatabase')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_lesson(self, topic, description, text, status):
        new_lesson = Lesson(topic=topic, description=description, text=text, status=status)
        self.session.add(new_lesson)
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

    def delete_lesson(self, lesson_id):
        lesson = self.session.query(Lesson).filter_by(id=lesson_id).first()
        if lesson:
            self.session.delete(lesson)
            self.session.commit()

    def delete_lessons_with_status(self, status):
        lessons = self.session.query(Lesson).filter_by(status=status).all()
        for lesson in lessons:
            self.session.delete(lesson)
        self.session.commit()

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()

    def delete_users_with_status(self, status):
        users = self.session.query(User).filter_by(status=status).all()
        for user in users:
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

    def get_lessons_grouped_by_topic(self):
        topics = {}
        lessons = self.session.query(Lesson).all()
        for lesson in lessons:
            if lesson.topic not in topics:
                topics[lesson.topic] = []
            topics[lesson.topic].append(lesson)
        return topics

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

    def remove_admin_role(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            user.role = "user"
            self.session.commit()

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
