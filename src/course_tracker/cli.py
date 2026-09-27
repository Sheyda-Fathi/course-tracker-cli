"""Command-line interface """

import argparse
import sys
from pathlib import Path

from .exceptions import TrackerError
from .gpa import calculate_gpa_from_db
from .repository import AssignmentRepository, CourseRepository

DEFAULT_DB_PATH = Path.home() / ".course_tracker" / "tracker.db"


def resolve_db_path(args: argparse.Namespace) -> Path:
    if args.db_path is not None:
        return args.db_path
    return DEFAULT_DB_PATH


def cmd_init(args: argparse.Namespace) -> int:
    from .db import init_db

    path = resolve_db_path(args)
    path.parent.mkdir(parents=True, exist_ok=True)
    init_db(path)
    print(f"db created at {path}")
    return 0


def cmd_add_course(args: argparse.Namespace) -> int:
    path = resolve_db_path(args)
    repo = CourseRepository(path)
    course = repo.add(args.name, args.credits, args.term)
    print(f"Added course '{course.name}' (id={course.id})")
    return 0


def cmd_list_courses(args: argparse.Namespace) -> int:
    path = resolve_db_path(args)
    repo = CourseRepository(path)
    courses = repo.list_all(term=args.term)
    if not courses:
        print("No courses found")
    else:
        for course in courses:
            print(f"{course.id}. {course.name}  {course.credits} credits  ({course.term})")
    return 0


def cmd_delete_course(args: argparse.Namespace) -> int:
    path = resolve_db_path(args)
    repo = CourseRepository(path)
    repo.delete(args.course_id)
    print(f"Course {args.course_id} deleted successfully.")
    return 0

def cmd_add_assignment(args: argparse.Namespace) -> int:
    path = resolve_db_path(args)
    repo = AssignmentRepository(path)
    assignment = repo.add(args.course_id, args.title, args.due_date, args.weight)
    print(f"Added assignment '{assignment.title}' (id={assignment.id}) to course {args.course_id}")
    return 0


def cmd_list_assignments(args: argparse.Namespace) -> int:
    path = resolve_db_path(args)
    repo = AssignmentRepository(path)
    assignments = repo.list_by_course(args.course_id)
    if not assignments:
        print("No assignments found")
    else:
        for a in assignments:
            grade = a.grade if a.grade is not None else "-"
            print(f"{a.id}. {a.title}  {a.weight}%  grade={grade}")
    return 0


def cmd_set_grade(args: argparse.Namespace) -> int:
    path = resolve_db_path(args)
    repo = AssignmentRepository(path)
    repo.set_grade(args.assignment_id, args.grade)
    print(f"Set grade {args.grade} for assignment {args.assignment_id}")
    return 0


def cmd_gpa(args: argparse.Namespace) -> int:
    path = resolve_db_path(args)
    gpa = calculate_gpa_from_db(path, term=args.term)
    if gpa is None:
        print("No graded assignments yet")
    else:
        print(f"GPA: {gpa:.2f}")
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="course-tracker",
        description="A CLI course and assignment tracker",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="Path to the db file (default: ~/.course_tracker/tracker.db)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create a new db")
    p_init.set_defaults(func=cmd_init)

    p_add_course = sub.add_parser("add-course", help="Add a new course")
    p_add_course.add_argument("name")
    p_add_course.add_argument("credits", type=int)
    p_add_course.add_argument("term")
    p_add_course.set_defaults(func=cmd_add_course)

    p_list_courses = sub.add_parser("list-courses", help="List all courses")
    p_list_courses.add_argument("--term", default=None)
    p_list_courses.set_defaults(func=cmd_list_courses)

    p_delete_course = sub.add_parser("delete-course", help="Delete a course")
    p_delete_course.add_argument("course_id", type=int)
    p_delete_course.set_defaults(func=cmd_delete_course)

    p_add_assignment = sub.add_parser("add-assignment", help="Add a new assignment")
    p_add_assignment.add_argument("course_id", type=int)
    p_add_assignment.add_argument("title")
    p_add_assignment.add_argument("due_date")
    p_add_assignment.add_argument("weight", type=float)
    p_add_assignment.set_defaults(func=cmd_add_assignment)

    p_list_assignments = sub.add_parser("list-assignments", help="List assignments for a course")
    p_list_assignments.add_argument("course_id", type=int)
    p_list_assignments.set_defaults(func=cmd_list_assignments)

    p_set_grade = sub.add_parser("set-grade", help="Set the grade for an assignment")
    p_set_grade.add_argument("assignment_id", type=int)
    p_set_grade.add_argument("grade", type=float)
    p_set_grade.set_defaults(func=cmd_set_grade)

    p_gpa = sub.add_parser("gpa", help="Show the credit-weighted GPA")
    p_gpa.add_argument("--term", default=None)
    p_gpa.set_defaults(func=cmd_gpa)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        return args.func(args)
    except TrackerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())