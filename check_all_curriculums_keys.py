import json

path = r"D:\Project\WebLuyenThi\backend\db\all_curriculums.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Keys in all_curriculums.json:")
for k in data.keys():
    print(f" - {k}: chapters={len(data[k].get('chapters', {})) if isinstance(data[k], dict) else 'not a dict'}")
