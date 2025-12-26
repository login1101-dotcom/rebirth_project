
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def final_polish_site(site_dir):
    style_path = os.path.join(site_dir, "style.css")
    if not os.path.exists(style_path): return

    with open(style_path, 'r', encoding='utf-8') as f:
        css = f.read()

    # Find all category color variables
    color_vars = re.findall(r'--color-([a-z0-9_-]+):', css)
    
    category_overrides = ""
    for cv in color_vars:
        category_overrides += f".nav-{cv} {{ color: var(--color-{cv}) !important; }}\n"

    final_css_block = f"""
/* --- Final Refined Navigation UI --- */
.main-nav a {{
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    display: inline-block !important;
    text-decoration: none !important;
}}

.main-nav a:hover,
.main-nav a.active {{
    transform: translateY(-5px) scale(1.15) !important;
    font-weight: 800 !important;
    text-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}}

{category_overrides}
"""
    # Remove any old "Refined Navigation" blocks to avoid bloat
    css = re.sub(r'/\* --- Final Refined Navigation UI --- \*/.*$', '', css, flags=re.DOTALL)
    css += "\n" + final_css_block
    
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(css)

    # HTML Fixes
    for fname in os.listdir(site_dir):
        if not fname.endswith(".html"): continue
        fpath = os.path.join(site_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()

        # 1. Fix duplicated classes (e.g., <a class="X" ... class="X">)
        html = re.sub(r'(<a\s+)(class="[^"]*")\s+href="([^"]*)"\s+class="[^"]*"', r'\1\2 href="\3"', html)

        # 2. Correctly set active class
        # First, strip 'active' from all links in nav
        nav_m = re.search(r'(<nav class="main-nav">.*?</nav>)', html, re.DOTALL)
        if nav_m:
            nav_html = nav_m.group(1)
            # Remove active class
            nav_html = re.sub(r'\s+active', '', nav_html)
            # Find the link matching current page
            # e.g. href="category_reading.html" on category_reading.html
            
            # Pattern to find the correct <a>
            # We must handle cases where index.html is the current page but nav has "Home" link
            search_page = fname
            
            p = re.compile(r'(<a\s+[^>]*href="' + re.escape(search_page) + r'"[^>]*)')
            if p.search(nav_html):
                # Add active
                if 'class="' in p.search(nav_html).group(1):
                    nav_html = p.sub(r'\1 class="active"', nav_html) # This is sloppy but let's refine
                    # Re-fix if we added double class
                    nav_html = re.sub(r'class="([^"]*)"\s+class="active"', r'class="\1 active"', nav_html)
                else:
                    nav_html = p.sub(r'\1 class="active"', nav_html)
            
            html = html.replace(nav_m.group(1), nav_html)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)

if __name__ == "__main__":
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            final_polish_site(site_path)
