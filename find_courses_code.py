import re

target = r"D:\Project\WebLuyenThi\frontend\index.html"
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
with open(r"C:\Users\admin\.gemini\antigravity\scratch\courses_code_output.txt", "w", encoding="utf-8") as f_out:
    for idx, line in enumerate(lines):
        if "coursesList" in line or "courseCatalog" in line or "defaultCourses" in line or "renderCourses" in line:
            f_out.write(f"Line {idx+1}: {line[:120]}\n")
