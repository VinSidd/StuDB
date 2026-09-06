# StuDB- University Student Portal & Quiz System

A terminal-based Python application that provides a student management portal backed by MySQL, paired with an interactive General Knowledge quiz module.

---

## Features

- **Automatic Database Initialization**: Automatically creates the `university` database and `student` table on startup if they do not already exist.
- **Account Registration & Login**: Validates credentials against MySQL and manages user sessions.
- **Profile Management**:
  - View current profile attributes (contact info, branch, enrollment number, study year).
  - Update profile details selectively (press Enter to retain existing values).
- **Interactive Quiz Module**:
  - Presents 5 randomized questions on the Constitution and history of India.
  - Computes score and provides feedback upon completion before returning to the portal menu.

---

## Project Structure

Ensure both Python files reside in the same root directory:

```text
.
├── finalproject.py   # Main entry point (auth, profile management, DB operations)
├── quizz.py          # Quiz module invoked from the main portal
└── README.md
