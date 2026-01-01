
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def embolden_article_headers(style_path):
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the base styled header to have a shadow and a left border
    content = re.sub(
        r'\.single-post header\.bg-styled\s*{[^}]*}',
        '.single-post header.bg-styled {\n    padding: 1.5rem 2rem;\n    border-radius: 12px;\n    margin-bottom: 2rem;\n    box-shadow: 0 4px 15px rgba(0,0,0,0.05);\n    border-left: 8px solid currentColor;\n}',
        content
    )

    # 2. Make the background gradients slightly more vibrant/distinct for each category
    # We'll override the bg-xxx classes to be more 'obvious'
    
    # Typing Lab / English Gym / etc often use these names
    # I'll update the standard light backgrounds to be slightly deeper.
    
    replacements = {
        # Blue (Daily / Reading / Listening)
        '#eff6ff, #dbeafe': '#dbeafe, #bfdbfe',
        # Red (Analysis / Writing / Speaking)
        '#fef2f2, #fee2e2': '#fee2e2, #fecaca',
        # Slate/Grey (Tools / Others)
        '#f8fafc, #e2e8f0': '#e2e8f0, #cbd5e1',
        # Manga Practice (Greenish/Yellowish?) - Let's check common ones
        '#f7fee7, #ecfccb': '#ecfccb, #d9f99d',
        # Manga Works (Purple/Indigo?)
        '#f5f3ff, #ede9fe': '#ede9fe, #ddd6fe'
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    for item in os.listdir(base_dir):
        site_dir = os.path.join(base_dir, item)
        if not os.path.isdir(site_dir): continue
        
        style_p = os.path.join(site_dir, "style.css")
        if os.path.exists(style_p):
            embolden_article_headers(style_p)
            print(f"Emboldened article headers in {item}")

if __name__ == "__main__":
    main()
