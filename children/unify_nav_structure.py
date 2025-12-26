
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def unify_navigation_content(site_dir):
    # 1. First, find a "SOURCE" navigation structure from index.html
    # because index.html usually has the most correct category lists.
    index_path = os.path.join(site_dir, "index.html")
    if not os.path.exists(index_path): return

    with open(index_path, 'r', encoding='utf-8') as f:
        idx_content = f.read()

    # Extract the <ul> content of the main-nav
    nav_match = re.search(r'<nav class="main-nav">\s*<ul>(.*?)</ul>\s*</nav>', idx_content, re.DOTALL)
    if not nav_match: return
    
    source_ul_content = nav_match.group(1).strip()
    
    # Ensure "ホーム" (Home) exists at the start of source_ul_content if it's not there
    if 'index.html' not in source_ul_content:
        home_li = '<li><a href="index.html">ホーム</a></li>'
        source_ul_content = home_li + "\n                    " + source_ul_content

    # Normalize name: "物語" -> "小説" for Novel Lab if detected
    if 'rebirth_child_novel' in site_dir:
        source_ul_content = source_ul_content.replace('物語', '小説')
        # Ensure the order is: ホーム, エッセイ, 小説, その他 (if exists), データ表示, Hub
        # This is harder to automate perfectly but we'll try to keep the unified source.

    # 2. Iterate all HTML files and swap their navigation with this "source_ul_content"
    for fname in os.listdir(site_dir):
        if not fname.endswith(".html"): continue
        fpath = os.path.join(site_dir, fname)
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace <ul>...</ul> inside <nav class="main-nav">
        # We use a pattern that catches the ul and its content
        new_content = re.sub(r'(<nav class="main-nav">\s*<ul[^>]*>).*?(</ul>\s*</nav>)', 
                             f'\\1\n                    {source_ul_content}\n                \\2', 
                             content, flags=re.DOTALL)
        
        # 3. Post-process: Set 'active' class correctly for the current page
        # Remove any existing active classes first
        new_content = re.sub(r'\s+active', '', new_content)
        
        # Add active to the link matching fname
        # Pattern: href="fname"
        search_href = f'href="{fname}"'
        if search_href in new_content:
            # Add class="active" or append to existing class
            # This handles both cases <a href="..."> and <a class="..." href="...">
            def active_adder(m):
                tag = m.group(0)
                if 'class="' in tag:
                    return re.sub(r'class="([^"]*)"', r'class="\1 active"', tag)
                else:
                    return tag.replace('href=', 'class="active" href=')
            
            new_content = re.sub(r'<a\s+[^>]*href="' + re.escape(fname) + r'"[^>]*>', active_adder, new_content)

        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)

if __name__ == "__main__":
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            unify_navigation_content(site_path)
