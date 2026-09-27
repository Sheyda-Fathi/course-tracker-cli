from pathlib import Path

from course_tracker.cli import DEFAULT_DB_PATH, build_parser, resolve_db_path

def test_default_db_path_is_in_home():
    assert DEFAULT_DB_PATH.parent.parent == Path.home()

def test_add_course_parses_arguments():
    parser = build_parser()
    args = parser.parse_args(["add-course", "Database", "3", "Fall 2026"])
    assert args.name == "Database"
    assert args.credits == 3
    assert args.term == "Fall 2026"


def test_list_courses_term_filter_defaults_to_none():
    parser = build_parser()
    args = parser.parse_args(["list-courses"])
    assert args.term is None


def test_add_assignment_parses_arguments():
    parser = build_parser()
    args = parser.parse_args(["add-assignment", "1", "Midterm", "2026-10-10", "30"])
    assert args.course_id == 1
    assert args.title == "Midterm"
    assert args.weight == 30.0


def test_set_grade_parses_arguments():
    parser = build_parser()
    args = parser.parse_args(["set-grade", "1", "17.5"])
    assert args.assignment_id == 1
    assert args.grade == 17.5


def test_gpa_parses_optional_term():
    parser = build_parser()
    args = parser.parse_args(["gpa", "--term", "Fall 2026"])
    assert args.term == "Fall 2026"


def test_db_path_override():
    parser = build_parser()
    custom = Path("custom/tracker.db")
    args = parser.parse_args(["--db-path", str(custom), "list-courses"])
    assert resolve_db_path(args) == custom