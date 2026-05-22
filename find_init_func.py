target = r"D:\Project\WebLuyenThi\frontend\index.html"

with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for: "let savedCurriculum = localStorage.getItem('hsa_master_curriculum');"
idx = content.find("let savedCurriculum = localStorage.getItem('hsa_master_curriculum');")
if idx == -1:
    print("Cannot find savedCurriculum initialization!")
    exit(1)

# Print 1000 characters before this point to see the enclosing function header
print("Enclosing context of startup block:")
print(content[idx-1000:idx])
