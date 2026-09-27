# Course Tracker CLI

A command-line application for managing university courses, assignments, grades, and GPA.

The project uses Python and SQLite to store course and assignment data locally and provides a simple CLI for managing academic information.

## Features

* Add, list, and delete courses
* Filter courses by semester
* Add and list assignments for each course
* Set grades for assignments
* Calculate GPA based on course credits
* Store data in a local SQLite database
* Validate grades and course information
* Run automated tests with pytest

## Tech Stack

* **Python 3.11+**
* **SQLite**
* **argparse**
* **pytest**
* **dataclasses**

## Installation

Clone the repository:

```bash
git clone https://github.com/Sheyda-Fathi/course-tracker-cli.git
cd course-tracker-cli
```

Create and activate a virtual environment:

### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

Install the project and development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

Initialize the database:

```bash
course-tracker init
```

Add a course:

```bash
course-tracker add-course "Database" 3 "Fall 2026"
```

List courses:

```bash
course-tracker list-courses
```

Add an assignment:

```bash
course-tracker add-assignment 1 "Midterm" 2026-10-10 30
```

List assignments for a course:

```bash
course-tracker list-assignments 1
```

Set a grade:

```bash
course-tracker set-grade 1 18
```

Calculate GPA:

```bash
course-tracker gpa
```

A sample result:

```text
GPA: 16.60
```

The database is stored locally at:

```text
~/.course_tracker/tracker.db
```

A different database path can be provided using the `--db-path` option.

## Example Workflow

A typical workflow can look like this:

```text
Initialize database
       ↓
Add courses
       ↓
Add assignments
       ↓
Set assignment grades
       ↓
Calculate GPA
```

For example:

```bash
course-tracker init

course-tracker add-course "Database" 3 "Fall 2026"

course-tracker add-assignment 1 "Midterm" 2026-10-10 30
course-tracker add-assignment 1 "Final" 2026-12-01 70

course-tracker set-grade 1 18
course-tracker set-grade 2 16

course-tracker gpa
```

Output:

```text
GPA: 16.60
```

## Project Structure

```text
course-tracker-cli/
│
├── src/
│   └── course_tracker/
│       ├── cli.py
│       ├── db.py
│       ├── models.py
│       ├── repository.py
│       ├── gpa.py
│       └── exceptions.py
│
├── tests/
│
├── docs/
│   └── git-workflow.md
│
├── pyproject.toml
└── requirements.txt
```

### Main Components

* **`cli.py`** — Defines the command-line interface and handles user commands.
* **`db.py`** — Creates and manages SQLite database connections and the database schema.
* **`models.py`** — Contains the `Course` and `Assignment` data models.
* **`repository.py`** — Handles database operations for courses and assignments.
* **`gpa.py`** — Contains the GPA calculation logic.
* **`exceptions.py`** — Defines custom exceptions used by the application.
* **`tests/`** — Contains the automated test suite.

## Testing

The project uses `pytest` for automated testing.

Run all tests with:

```bash
pytest
```

Current test suite:

```text
26 passed
```

The tests use temporary databases so that test data does not affect the main local database.

## Git Workflow

The project was developed using a feature-branch workflow.

The main development branches were:

```text
main
├── feat/schema-and-courses
├── feat/assignments
├── feat/gpa-calculation
└── feat/cli-and-tests
```

Each feature was developed separately and then merged into `main` through a Pull Request.

During development, two Git conflicts were intentionally created and resolved:

* One **merge conflict**
* One **rebase conflict**

The details of these conflicts and how they were resolved are documented in:

`docs/git-workflow.md`

## Future Improvements

Possible future improvements include:

* Update commands for courses and assignments
* Export grades to CSV
* Due-date reminders
* Additional CLI filtering options
* More comprehensive CLI tests
* Support for additional academic terms

## Author

**Sheyda Fathi**

GitHub: [Sheyda-Fathi](https://github.com/Sheyda-Fathi)
