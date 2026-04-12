import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS certificate_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    certificate_type TEXT,
    purpose TEXT,
    status TEXT DEFAULT 'Pending',
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Certificate table created successfully ✅")