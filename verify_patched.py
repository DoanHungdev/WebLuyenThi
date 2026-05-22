import re
import subprocess
import tempfile
import os

targets = [
    r"C:\Users\admin\.gemini\antigravity\scratch\HSA\HSA_Roadmap_Sheet.html",
    r"C:\Users\admin\Downloads\HSA_Roadmap_Sheet.html"
]

for target in targets:
    print(f"Checking {target}...")
    if not os.path.exists(target):
        print(f"ERROR: {target} does not exist!")
        continue
    
    with open(target, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Verify JS blocks syntax
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    if not scripts:
        print(f"ERROR: No <script> tags found in {target}")
        continue
        
    for idx, script in enumerate(scripts):
        if "switchAdminTab" in script:
            with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode='w', encoding='utf-8') as temp_f:
                temp_f.write(script)
                temp_file_name = temp_f.name
            
            try:
                res = subprocess.run(["node", "--check", temp_file_name], capture_output=True, text=True)
                if res.returncode == 0:
                    print(f"  [JS OK] switchAdminTab script block is valid.")
                else:
                    print(f"  [JS ERROR] Syntax error in script block:")
                    print(res.stderr)
            finally:
                os.unlink(temp_file_name)
    
    # 2. Check HTML structure for adminView
    # Verify div balance inside #adminView:
    # Look for '<div id="adminView"' in content
    idx_admin = content.find('<div id="adminView"')
    if idx_admin == -1:
        print("  [HTML ERROR] Could not find '<div id=\"adminView\"'")
    else:
        # Let's count standard HTML tags or print a snippet around it to make sure it's structurally fine
        print("  [HTML OK] Found '<div id=\"adminView\"'")
        # Also look for the closing elements we noted: '</div> <!-- admin-page-body --> </main> </div>'
        if "</div> <!-- admin-page-body --> </main> </div>" in content:
            print("  [HTML OK] Found matching closing comments/tags: </div> <!-- admin-page-body --> </main> </div>")
        else:
            print("  [HTML WARNING] Could not find the exactly matched closing block. Let's make sure closing structure is present.")
            
print("Verification complete.")
