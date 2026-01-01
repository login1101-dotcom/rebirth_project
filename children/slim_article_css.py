
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def slim_article_headers(style_path):
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update .single-post header.bg-styled padding and margin
    # From: padding: 2rem; margin-bottom: 2rem;
    # To: padding: 1.2rem 1.5rem; margin-bottom: 1.5rem;
    content = re.sub(
        r'\.single-post header\.bg-styled\s*{[^}]*}',
        '.single-post header.bg-styled {\n    padding: 1rem 1.5rem;\n    border-radius: 12px;\n    margin-bottom: 1.5rem;\n}',
        content
    )

    # 2. Update .single-post h1 font size
    # From: font-size: 2.5rem;
    # To: font-size: 1.6rem;
    content = re.sub(
        r'\.single-post h1\s*{[^}]*}',
        '.single-post h1 {\n    font-size: 1.6rem;\n    font-weight: 700;\n    margin: 0.5rem 0;\n    line-height: 1.4;\n}',
        content
    )
    
    # 3. Adjust .article-meta inside single-post if needed
    # (Already handled reasonably, but ensuring it's compact)

    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    for item in os.listdir(base_dir):
        site_dir = os.path.join(base_dir, item)
        if not os.path.isdir(site_dir): continue
        
        style_p = os.path.join(site_dir, "style.css")
        if os.path.exists(style_p):
            slim_article_headers(style_p)
            print(f"Slimmed article header in {item}")

if __name__ == "__main__":
    main()
