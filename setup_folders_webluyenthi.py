import os
import shutil

dirs = [
    r"D:\Project\WebLuyenThi",
    r"D:\Project\WebLuyenThi\backend",
    r"D:\Project\WebLuyenThi\backend\db",
    r"D:\Project\WebLuyenThi\backend\routes",
    r"D:\Project\WebLuyenThi\frontend"
]

# Create new directory structure
for d in dirs:
    if not os.path.exists(d):
        os.makedirs(d)
        print(f"Created directory: {d}")
    else:
        print(f"Directory already exists: {d}")

# Clean up old unused backend/frontend folders in D:\Project if they exist
old_backend = r"D:\Project\backend"
old_frontend = r"D:\Project\frontend"

if os.path.exists(old_backend):
    try:
        shutil.rmtree(old_backend)
        print(f"Removed old backend directory: {old_backend}")
    except Exception as e:
        print(f"Could not remove old backend: {e}")

if os.path.exists(old_frontend):
    try:
        shutil.rmtree(old_frontend)
        print(f"Removed old frontend directory: {old_frontend}")
    except Exception as e:
        print(f"Could not remove old frontend: {e}")
