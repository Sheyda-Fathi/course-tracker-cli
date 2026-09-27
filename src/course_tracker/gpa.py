"""Weighted GPA calculation, decoupled from the database"""

from .models import Assignment, Course
from .repository import AssignmentRepository, CourseRepository


def calculate_course_grade(assignments: list[Assignment]) -> float | None:
    graded = [a for a in assignments if a.grade is not None]
    if not graded:
        return None

    total_weight = sum(a.weight for a in graded)
    if total_weight == 0:
        return None

    return sum(a.grade * a.weight for a in graded) / total_weight


def calculate_gpa(courses: list[Course], assignments_by_course: dict[int, list[Assignment]]) -> float | None:
    """Return the credit-weighted GPA across courses."""
    total_credits = 0
    weighted_sum = 0.0

    for course in courses:
        course_grade = calculate_course_grade(assignments_by_course.get(course.id, []))
        if course_grade is None:
            continue
        total_credits += course.credits
        weighted_sum += course_grade * course.credits

    if total_credits == 0:
        return None

    return weighted_sum / total_credits


def calculate_gpa_from_db(db_path, term: str | None = None) -> float | None:
    course_repo = CourseRepository(db_path)
    assignment_repo = AssignmentRepository(db_path)

    courses = course_repo.list_all(term=term)
    assignments_by_course = {
        course.id: assignment_repo.list_by_course(course.id) for course in courses
    }
    return calculate_gpa(courses, assignments_by_course)