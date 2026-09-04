import sqlite3


# ---------------- TASK DATABASE ----------------

def create_database():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            date TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

    connection.commit()
    connection.close()


def add_task(task, date):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO tasks (task, date, status) VALUES (?, ?, ?)",
        (task, date, "Pending")
    )

    connection.commit()
    connection.close()


def get_tasks():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    connection.close()
    return tasks


def delete_task(task_id):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()


def complete_task(task_id):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE tasks SET status = 'Completed' WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()


def get_pending_tasks_count():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'Pending'"
    )

    count = cursor.fetchone()[0]

    connection.close()
    return count


# ---------------- TIMETABLE DATABASE ----------------

def create_timetable_table():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            subject TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            room TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_class(day, subject, start_time, end_time, room):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO timetable
        (day, subject, start_time, end_time, room)
        VALUES (?, ?, ?, ?, ?)
        """,
        (day, subject, start_time, end_time, room)
    )

    connection.commit()
    connection.close()


def get_classes():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM timetable")
    classes = cursor.fetchall()

    connection.close()
    return classes


def delete_class(class_id):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM timetable WHERE id = ?",
        (class_id,)
    )

    connection.commit()
    connection.close()


# ---------------- STUDY MATERIALS DATABASE ----------------

def create_materials_table():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            description TEXT,
            file_name TEXT
        )
    """)

    # Add file_name column to an existing database
    try:
        cursor.execute(
            "ALTER TABLE materials ADD COLUMN file_name TEXT"
        )
    except sqlite3.OperationalError:
        pass

    connection.commit()
    connection.close()


def add_material(subject, topic, description, file_name=""):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO materials
        (subject, topic, description, file_name)
        VALUES (?, ?, ?, ?)
        """,
        (subject, topic, description, file_name)
    )

    connection.commit()
    connection.close()


def get_materials():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()

    connection.close()
    return materials


def delete_material(material_id):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM materials WHERE id = ?",
        (material_id,)
    )

    connection.commit()
    connection.close()
    # ---------------- ASSIGNMENTS DATABASE ----------------

def create_assignments_table():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            assignment TEXT NOT NULL,
            deadline TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)

    connection.commit()
    connection.close()


def add_assignment(subject, assignment, deadline):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO assignments
        (subject, assignment, deadline, status)
        VALUES (?, ?, ?, ?)
        """,
        (subject, assignment, deadline, "Pending")
    )

    connection.commit()
    connection.close()


def get_assignments():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM assignments")
    assignments = cursor.fetchall()

    connection.close()
    return assignments


def complete_assignment(assignment_id):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE assignments SET status = 'Completed' WHERE id = ?",
        (assignment_id,)
    )

    connection.commit()
    connection.close()


def delete_assignment(assignment_id):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM assignments WHERE id = ?",
        (assignment_id,)
    )

    connection.commit()
    connection.close()
    