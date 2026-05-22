import re
import os

target = r"C:\Users\admin\Downloads\HSA_Roadmap_Sheet.html"

if not os.path.exists(target):
    print("Target does not exist!")
    exit(1)

with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the adminView view section.
idx = content.find('<div id="adminView"')
if idx == -1:
    print("Cannot find #adminView")
    exit(1)

tokens = re.findall(r'<(div|/div|main|/main|aside|/aside|/section|section)(?:\s|>|/)', content[idx:idx+100000], re.IGNORECASE)

# Let's count open/close tokens specifically for adminView.
# We want to trace the nesting starting from '<div id="adminView"'.
# We open a div (adminView), then inside we open 'div' (admin-spa-container), then 'aside' (adminSidebar), then 'main' (admin-main-panel), etc.
# Let's see the sequence of tags:
# '<div id="adminView"' is a 'div' tag.
# Inside it, we have:
# - <div class="admin-spa-container"> (div)
# - <aside class="admin-sidebar" ...> (aside)
# - ... (nested elements inside aside, all divs open and close)
# - </aside>
# - <main class="admin-main-panel"> (main)
# - <div class="admin-top-bar">...</div> (div, /div)
# - <div class="admin-page-body"> (div)
# - <div class="admin-page-header">...</div> (div, /div)
# - <div id="adminTabContent_students" ...> ... </div> (div, /div)
# - <div id="adminTabContent_curriculum" ...> ... </div> (div, /div)
# - <div id="adminTabContent_reports" ...> ... </div> (div, /div)
# Then at the very end of adminView, what tags close?
# We need to close:
# 1. admin-page-body (div) -> </div>
# 2. admin-main-panel (main) -> </main>
# 3. admin-spa-container (div) -> </div>
# 4. adminView (div) -> </div>
# Let's see the actual closing tags at the end of adminView.
# Let's write a file with the snippet after reports to avoid terminal encoding errors.
idx_reports = content.find('id="adminTabContent_reports"')
if idx_reports != -1:
    snippet = content[idx_reports:idx_reports+4000]
    out_path = r"C:\Users\admin\.gemini\antigravity\scratch\check_reports_end.txt"
    with open(out_path, 'w', encoding='utf-8') as f_out:
        f_out.write(snippet)
    print(f"Successfully wrote reports end snippet to: {out_path}")
else:
    print("Could not find adminTabContent_reports")
