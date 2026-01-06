import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"

def fix_sidebar(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Target the categories widget
    # Find <h3 class="widget-title">Categories</h3> and replace until the end of the widget div
    new_content = re.sub(
        r'<h3 class="widget-title">Categories</h3>.*?</div>\s*</div>',
        '<h3 class="widget-title">Categories</h3>\n                <div id="category-list"></div>\n            </div>',
        content,
        flags=re.DOTALL
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

for root, dirs, files in os.walk(os.path.join(ROOT_DIR, "children")):
    for f in files:
        if f.endswith(".html") and (f.startswith("category_") or f == "index.html"):
            fix_sidebar(os.path.join(root, f))
