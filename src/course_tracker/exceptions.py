"""Custom exceptions"""

MIN_GRADE = 0
MAX_GRADE = 20
class TrackerError(Exception):
    """Base class """


class CourseNotFoundError(TrackerError):
    def __init__(self, course_id: int) -> None:
        self.course_id = course_id
        super().__init__(f"course with id {course_id} not found")


class DuplicateCourseError(TrackerError):
    def __init__(self, name: str, term: str) -> None:
        self.name = name
        self.term = term
        super().__init__(f"course '{name}' already exists for term '{term}'")


class InvalidGradeError(TrackerError):
    def __init__(self, grade: float) -> None:
        self.grade = grade
        super().__init__(f"grade {grade} is not between {MIN_GRADE} and {MAX_GRADE}")


class AssignmentNotFoundError(TrackerError):
    def __init__(self, assignment_id: int) -> None:
        self.assignment_id = assignment_id
        super().__init__(f"assignment with id {assignment_id} not found")