import pytest
from course_tracker.db import init_db
from course_tracker.exceptions import AssignmentNotFoundError,InvalidGradeError
from course_tracker.repository import AssignmentRepository,CourseRepository

@pytest.fixture
def repo(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    course_repo = CourseRepository(db_path)
    assignment_repo = AssignmentRepository(db_path)
    course = course_repo.add("db", 3, "fall 2026")
    return assignment_repo, course.id

#add & list assignment
def test1(repo):
    assignment_repo, course_id = repo
    assignment_repo.add(course_id, "midterm", "2026-10-10", 30)
    assignments = assignment_repo.list_by_course(course_id)
    assert len(assignments) == 1
    assert assignments[0].title == "midterm"


# grade updates
def test2(repo):
    assignment_repo, course_id = repo
    a = assignment_repo.add(course_id, "midterm", "2026-10-10", 30)
    assignment_repo.set_grade(a.id, 17)
    assignments = assignment_repo.list_by_course(course_id)
    assert assignments[0].grade == 17

# grade above 20
def test3(repo):
    assignment_repo, course_id = repo
    a = assignment_repo.add(course_id, "midterm", "2026-10-10", 30)
    with pytest.raises(InvalidGradeError):
        assignment_repo.set_grade(a.id, 25)

# negative grade
def test4(repo):
    assignment_repo, course_id = repo
    a = assignment_repo.add(course_id, "midterm", "2026-10-10", 30)
    with pytest.raises(InvalidGradeError):
        assignment_repo.set_grade(a.id, -5)

# set grade for missing assignment
def test5(repo):
    assignment_repo, course_id = repo
    with pytest.raises(AssignmentNotFoundError):
        assignment_repo.set_grade(999, 15)

# no assignments
def test6(repo):
    assignment_repo, course_id = repo
    assert assignment_repo.list_by_course(course_id) == []