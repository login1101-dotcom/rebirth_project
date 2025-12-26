
import os
import re

BASE_DIR = "/Users/jono/Desktop/rebirth_project/children"
TARGET_DIRS = [
    "rebirth_child_health",
    "rebirth_child_english",
    "rebirth_child_novel",
    "rebirth_child_manga",
    "rebirth_child_youtube"
]

def get_article_info(dir_path):
    articles = []
    # Scan for post_*.html files
    files = [f for f in os.listdir(dir_path) if f.startswith("post_") and f.endswith(".html") and "temp" not in f and "fix" not in f and "update" not in f]
    
    for f in files:
        # Extract number
        num_match = re.search(r'post_(\d+).html', f)
        if not num_match: continue
        num = int(num_match.group(1))
        
        path = os.path.join(dir_path, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Extract category from header class
        # Pattern: class="bg-styled bg-diet" or similar
        cat_match = re.search(r'class=["\']bg-styled bg-([a-z0-9_-]+)["\']', content)
        if not cat_match:
            # Fallback: try to find it in meta span like <span class="cat text-diet">
            cat_match = re.search(r'class=["\']cat text-([a-z0-9_-]+)["\']', content)
            
        category = cat_match.group(1) if cat_match else "unknown"
        
        articles.append({
            "filename": f,
            "number": num,
            "category": category
        })
    
    # Sort by number to ensure logical order (1 -> 2 -> 3)
    articles.sort(key=lambda x: x["number"])
    return articles

def generate_nav_html(prev_art, next_art, category_slug):
    color_var = f"var(--color-{category_slug})"
    
    # Previous Link
    if prev_art:
        prev_link = f'<a href="{prev_art["filename"]}" style="text-decoration: none; color: {color_var};">&laquo; 前の記事</a>'
    else:
        prev_link = '<span style="color: #ccc;">&laquo; 前の記事</span>'
        
    # Next Link
    if next_art:
        next_link = f'<a href="{next_art["filename"]}" style="text-decoration: none; color: {color_var};">次の記事 &raquo;</a>'
    else:
        next_link = '<span style="color: #ccc;">次の記事 &raquo;</span>'
    
    html = f'''
                    <div class="post-navigation" style="display: flex; justify-content: space-between; margin-bottom: 1rem; font-size: 0.9rem; font-weight: bold;">
                        {prev_link}
                        {next_link}
                    </div>'''
    return html

def process_directory(dirname):
    dir_path = os.path.join(BASE_DIR, dirname)
    if not os.path.exists(dir_path):
        print(f"Directory not found: {dirname}")
        return

    print(f"Processing {dirname}...")
    articles = get_article_info(dir_path)
    
    # Group by category
    cat_map = {}
    for a in articles:
        c = a["category"]
        if c not in cat_map: cat_map[c] = []
        cat_map[c].append(a)
    
    # Apply to files
    for a in articles:
        f_path = os.path.join(dir_path, a["filename"])
        cat = a["category"]
        siblings = cat_map.get(cat, [])
        
        if not siblings: continue
        
        try:
            curr_idx = siblings.index(a)
        except ValueError:
            continue
            
        prev_art = siblings[curr_idx - 1] if curr_idx > 0 else None
        next_art = siblings[curr_idx + 1] if curr_idx < len(siblings) - 1 else None
        
        # Generate Navigation HTML
        # Top: slightly different margins handling in logic if needed, but styling allows re-use if wrapper handles it.
        # But here I used explicit margins in the style str.
        # Top Nav
        top_nav = generate_nav_html(prev_art, next_art, cat)
        
        # Bottom Nav (Same HTML structure, maybe diff margins? In typing example, they were:
        # Top: margin-bottom: 1rem
        # Bottom: margin-top: 3rem; margin-bottom: 1rem
        
        # Let's adjust Generate function to take styles or specific margins?
        # Or just string replace margins.
        bottom_nav = top_nav.replace('margin-bottom: 1rem;', 'margin-top: 3rem; margin-bottom: 1rem;')
        
        with open(f_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # --- CLEANUP OLD NAV ---
        # Remove any existing post-navigation divs to avoid duplication
        # Regex for <div class="post-navigation" ... > ... </div>
        # Use DOTALL
        content = re.sub(r'<div class="post-navigation".*?</div>', '', content, flags=re.DOTALL)
        
        # --- INSERT TOP NAV ---
        # Find breadcrumb
        # <div class="breadcrumb" ... > ... </div>
        # Insert after it.
        # We look for the closing </div> of breadcrumb.
        
        # We can find `class="breadcrumb"` and then find the next `</div>`.
        if 'class="breadcrumb"' in content:
            # Robust insertion: 
            # Find the match, get end position.
            m = re.search(r'(<div class="breadcrumb".*?</div>)', content, re.DOTALL)
            if m:
                # Insert after match
                content = content[:m.end()] + '\n' + top_nav + content[m.end():]
        
        # --- INSERT BOTTOM NAV ---
        # Insert before closing </div> of post-content
        # Strategy: Find </article> and find the last </div> before it.
        # Assumption: The closing div of post-content is immediately before </article> (ignoring whitespace).
        
        # Search for pattern: </div>\s*</article>
        m_bottom = re.search(r'(</div>\s*</article>)', content, re.DOTALL)
        if m_bottom:
             # Insert nav before the group
             start_idx = m_bottom.start()
             content = content[:start_idx] + '\n' + bottom_nav + '\n' + content[start_idx:]
        
        # --- ENSURE SIDEBAR.JS ---
        if 'src="sidebar.js"' not in content:
             content = content.replace('</body>', '<script src="sidebar.js"></script>\n</body>')
             
        with open(f_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print(f"Updated {len(articles)} articles in {dirname}")

if __name__ == "__main__":
    for d in TARGET_DIRS:
        process_directory(d)
