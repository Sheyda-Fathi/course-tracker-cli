"""Parameterized SQL queries for courses (CRUD)"""

from pathlib import Path
from .db import get_connection
from .exceptions import AssignmentNotFoundError, CourseNotFoundError, DuplicateCourseError, InvalidGradeError
from .models import Assignment, Course

class CourseRepository:
    """all database operations for courses"""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def add(self, name: str, credits: int, term: str) -> Course:
        with get_connection(self._db_path) as conn:
            existing = conn.execute("SELECT id FROM courses WHERE name = ? AND term = ?",(name, term),).fetchone()
            if existing is not None:
                raise DuplicateCourseError(name, term)

            cursor = conn.execute("INSERT INTO courses (name, credits, term) VALUES (?, ?, ?)",(name, credits, term),)
            return Course(id=cursor.lastrowid, name=name, credits=credits, term=term)

    def list_all(self, term: str | None = None) -> list[Course]:
        with get_connection(self._db_path) as conn:
            if term is not None:
                rows = conn.execute("SELECT id, name, credits, term FROM courses WHERE term = ?",(term,),).fetchall()
            else:
                rows = conn.execute("SELECT id, name, credits, term FROM courses").fetchall()
            return [Course(**dict(row)) for row in rows]

    def get(self, course_id: int) -> Course:
        with get_connection(self._db_path) as conn:
            row = conn.execute("SELECT id, name, credits, term FROM courses WHERE id = ?",(course_id,),).fetchone()
            if row is None:
                raise CourseNotFoundError(course_id)
            return Course(**dict(row))

    def delete(self, course_id: int) -> None:
        with get_connection(self._db_path) as conn:
            cursor = conn.execute("DELETE FROM courses WHERE id = ?", (course_id,))
            if cursor.rowcount == 0:
                raise CourseNotFoundError(course_id)

class AssignmentRepository:
    """all database operations for assignment"""

    def __init__(self , _db_path :Path) -> None:
        self._db_path = _db_path

    def add(self,course_id:int, title:str, due_date:str, weight:float) -> Assignment :
        with get_connection(self._db_path) as conn:
            cursor = conn.execute("INSERT INTO assignments (course_id,title,due_date,weight,grade) VALUES (?, ?, ?, ?, ?)", (course_id, title, due_date, weight, None),)
            return Assignment(id=cursor.lastrowid,course_id=course_id,title=title,due_date=due_date,weight=weight,grade=None)

    def list_by_course(self,course_id:int)->list[Assignment]:
        with get_connection(self._db_path) as conn:
            rows = conn.execute("SELECT id,course_id,title,due_date,weight,grade FROM assignments WHERE course_id = ? ",(course_id,),).fetchall()
            return [Assignment(**dict(row)) for row in rows]
        
    def set_grade(self,assignment_id:int, grade:float)->None:
        if grade <0 or grade>20 :
            raise InvalidGradeError(grade)
        with get_connection(self._db_path) as conn:
            cursor = conn.execute("UPDATE assignments SET grade = ? WHERE id = ?", (grade,assignment_id),)
            if cursor.rowcount == 0 :
                raise AssignmentNotFoundError(assignment_id)