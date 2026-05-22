import os

src = r"C:\Users\admin\Downloads\HSA_Roadmap_Sheet.html"
dest = r"D:\Project\WebLuyenThi\frontend\index.html"

if not os.path.exists(src):
    print(f"ERROR: Source HTML not found at {src}")
    exit(1)

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

# Perform branding replacements
# Let's list common branding text strings to replace in HTML content:
replacements = {
    "LAB Academy": "Skibidi Study",
    "LAB ACADEMY": "SKIBIDI STUDY",
    "lab academy": "skibidi study",
    "CÙNG LAB": "CÙNG SKIBIDI STUDY",
    "Cùng LAB": "Cùng Skibidi Study",
    "Đội ngũ LAB": "Đội ngũ Skibidi Study",
    "Giáo viên LAB": "Giáo viên Skibidi Study",
    "học cùng LAB": "học cùng Skibidi Study",
    "ôn thi cùng LAB": "ôn thi cùng Skibidi Study",
    "chinh phục 80+ tsa cùng lab": "chinh phục 80+ tsa cùng Skibidi Study",
    "CHINH PHỤC 80+ TSA CÙNG LAB": "CHINH PHỤC 80+ TSA CÙNG SKIBIDI STUDY",
}

for old, new in replacements.items():
    html = html.replace(old, new)

# Let's search if there are other LAB references in headers or title tags.
# For example, <title> or <h1> or similar.
html = html.replace("LAB_Roadmap", "Skibidi_Study_Roadmap")
html = html.replace("LAB Roadmap", "Skibidi Study Roadmap")

with open(dest, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Frontend migrated and branded to Skibidi Study successfully at: {dest}")
