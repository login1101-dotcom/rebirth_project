import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

posts = []
for root, dirs, files in os.walk(CHILDREN_DIR):
    for f in files:
        if f.startswith("post_") and f.endswith(".html"):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            title_match = re.search(r'<h1>(.*?)</h1>', content)
            title = re.sub(r'<.*?>', '', title_match.group(1)).strip() if title_match else "N/A"
            
            date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
            date = date_match.group(1) if date_match else "N/A"
            
            posts.append({
                "path": os.path.relpath(path, ROOT_DIR),
                "title": title,
                "date": date
            })

for p in sorted(posts, key=lambda x: x['path']):
    print(f"{p['path']} | {p['date']} | {p['title']}")
