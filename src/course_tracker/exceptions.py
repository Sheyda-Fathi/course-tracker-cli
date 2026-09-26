"""Custom exceptions"""


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
        super().__init__(f"grade {grade} is not between 0 and 20")


class AssignmentNotFoundError(TrackerError):
    def __init__(self, assignment_id: int) -> None:
        self.assignment_id = assignment_id
        super().__init__(f"assignment with id {assignment_id} not found")