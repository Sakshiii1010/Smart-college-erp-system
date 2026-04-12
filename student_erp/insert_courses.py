import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

courses = [
("Python Programming","Dr. Sharma","6 Weeks","Learn Python from basics"),
("Web Development","Prof. Kumar","8 Weeks","HTML CSS JS Flask"),
("Machine Learning","Dr. Verma","10 Weeks","Intro to ML"),
("Cyber Security","Prof. Singh","6 Weeks","Security fundamentals")
]

cursor.executemany("""
INSERT INTO courses (course_name, instructor, duration, description)
VALUES (?,?,?,?)
""", courses)

conn.commit()
conn.close()

print("Courses inserted successfully ✅")