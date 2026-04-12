import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    title TEXT,
    message TEXT,
    category TEXT,
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.executemany("""
INSERT INTO notifications (student_id, title, message, category)
VALUES (?, ?, ?, ?)
""", [
    (None, "Mid Term Exam Schedule", "Mid term exams start from 15th March.", "Examination"),
    (None, "Fee Reminder", "Last date to pay fees is 10th March.", "Fees"),
    (1, "Project Submission", "Submit final year project report by Friday.", "Academic")
])

conn.commit()
conn.close()

print("Notifications table created ✅")