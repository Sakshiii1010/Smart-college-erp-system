import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

books = [
("Python Programming","Mark Lutz","Programming",5),
("Database Management System","Korth","Database",4),
("Operating System Concepts","Silberschatz","OS",3),
("Computer Networks","Andrew Tanenbaum","Networking",4)
]

cursor.executemany("""
INSERT INTO books (book_title,author,category,available_copies)
VALUES (?,?,?,?)
""",books)

conn.commit()
conn.close()

print("Books added successfully 📚")