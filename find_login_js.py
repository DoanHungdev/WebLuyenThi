import re

target = r"D:\Project\WebLuyenThi\frontend\index.html"

with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for "password" or "username" or "admin2026" or "class="modal" or similar in index.html to find how login works
lines = content.split('\n')
for idx, line in enumerate(lines):
    if "admin2026" in line or "submit" in line.lower() and "login" in line.lower() or "hsa_users_db" in line:
        print(f"Line {idx+1}: {line[:120]}")
