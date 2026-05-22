target = r"D:\Project\WebLuyenThi\frontend\index.html"

with open(target, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out_path = r"C:\Users\admin\.gemini\antigravity\scratch\toggle_snippet_output.txt"
with open(out_path, 'w', encoding='utf-8') as f_out:
    start = 14730
    end = 14780
    for i in range(start, min(end, len(lines))):
        f_out.write(f"Line {i+1}: {lines[i]}")

print("Done writing toggle snippet.")
