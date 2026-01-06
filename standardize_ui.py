import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

def clean_nav_active(header_html):
    # Remove all "active" classes from nav links to start fresh
    header_html = re.sub(r'class="active site-brand"', 'class="site-brand"', header_html)
    header_html = re.sub(r'class="active"', '', header_html)
    # Also clean up potential double spaces
    header_html = re.sub(r'  +', ' ', header_html)
    return header_html

def set_nav_active(header_html, page_type, cat_id=None):
    # page_type: 'index', 'category', 'post'
    header_html = clean_nav_active(header_html)
    if page_type == 'index':
        # Home and Brand are active
        header_html = header_html.replace('class="site-brand"', 'class="active site-brand"')
        header_html = header_html.replace('href="index.html">ホーム', 'class="active" href="index.html">ホーム')
    elif page_type == 'category' and cat_id:
        # Specific category link is active
        pattern = rf'href="category_{cat_id}\.html"'
        header_html = re.sub(pattern, f'class="active" href="category_{cat_id}.html"', header_html)
    elif page_type == 'post':
        # No specific nav is active, or maybe Home? User likes consistency.
        pass
    return header_html

def process_project(proj_path):
    proj_name = os.path.basename(proj_path)
    index_path = os.path.join(proj_path, "index.html")
    if not os.path.exists(index_path): return

    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    # Extract Master Header and Footer
    header_match = re.search(r'<header>.*?</header>', index_content, re.DOTALL)
    footer_match = re.search(r'<footer.*?>.*?</footer>', index_content, re.DOTALL)
    
    if not header_match or not footer_match:
        print(f"Skipping {proj_name}: Couldn't find header/footer in index.html")
        return

    master_header = header_match.group(0)
    master_footer = footer_match.group(0)

    # Process all sub-pages
    for f in os.listdir(proj_path):
        if f == "index.html": continue
        if not f.endswith(".html"): continue
        
        file_path = os.path.join(proj_path, f)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Determine page type and cat_id
        page_type = 'post'
        cat_id = None
        if f.startswith("category_"):
            page_type = 'category'
            cat_id = f.replace("category_", "").replace(".html", "")
        
        # Prepare specific header
        page_header = set_nav_active(master_header, page_type, cat_id)

        # Replace Header
        new_content = re.sub(r'<header>.*?</header>', page_header, content, flags=re.DOTALL)
        # Replace Footer
        new_content = re.sub(r'<footer.*?>.*?</footer>', master_footer, new_content, flags=re.DOTALL)

        # Ensure Home/ホーム exists in nav if somehow lost (it shouldn't be if index.html has it)
        # But let's check the font size of the tagline in the site-brand
        # index.html has: style="font-size: 0.8rem; color: #64748b; margin-left: 10px; font-weight: normal;"
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
    
    print(f"Standardized header/footer for {proj_name}")

if __name__ == "__main__":
    for d in os.listdir(CHILDREN_DIR):
        p = os.path.join(CHILDREN_DIR, d)
        if os.path.isdir(p):
            process_project(p)
