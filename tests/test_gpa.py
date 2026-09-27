from course_tracker.db import init_db
from course_tracker.gpa import calculate_course_grade, calculate_gpa, calculate_gpa_from_db
from course_tracker.models import Assignment, Course
from course_tracker.repository import AssignmentRepository, CourseRepository

def make_assignment(weight, grade, course_id=1):
    return Assignment(id=None, course_id=course_id, title="x", due_date="2026-01-01", weight=weight, grade=grade)


def test_course_grade_weighted_average():
    assignments = [make_assignment(30, 18), make_assignment(70, 16)]
    grade = calculate_course_grade(assignments)
    assert round(grade, 2) == round((30 * 18 + 70 * 16) / 100, 2)


def test_course_grade_ignores_ungraded_assignments():
    assignments = [make_assignment(30, 18), make_assignment(70, None)]
    grade = calculate_course_grade(assignments)
    assert grade == 18


def test_course_grade_none_when_nothing_graded():
    assignments = [make_assignment(30, None), make_assignment(70, None)]
    assert calculate_course_grade(assignments) is None


def test_gpa_is_credit_weighted():
    courses = [
        Course(id=1, name="db", credits=3, term="fall 2026"),
        Course(id=2, name="eng", credits=2, term="fall 2026"),
    ]
    assignments_by_course = {
        1: [make_assignment(100, 18, course_id=1)],
        2: [make_assignment(100, 20, course_id=2)],
    }
    gpa = calculate_gpa(courses, assignments_by_course)
    assert round(gpa, 2) == round((18 * 3 + 20 * 2) / 5, 2)


def test_gpa_none_when_no_course_graded():
    courses = [Course(id=1, name="db", credits=3, term="fall 2026")]
    assignments_by_course = {1: [make_assignment(100, None, course_id=1)]}
    assert calculate_gpa(courses, assignments_by_course) is None


def test_gpa_from_db_end_to_end(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    course_repo = CourseRepository(db_path)
    assignment_repo = AssignmentRepository(db_path)

    course = course_repo.add("db", 3, "fall 2026")
    assignment = assignment_repo.add(course.id, "final", "2026-12-01", 100)
    assignment_repo.set_grade(assignment.id, 17)

    gpa = calculate_gpa_from_db(db_path)
    assert gpa == 17