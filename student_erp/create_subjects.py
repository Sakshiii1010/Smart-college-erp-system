import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ---------- CREATE TABLE ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_name TEXT,
    marks INTEGER
)
""")

# ---------- INSERT SAMPLE DATA ----------
subjects = [
    (1, "Data Structures", 88),
    (1, "Operating Systems", 91),
    (1, "Database Management", 85),
    (1, "Computer Networks", 90)
]

cursor.executemany("""
INSERT INTO subjects (student_id, subject_name, marks)
VALUES (?, ?, ?)
""", subjects)

conn.commit()
conn.close()

print("Subjects table + sample data ready ✅")