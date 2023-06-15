import pytest

from database.py_master_bot_database import PyMasterBotDatabase


# Тести для методу add_lesson
def test_add_lesson():
    db = PyMasterBotDatabase()
    db.add_lesson("Math", "Lesson about algebra", "Text of the lesson", "pending")
    assert db.check_lesson_exists(1) == True


# Тести для методу add_lesson_progress
def test_add_lesson_progress():
    db = PyMasterBotDatabase()
    db.add_user(1, "John", "john123")
    db.add_lesson("Math", "Lesson about algebra", "Text of the lesson", "pending")
    db.add_lesson_progress(1, 1)
    user = db.get_user_by_id(1)
    assert user.progress == []


# Тести для методу add_points
def test_add_points():
    db = PyMasterBotDatabase()
    db.add_user(2, "John", "john123")  # Use a different user ID
    db.add_points(2, 10)  # Use the same user ID as the added user
    user = db.get_user_by_id(2)
    assert user.score == 10


# Тести для методу add_admin_role
def test_add_admin_role():
    db = PyMasterBotDatabase()
    db.add_user(3, "John", "john123")
    db.add_admin_role(3)
    user = db.get_user_by_id(3)
    assert user.role == "admin"


# Тести для методу add_user
def test_add_user():
    db = PyMasterBotDatabase()
    db.add_user(4, "John", "john123")
    assert db.check_user_exists(4) == True


# Тести для методу check_lesson_exists
def test_check_lesson_exists():
    db = PyMasterBotDatabase()
    db.add_lesson("Math", "Lesson about algebra", "Text of the lesson", "pending")
    assert db.check_lesson_exists(1) == True


# Тести для методу check_user_exists
def test_check_user_exists():
    db = PyMasterBotDatabase()
    db.add_user(5, "John", "john123")
    assert db.check_user_exists(5) == True


# Тести для методу delete_lesson
def test_delete_lesson():
    db = PyMasterBotDatabase()
    db.add_lesson("Math", "Lesson about algebra", "Text of the lesson", "pending")
    db.delete_lesson(4)
    assert db.check_lesson_exists(4) == False


# Тести для методу delete_lessons_with_status
def test_delete_lessons_with_status():
    db = PyMasterBotDatabase()
    db.add_lesson("Math", "Lesson about algebra", "Text of the lesson", "pending")
    db.add_lesson("Physics", "Lesson about motion", "Text of the lesson", "bonus")
    db.delete_lessons_with_status("bonus")
    assert db.check_lesson_exists(6) == False


# Тести для методу delete_user
def test_delete_user():
    db = PyMasterBotDatabase()
    db.add_user(7, "John", "john123")
    db.delete_user(7)
    assert db.check_user_exists(7) == False


# Тести для методу delete_users_with_status
def test_delete_users_with_status():
    db = PyMasterBotDatabase()
    db.add_user(8, "John", "john123", status = "оплачено")
    db.add_user(9, "Jane", "jane456", status = "оплачено")
    db.add_user(10, "Mike", "mike789", status = "оплачено")
    db.add_user(11, "Emily", "emily123")
    db.add_user(12, "Alex", "alex456")
    db.add_user(13, "Sarah", "sarah789")
    db.add_user(14, "David", "david123")

    db.delete_users_with_status("оплачено")
    assert db.check_user_exists(8) == False
    assert db.check_user_exists(9) == False
    assert db.check_user_exists(10) == False
    assert db.check_user_exists(11) == True
    assert db.check_user_exists(12) == True
    assert db.check_user_exists(13) == True
    assert db.check_user_exists(14) == True


def test_get_leaderboard():
    database = PyMasterBotDatabase()
    database.add_user(15, "John Doe", "johndoe")
    database.add_user(16, "Jane Smith", "janesmith")
    database.add_user(17, "Robert Johnson", "robertjohnson")

    database.add_points(15, 50)
    database.add_points(16, 30)
    database.add_points(17, 70)

    leaderboard = database.get_leaderboard()

    assert leaderboard[0].id == 17  # Robert Johnson has the highest score
    assert leaderboard[1].id == 15  # John Doe is second
    assert leaderboard[2].id == 16  # Jane Smith is third


def test_get_lessons_by_status():
    database = PyMasterBotDatabase()
    database.add_lesson("Math", "Introduction to Algebra", "Lesson content", "free")
    database.add_lesson("Science", "Introduction to Physics", "Lesson content", "paid")
    database.add_lesson(
        "History", "Introduction to World History", "Lesson content", "free"
    )

    lessons = database.get_lessons_by_status("free")
    paid_lessons = database.get_lessons_by_status("paid")

    assert lessons[0].id == 7
    assert lessons[1].id == 9
    assert paid_lessons[0].id == 8


def test_get_user_by_id():
    database = PyMasterBotDatabase()
    user_id = 18
    name = "John Doe"
    username = "johndoe"

    database.add_user(user_id, name, username)

    user = database.get_user_by_id(user_id)

    assert user.id == user_id
    assert user.name == name
    assert user.username == username
