target = r"D:\Project\WebLuyenThi\frontend\index.html"

with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("function initSystem()")
if idx == -1:
    print("Cannot find initSystem!")
    exit(1)

out_path = r"C:\Users\admin\.gemini\antigravity\scratch\initSystem_output.txt"
with open(out_path, 'w', encoding='utf-8') as f_out:
    f_out.write(content[idx:idx+4000])

print("Done writing initSystem block.")
