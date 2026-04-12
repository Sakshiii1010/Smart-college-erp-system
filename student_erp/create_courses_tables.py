import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ---------- COURSES TABLE ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT,
    instructor TEXT,
    duration TEXT,
    description TEXT
)
""")

# ---------- ENROLLMENTS TABLE ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS course_enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    status TEXT DEFAULT 'Enrolled',
    enrolled_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Courses tables created successfully ✅")