import pytest
from course_tracker.db import init_db
from course_tracker.exceptions import CourseNotFoundError, DuplicateCourseError
from course_tracker.repository import CourseRepository


@pytest.fixture
def repo(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    return CourseRepository(db_path)

# add and get course
def test1(repo):
    course = repo.add("Database", 3, "Fall 2026")
    fetched = repo.get(course.id)
    assert fetched.name == "Database"
    assert fetched.credits == 3

#add duplicate course
def test2(repo):
    repo.add("Database", 3, "Fall 2026")
    with pytest.raises(DuplicateCourseError):
        repo.add("Database", 3, "Fall 2026")

#get missing course
def test3(repo):
    with pytest.raises(CourseNotFoundError):
        repo.get(999)

#all list detail
def test4(repo):
    repo.add("Database", 3, "Fall 2026")
    repo.add("AI", 3, "Fall 2026")
    courses = repo.list_all()
    assert len(courses) == 2

#filter a list by term
def test5(repo):
    repo.add("Database", 3, "Fall 2026")
    repo.add("Old Course", 3, "Spring 2025")
    courses = repo.list_all(term="Fall 2026")
    assert len(courses) == 1
    assert courses[0].name == "Database"

#delete a course
def test6(repo):
    course = repo.add("Database", 3, "Fall 2026")
    repo.delete(course.id)
    with pytest.raises(CourseNotFoundError):
        repo.get(course.id)

#delete a missing course
def test7(repo):
    with pytest.raises(CourseNotFoundError):
        repo.delete(999)