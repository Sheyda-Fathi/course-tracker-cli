"""Data models"""
from dataclasses import dataclass
from datetime import date

@dataclass
class Course:
    id: int | None
    name: str
    credits: int
    term: str

@dataclass
class Assignment:
    id: int | None
    course_id: int
    title: str
    due_date: str
    weight: float
    grade: float | None = None

    @property
    def is_overdue(self) -> bool:
        return self.grade is None and date.fromisoformat(self.due_date) < date.today()