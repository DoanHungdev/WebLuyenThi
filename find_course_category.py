import re

target = r"D:\Project\WebLuyenThi\frontend\index.html"
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
with open(r"C:\Users\admin\.gemini\antigravity\scratch\course_cat_output.txt", "w", encoding="utf-8") as f_out:
    for idx, line in enumerate(lines):
        if "selectCourseCategory" in line or "course" in line.lower() and "render" in line.lower() or "courses =" in line:
            f_out.write(f"Line {idx+1}: {line[:120]}\n")
            # print context around the match
            start = max(0, idx - 5)
            end = min(len(lines), idx + 20)
            f_out.write(f"--- Context for line {idx+1} ---\n")
            for i in range(start, end):
                f_out.write(f"  {i+1}: {lines[i]}\n")
            f_out.write("=" * 40 + "\n")
