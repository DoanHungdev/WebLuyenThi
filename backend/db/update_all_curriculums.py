import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

all_curri_path = r"D:\Project\WebLuyenThi\backend\db\all_curriculums.json"
import_script_path = r"D:\Project\WebLuyenThi\backend\db\import_course.py"

# Read the chapters structure from the import_course.py file
# (or we can query it directly from SQLite since we just saved it!)
import sqlite3
db_path = r"D:\Project\WebLuyenThi\backend\db\database.sqlite"

try:
    print(f"Reading curriculum course_9 from database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT lesson_data FROM curriculums WHERE subject = 'course_9';")
    row = cursor.fetchone()
    if not row:
        print("Error: course_9 not found in database!")
        sys.exit(1)
        
    lesson_data_json = json.loads(row[0])
    conn.close()
    
    print(f"Reading all_curriculums.json from: {all_curri_path}")
    with open(all_curri_path, "r", encoding="utf-8") as f:
        all_curri = json.load(f)
        
    print("Injecting new course curriculum into JSON under keys 'course_5' and 'course_9'...")
    all_curri["course_9"] = lesson_data_json
    all_curri["course_5"] = lesson_data_json
    
    print(f"Writing updated all_curriculums.json back...")
    with open(all_curri_path, "w", encoding="utf-8") as f:
        json.dump(all_curri, f, ensure_ascii=False, indent=2)
        
    print("Successfully synchronized all_curriculums.json!")
except Exception as e:
    print("Error synchronizing:", e)
