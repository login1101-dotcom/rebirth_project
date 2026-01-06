import os
import re

TARGET_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work/children/rebirth_child_reading"

def clean_reading_files():
    for f in os.listdir(TARGET_DIR):
        if not f.endswith(".html"): continue
        
        path = os.path.join(TARGET_DIR, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Regex to empty the category-list div
        # Matches <div id="category-list"> ... </div>
        # and replaces it with <div id="category-list"></div>
        
        pattern = r'<div id="category-list">.*?</div>'
        new_content = re.sub(pattern, '<div id="category-list"></div>', content, flags=re.DOTALL)
        
        if content != new_content:
            print(f"Cleaned sidebar in {f}")
            with open(path, 'w', encoding='utf-8') as file:
                file.write(new_content)

    # Delete old book_*.html files
    for f in ["book_nishida.html", "book_schrodinger.html", "book_yamamoto.html"]:
        p = os.path.join(TARGET_DIR, f)
        if os.path.exists(p):
            os.remove(p)
            print(f"Deleted old file {f}")

if __name__ == "__main__":
    clean_reading_files()
