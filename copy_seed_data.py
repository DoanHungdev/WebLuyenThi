import shutil
import os

src = r"C:\Users\admin\.gemini\antigravity\brain\603d9c03-4d2b-41ab-b115-20923d981705\scratch\all_curriculums.json"
dest = r"D:\Project\WebLuyenThi\backend\db\all_curriculums.json"

if os.path.exists(src):
    shutil.copy(src, dest)
    print(f"Copied seed data from {src} to {dest}")
else:
    print(f"ERROR: Seed data not found at {src}")
