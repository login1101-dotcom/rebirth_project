
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def update_css_for_nav(style_path):
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add transition to all nav links
    if 'transition' not in content or '.main-nav a' not in content:
        # We might need to find where .main-nav a is defined and add transition
        content = content.replace('.main-nav a {', '.main-nav a {\n    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);')

    # 2. Add the "Active/Up" style
    # Base active style for standard links
    active_style = """
/* Navigation Active/Hover "Up" Effect */
.main-nav a {
    display: inline-block;
}

.main-nav a:hover,
.main-nav a.active {
    transform: translateY(-3px) scale(1.1);
    font-weight: 700;
}
"""
    if '.main-nav a.active' not in content:
        content += active_style

    # 3. Ensure Category Nav links are ALWAYS colored
    # We look for definitions like .nav-xxx:hover, .nav-xxx.active { color: var(--color-xxx) !important; }
    # and change them to .nav-xxx { color: var(--color-xxx) !important; }
    # Regex to catch .nav-xxxx:hover, .nav-xxxx.active { ... }
    pattern = re.compile(r'(\.nav-[a-z0-9_-]+):hover,\s*\1\.active\s*\{([^}]*)\}', re.DOTALL)
    
    def color_replacer(match):
        nav_class = match.group(1)
        styles = match.group(2)
        # Create a rule that applies the color always
        return f"{nav_class} {{\n{styles}\n}}\n\n{match.group(0)}"

    content = pattern.sub(color_replacer, content)

    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(content)

def update_html_nav_active(site_dir):
    # Find all html files
    for fname in os.listdir(site_dir):
        if not fname.endswith(".html"): continue
        fpath = os.path.join(site_dir, fname)
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Ensure Typing Lab special case: add nav classes if missing
        if 'rebirth_child_typing' in site_dir:
            content = content.replace('href="category_daily.html">', 'href="category_daily.html" class="nav-daily">')
            content = content.replace('href="category_analysis.html">', 'href="category_analysis.html" class="nav-analysis">')
            content = content.replace('href="category_tools.html">', 'href="category_tools.html" class="nav-tools">')

        # Generic: Remove all existing "active" classes in main-nav to reset
        content = re.sub(r'(<nav class="main-nav">.*?) class="active"', r'\1', content, flags=re.DOTALL)
        
        # Add active class to the link matching current page
        # Search for href="current_page" and add class="active" (or append to class if exists)
        esc_fname = re.escape(fname)
        
        # If the file is 'index.html', we usually don't have a nav link to index.html in the main nav? 
        # Actually some sites do.
        
        # Pattern to find the <a> tag with this href in the main-nav
        search_pattern = r'(<nav class="main-nav">.*?<a\s+[^>]*href="' + esc_fname + r'"[^>]*)'
        
        if re.search(search_pattern, content, re.DOTALL):
            # If it has a class attribute already
            if re.search(search_pattern + r'class="', content, re.DOTALL):
                content = re.sub(search_pattern + r'class="([^"]*)', r'\1class="\2 active', content, flags=re.DOTALL)
            else:
                # Add class attribute
                content = re.sub(search_pattern, r'\1 class="active"', content, flags=re.DOTALL)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            print(f"Updating {item}...")
            style_p = os.path.join(site_path, "style.css")
            if os.path.exists(style_p):
                update_css_for_nav(style_p)
            update_html_nav_active(site_path)

if __name__ == "__main__":
    main()
