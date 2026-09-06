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

## Prerequisites

Make sure you have the following installed on your machine before running the application:

1. **Python 3.8 or higher**
   - Download: [python.org](https://www.python.org/downloads/)
   - Verify installation:
     ```bash
     python --version
     ```

2. **MySQL Server**
   - Install MySQL Server (e.g., via MySQL Community Server or XAMPP) and ensure the MySQL service is running.
   - Verify connection in your terminal:
     ```bash
     mysql -u root -p
     ```

3. **Required Python Libraries**
   - `mysql-connector-python`: Required to connect Python to MySQL.
     ```bash
     pip install mysql-connector-python
     ```

---

## Configuration

Before launching the application, configure your MySQL database credentials. Currently, these settings are located at the top of `finalproject.py`:

```python
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DATABASE_NAME = os.getenv("DB_NAME", "university")
TABLE_NAME = "student"
```

---

## Database Schema

The application automatically checks for and initializes the database and table during startup via `setup_database()`.

### Entity-Relationship Details

- **Database**: `university`
- **Table**: `student`
- **Primary Key**: `name`
- **Unique Key**: `enroll`

### Table Definition (`student`)

| Column Name | Data Type     | Constraints           | Description                                      |
|-------------|---------------|-----------------------|--------------------------------------------------|
| `name`      | `VARCHAR(255)`| `PRIMARY KEY`         | Student full name (used as unique login username)|
| `email`     | `VARCHAR(255)`|                       | Student email address                            |
| `contact`   | `VARCHAR(20)` |                       | Phone / contact number                           |
| `branch`    | `VARCHAR(100)`|                       | Academic department / branch                     |
| `enroll`    | `VARCHAR(50)` | `UNIQUE`              | University enrollment ID                         |
| `year`      | `VARCHAR(10)` |                       | Current academic year                            |
| `password`  | `VARCHAR(255)`|                       | Account authentication credential                |

### Raw DDL SQL

```sql
CREATE DATABASE IF NOT EXISTS university;

USE university;

CREATE TABLE IF NOT EXISTS student (
    name VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255),
    contact VARCHAR(20),
    branch VARCHAR(100),
    enroll VARCHAR(50) UNIQUE,
    year VARCHAR(10),
    password VARCHAR(255)
);
```

---

## Project Structure

Ensure both Python files reside in the same root directory:

```text
.
├── finalproject.py   # Main entry point (auth, profile management, DB operations)
├── quizz.py          # Quiz module invoked from the main portal
└── README.md
