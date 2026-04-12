import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS id_card_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    full_name TEXT,
    father_name TEXT,
    dob TEXT,
    course TEXT,
    address TEXT,
    photo TEXT,
    status TEXT DEFAULT 'Pending',
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("ID Card Table Created Successfully ✅")