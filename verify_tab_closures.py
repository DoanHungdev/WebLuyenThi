import re
import os

target = r"C:\Users\admin\Downloads\HSA_Roadmap_Sheet.html"

with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

idx_students = content.find('<div id="adminTabContent_students"')
idx_curriculum = content.find('id="adminTabContent_curriculum"')
idx_reports = content.find('id="adminTabContent_reports"')

out_path = r"C:\Users\admin\.gemini\antigravity\scratch\verify_tab_closures_output.txt"
with open(out_path, 'w', encoding='utf-8') as f_out:
    f_out.write(f"Students index: {idx_students}\n")
    f_out.write(f"Curriculum index: {idx_curriculum}\n")
    f_out.write(f"Reports index: {idx_reports}\n\n")
    
    if idx_curriculum != -1:
        f_out.write("--- Snippet before adminTabContent_curriculum ---\n")
        f_out.write(content[idx_curriculum-400:idx_curriculum+100])
        f_out.write("\n\n")
        
    if idx_reports != -1:
        f_out.write("--- Snippet before adminTabContent_reports ---\n")
        f_out.write(content[idx_reports-400:idx_reports+100])
        f_out.write("\n\n")

print("Done writing to verification file.")
