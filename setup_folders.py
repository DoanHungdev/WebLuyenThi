import os

dirs = [
    r"D:\Project",
    r"D:\Project\backend",
    r"D:\Project\backend\db",
    r"D:\Project\backend\routes",
    r"D:\Project\frontend"
]

for d in dirs:
    if not os.path.exists(d):
        os.makedirs(d)
        print(f"Created directory: {d}")
    else:
        print(f"Directory already exists: {d}")
