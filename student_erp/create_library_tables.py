import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# BOOKS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT,
    author TEXT,
    category TEXT,
    available_copies INTEGER
)
""")

# BOOK ISSUE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS book_issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    book_id INTEGER,
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TEXT,
    status TEXT DEFAULT 'Borrowed'
)
""")

conn.commit()
conn.close()

print("Library tables created successfully ✅")