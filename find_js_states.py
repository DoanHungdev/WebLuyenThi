import re
import os

target = r"D:\Project\WebLuyenThi\frontend\index.html"

with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for functions related to authentication, curriculum, students
functions_to_find = [
    r"function\s+login\s*\(",
    r"window\.login\s*=",
    r"function\s+logout\s*\(",
    r"window\.logout\s*=",
    r"function\s+renderAdminStudents\s*\(",
    r"function\s+saveCurriculumChanges\s*\(",
    r"function\s+updateLessonProgress\s*\(",
    r"function\s+toggleLessonStatus\s*\(",
    r"localStorage\.getItem",
    r"localStorage\.setItem",
]

out_path = r"C:\Users\admin\.gemini\antigravity\scratch\js_states_output.txt"
with open(out_path, 'w', encoding='utf-8') as f_out:
    for pattern in functions_to_find:
        matches = list(re.finditer(pattern, content))
        f_out.write(f"Pattern '{pattern}' matches: {len(matches)}\n")
        for m in matches:
            start = max(0, m.start() - 200)
            end = min(len(content), m.end() + 600)
            f_out.write(f"--- Context (Position: {m.start()}): ---\n")
            f_out.write(content[start:end])
            f_out.write("\n=========================================\n\n")

print("Done writing to js_states_output.txt")
