
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

# Regex to find the <header> inside .single-post
# We want to change <header> to <header class="bg-primary-soft"> or similar,
# but we need to know WHICH category color to use.
# Since we are automating, we will try to detect the category class used in the "article-meta" link inside the header.
# e.g., <a href="..." class="cat text-daily">Daily</a> -> implied bg-daily.

def apply_header_bg(dir_path):
    article_path = os.path.join(dir_path, "article.html")
    style_path = os.path.join(dir_path, "style.css")
    
    if not os.path.exists(article_path) or not os.path.exists(style_path):
        return

    # 1. Update style.css to support colored header
    with open(style_path, 'r', encoding='utf-8') as f:
        css = f.read()

    # Modify .single-post header to accept padding/radius if colored
    # We'll just append a rule that makes the header look nice if it has a background.
    header_style = """
/* Styled Article Header */
.single-post header.bg-styled {
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
}
"""
    if ".single-post header.bg-styled" not in css:
        with open(style_path, 'a', encoding='utf-8') as f:
            f.write(header_style)

    # 2. Update article.html to add appropriate class
    with open(article_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the category class used in the meta tag
    # Looking for: class="cat text-([a-z]+)"
    match = re.search(r'class="cat text-([a-z]+)"', html)
    
    if match:
        cat_slug = match.group(1)
        bg_class = f"bg-{cat_slug}"
        
        # Now find the header tag inside single-post
        # <article class="single-post"> ... <header>
        
        # We replace <header> with <header class="bg-styled bg-{cat_slug}">
        # Be careful not to replace the site main header. We target the one after single-post.
        
        # Regex for single-post header
        # Context: <article class="single-post">\s*<header>
        
        html_new = re.sub(
            r'(<article class="single-post">\s*)<header>', 
            f'\\1<header class="bg-styled {bg_class}">', 
            html
        )
        
        if html_new != html:
            with open(article_path, 'w', encoding='utf-8') as f:
                f.write(html_new)
            print(f"Applied header color ({bg_class}) to: {os.path.basename(dir_path)}")
        else:
            print(f"Header already styled or not found in: {os.path.basename(dir_path)}")
            
    else:
        print(f"Could not detect category in: {os.path.basename(dir_path)}")

def main():
    if not os.path.exists(base_dir):
        return
    for item in os.listdir(base_dir):
        full_path = os.path.join(base_dir, item)
        if os.path.isdir(full_path):
            apply_header_bg(full_path)

if __name__ == "__main__":
    main()
