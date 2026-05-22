import re

target = r"D:\Project\WebLuyenThi\frontend\index.html"
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

out_path = r"C:\Users\admin\.gemini\antigravity\scratch\find_all_api_methods_output.txt"
with open(out_path, 'w', encoding='utf-8') as f_out:
    def find_func(name):
        f_out.write(f"=== SEARCHING FOR: {name} ===\n")
        matches = []
        # Search for function declarations or assignments
        p1 = re.compile(rf"(function\s+{name}\s*\(|window\.{name}\s*=)", re.IGNORECASE)
        for idx, line in enumerate(lines):
            if p1.search(line):
                matches.append(idx)
                f_out.write(f"Line {idx+1}: {line}\n")
        
        # If no match, just look for text match
        if not matches:
            for idx, line in enumerate(lines):
                if name in line:
                    matches.append(idx)
                    f_out.write(f"Line {idx+1} (substring): {line[:120]}\n")
        
        # For each match, print a block of 100 lines around it
        for m in matches[:3]:
            start = max(0, m - 10)
            end = min(len(lines), m + 100)
            f_out.write(f"\n--- Context for {name} (lines {start+1} to {end+1}) ---\n")
            for i in range(start, end):
                f_out.write(f"{i+1}: {lines[i]}\n")
            f_out.write("-" * 50 + "\n")

    # Let's search for the requested functions
    funcs = [
        "submitLogin",
        "initSystem",
        "loadProgress",
        "saveProgress",
        "renderAdminStudents",
        "saveCurriculumChanges",
        "toggleLessonStatus"
    ]

    for f in funcs:
        find_func(f)
