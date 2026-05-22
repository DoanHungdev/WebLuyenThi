target = r"D:\Project\WebLuyenThi\frontend\index.html"
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

for idx, line in enumerate(lines):
    if "<script" in line:
        print(f"Line {idx+1}: {line[:120]}")
    if "let activeCurriculum" in line or "var activeCurriculum" in line or "const activeCurriculum" in line:
        print(f"Line {idx+1}: {line[:120]}")
    if "let progressState" in line or "var progressState" in line or "const progressState" in line:
        print(f"Line {idx+1}: {line[:120]}")
