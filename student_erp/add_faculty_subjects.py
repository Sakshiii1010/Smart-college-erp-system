import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO faculty_subjects (faculty_id, subject_id)
VALUES (1,1)
""")

conn.commit()
conn.close()

print("Sample faculty subject added")