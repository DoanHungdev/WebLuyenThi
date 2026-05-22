import re

target = r"D:\Project\WebLuyenThi\frontend\index.html"

with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for "progressState[" or "tsaProgressState[" to find how individual lesson checks are saved.
lines = content.split('\n')
for idx, line in enumerate(lines):
    if "progressState[" in line or "tsaProgressState[" in line or "saveProgress()" in line:
        print(f"Line {idx+1}: {line[:120]}")
