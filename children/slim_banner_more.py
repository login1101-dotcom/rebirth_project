
import os
import re

target_files = [
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_novel/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_health/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_english/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_youtube/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_manga/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_reading/article.html"
]

def slim_down_banner(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find height in style attribute of the banner
    # Currently looks like: height:180px; ... font-size:5rem;
    
    # Update Height to 120px
    content = re.sub(r'height:\s*\d+px', 'height:120px', content)
    
    # Update Font Size to 3rem (smaller icon)
    content = re.sub(r'font-size:\s*\d+rem', 'font-size:3rem', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Slimmed down: {os.path.basename(os.path.dirname(filepath))}")

for p in target_files:
    slim_down_banner(p)
