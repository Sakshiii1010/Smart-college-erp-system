import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS uniform_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    size TEXT,
    quantity INTEGER,
    gender TEXT,
    remarks TEXT,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Uniform table created ✅")