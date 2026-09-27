# Git Workflow

This project was developed using a feature-branch workflow. Each major feature was developed on a separate branch and merged into `main` through a Pull Request.

The project also included two intentionally created Git conflicts: one merge conflict and one rebase conflict. Both were resolved manually as part of the Git practice.

## Branch Strategy

```text
main
├── feat/schema-and-courses
├── feat/assignments
├── feat/gpa-calculation
└── feat/cli-and-tests
```

Each feature was developed on its own branch, reviewed through a Pull Request, and then merged into `main`.

Three tags were used to mark the main project milestones:

| Tag      | Milestone                                                     |
| -------- | ------------------------------------------------------------- |
| `v0.1.0` | Schema, `CourseRepository`, and course tests                  |
| `v0.2.0` | Assignment repository, GPA calculation, and conflict practice |
| `v1.0.0` | Full CLI, final tests, and documentation                      |

## Conflict #1 — Merge Conflict

### What happened

While working on `feat/assignments`, an `is_overdue` property was added to the `Assignment` dataclass.

At the same time, an `is_graded` property was added directly to `main` in the same area of `models.py`.

### Why the conflict happened

Both branches modified the same part of `models.py`. Git could not automatically determine how the two changes should be combined.

### How it was resolved

The branch was updated with:

```bash
git merge main
```

Git marked the conflicting section with conflict markers:

```text
<<<<<<<
=======
>>>>>>>
```

Both properties were kept because they provide different functionality:

* `is_graded` checks whether an assignment has a grade.
* `is_overdue` checks whether an assignment is past its due date and has not been graded.

After removing the conflict markers and keeping both changes, the file was tested and the merge was completed with a commit.

## Conflict #2 — Rebase Conflict

### What happened

While working on `feat/gpa-calculation`, the grade validation in `set_grade` was changed to use the shared `MIN_GRADE` and `MAX_GRADE` constants.

At the same time, `main` contained another change to the same validation, using:

```python
not (0 <= grade <= 20)
```

### Why the conflict happened

Both changes modified the same `if` statement in `repository.py`.

Unlike the first conflict, these were two different implementations of the same validation.

### How it was resolved

The branch was rebased onto `main`:

```bash
git rebase main
```

Git reported a conflict because both versions modified the same section of the file.

The version using `MIN_GRADE` and `MAX_GRADE` was kept because these constants are also used by `InvalidGradeError`. This keeps the valid grade range in one place instead of repeating the values in multiple parts of the code.

After resolving the conflict, the rebase was continued:

```bash
git rebase --continue
```

Because rebase changes commit history, the updated branch was pushed using:

```bash
git push --force-with-lease
```

## Why This Workflow Was Used

Using a separate branch for each feature helped keep `main` in a working state and made each change easier to review through a Pull Request.

It also provided a safe way to practice both `merge` and `rebase`, including resolving real conflicts instead of only learning the commands theoretically.
