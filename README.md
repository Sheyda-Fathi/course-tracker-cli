# Course Tracker CLI

A command-line application for managing university courses, assignments, grades, and GPA.

The project uses Python and SQLite to store course and assignment data locally and provides a simple CLI for managing academic information.

## Features

- Add, list, and delete courses
- Filter courses by semester
- Add and list assignments for each course
- Set grades for assignments
- Calculate a credit-weighted GPA
- Store data in a local SQLite database
- Validate grades and course information
- Run automated tests with pytest

## Tech Stack

- **Python 3.11+**
- **SQLite** (standard-library `sqlite3`, raw parameterized SQL, no ORM)
- **argparse**
- **pytest**
- **dataclasses**

## Installation

Clone the repository:

```bash
git clone https://github.com/Sheyda-Fathi/course-tracker-cli.git
cd course-tracker-cli
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

Install the project and development dependencies (either command works):

```bash
pip install -e ".[dev]"
# or
pip install -r requirements.txt
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

## GPA Calculation

Grades use a 0–20 scale. The GPA is computed in two steps.

**1. Course grade** — the weighted average of that course's graded assignments:

```text
course_grade = Σ(grade × weight) / Σ(weight)
```

**2. GPA** — the average of course grades, weighted by each course's credits:

```text
GPA = Σ(course_grade × credits) / Σ(credits)
```

Worked example (the workflow above): the *Database* course has 3 credits, a Midterm graded 18 (weight 30) and a Final graded 16 (weight 70).

```text
course_grade = (18×30 + 16×70) / (30 + 70) = 1660 / 100 = 16.60
GPA          = (16.60 × 3) / 3            = 16.60
```

A credit-weighted GPA is used instead of a simple average because a 4-credit course should influence the result more than a 1-credit course.

## Design Decisions

### Deleting a course deletes its assignments (`ON DELETE CASCADE`)

The `assignments` table references `courses` with a foreign key declared as `ON DELETE CASCADE`. When a course is deleted, all of its assignments are deleted with it.

**Why:** an assignment has no meaning without its course. Cascading avoids orphaned rows and keeps the database consistent without extra cleanup code.

**Trade-off:** the deletion is permanent, and deleting a course silently removes every grade recorded under it. An alternative is `ON DELETE RESTRICT`, which refuses to delete a course that still has assignments. That is safer for data you cannot recreate, but it forces the user to delete assignments one by one. For a small personal tracker, cascade was the more convenient choice.

**Important detail:** SQLite does **not** enforce foreign keys by default. `PRAGMA foreign_keys = ON` must be executed on every new connection, so it is set once inside `get_connection()` in `db.py`, and every database operation goes through that function.

### Other decisions

- **Parameterized queries only.** Every SQL statement uses `?` placeholders. User input is never formatted into SQL strings, which prevents SQL injection.
- **One context manager for connections.** `get_connection()` commits on success, rolls back on any exception, and always closes the connection.
- **Repository layer.** SQL lives only in `repository.py`; the CLI never touches the database directly, which keeps the CLI thin and the data layer testable.
- **Tests use temporary databases**, never the real one in `~/.course_tracker/`.

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
├── requirements.txt
└── README.md
```

### Main Components

- **`cli.py`** — Defines the command-line interface and handles user commands.
- **`db.py`** — Creates and manages SQLite database connections and the database schema.
- **`models.py`** — Contains the `Course` and `Assignment` data models.
- **`repository.py`** — Handles database operations for courses and assignments.
- **`gpa.py`** — Contains the GPA calculation logic.
- **`exceptions.py`** — Defines custom exceptions used by the application.
- **`tests/`** — Contains the automated test suite.

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

Each feature was developed separately and then merged into `main` through a Pull Request. Milestones are marked with the tags `v0.1.0`, `v0.2.0`, and `v1.0.0`; see the [v1.0.0 release](https://github.com/Sheyda-Fathi/course-tracker-cli/releases/tag/v1.0.0).

During development, two Git conflicts were intentionally created and resolved:

- One **merge conflict**
- One **rebase conflict**

The details of these conflicts and how they were resolved are documented in [`docs/git-workflow.md`](docs/git-workflow.md).

## What I Learned

- **Feature branches and Pull Requests are useful even when working alone.** Keeping each feature on its own branch kept `main` working at all times, and writing a PR forced me to review my own changes before merging.
- **Merge and rebase solve the same problem differently.** A merge keeps both lines of history and adds a merge commit; a rebase replays my commits on top of `main` for a linear history. Because rebase rewrites commits, the branch has to be pushed with `git push --force-with-lease`.
- **Resolving a conflict means understanding both changes, not picking a side.** In the merge conflict I kept both properties because they did different things; in the rebase conflict I kept the version that used shared constants so the valid grade range lives in one place.
- **SQLite does not enforce foreign keys unless asked.** Without `PRAGMA foreign_keys = ON` on each connection, `ON DELETE CASCADE` silently does nothing.
- **Parameterized queries** keep user input separate from SQL and are the fix for SQL injection.
- **A context manager is a clean way to guarantee commit, rollback, and close** happen no matter how a database operation ends.
- **Tests should never touch real data**; temporary databases make tests fast and safe.

## Future Improvements

Possible future improvements include:

- Update commands for courses and assignments
- Export grades to CSV
- Due-date reminders
- Additional CLI filtering options
- More comprehensive CLI tests
- Support for additional academic terms

## Author

**Sheyda Fathi**

GitHub: [Sheyda-Fathi](https://github.com/Sheyda-Fathi)
