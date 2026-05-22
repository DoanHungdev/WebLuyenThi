import sqlite3

db_path = r"D:\Project\WebLuyenThi\backend\db\database.sqlite"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open(r"C:\Users\admin\.gemini\antigravity\scratch\db_inspection.txt", "w", encoding="utf-8") as f:
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    f.write(f"Tables: {tables}\n\n")

    # Inspect users
    cursor.execute("SELECT id, username, password, fullname, role FROM users")
    users = cursor.fetchall()
    f.write("Users:\n")
    for u in users:
        f.write(f"{u}\n")

    # Inspect curriculums subjects
    cursor.execute("SELECT subject, length(lesson_data) FROM curriculums")
    curris = cursor.fetchall()
    f.write("\nCurriculums:\n")
    for c in curris:
        f.write(f"{c}\n")

    # Inspect courses
    cursor.execute("SELECT id, name, category, teacher, price FROM courses")
    courses = cursor.fetchall()
    f.write("\nCourses:\n")
    for c in courses:
        f.write(f"{c}\n")

conn.close()
