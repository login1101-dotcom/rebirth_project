import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"

for root, dirs, files in os.walk(os.path.join(ROOT_DIR, "children")):
    for f in files:
        if f.startswith("category_") and f.endswith(".html"):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Replace the entire category widget content with a single empty div
            new_content = re.sub(r'<div id="category-list">.*?</div>', '<div id="category-list"></div>', content, flags=re.DOTALL)
            
            with open(path, 'w', encoding='utf-8') as file:
                file.write(new_content)
