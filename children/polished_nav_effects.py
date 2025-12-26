
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def polished_nav_update(site_dir):
    style_path = os.path.join(site_dir, "style.css")
    if not os.path.exists(style_path): return

    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the base .main-nav a to include the polished transition and display
    # We'll replace the existing block if found, or just append a better one.
    # Find: .main-nav a { ... }
    content = re.sub(r'\.main-nav a\s*\{[^}]*\}', 
                     '.main-nav a {\n    font-weight: 500;\n    color: var(--text-light);\n    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);\n    display: inline-block;\n    position: relative;\n}', 
                     content)

    # 2. Update Hover/Active behavior (Up and Highlight)
    # We find .main-nav a:hover, .main-nav a.active and replace it
    content = re.sub(r'\.main-nav a:hover,\s*\.main-nav a\.active\s*\{[^}]*\}',
                     '.main-nav a:hover,\n.main-nav a.active {\n    color: var(--primary);\n    transform: translateY(-4px) scale(1.15);\n    font-weight: 800;\n    text-shadow: 0 4px 10px rgba(0,0,0,0.1);\n}',
                     content)

    # 3. Handle Category Colors - ALWAYS colored
    # We ensure .nav-xxx { color: var(--color-xxx) !important; } exists and is independent of hover
    # I'll look for the Category Colors section and strengthen it.
    
    # First, cleaning up any double definitions my previous script might have added
    content = re.sub(r'\.nav-[a-z0-9_-]+\s*{\n\s*color: var\(--color-[a-z0-9_-]+\) !important;\n\n}\n\n', '', content)

    # Now, find all --color-xxx variables and create .nav-xxx rules
    colors = re.findall(r'--color-([a-z0-9_-]+):', content)
    nav_rules = "/* Always Colored Category Nav */\n"
    for c in colors:
        if f'.nav-{c}' not in content:
            nav_rules += f'.nav-{c} {{ color: var(--color-{c}) !important; }}\n'
        else:
            # If it already exists, ensure it's not just for hover
            # (Handled by the fact we are searching for just the class)
            pass
    
    # Append nav rules if any
    if nav_rules != "/* Always Colored Category Nav */\n":
        content += "\n" + nav_rules

    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # 4. HTML Side: Standardize links and set Active
    for fname in os.listdir(site_dir):
        if not fname.endswith(".html"): continue
        fpath = os.path.join(site_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()

        # Add classes to navigation links based on their href (category_name.html -> nav-name)
        # Regex to find <a> tags in nav
        def link_fixer(match):
            href = match.group(2)
            # category_reading.html -> reading
            m = re.match(r'category_([a-z0-9_-]+)\.html', href)
            cat_name = m.group(1) if m else None
            
            # If we already have a class, don't double it unless it's missing the nav-xxx
            tag_open = match.group(1)
            rest = match.group(3)
            
            # If current page matches href, add .active
            is_active = (href == fname)
            
            new_classes = []
            if cat_name: new_classes.append(f"nav-{cat_name}")
            if is_active: new_classes.append("active")
            
            if not new_classes:
                return match.group(0)
            
            # If class exists
            if 'class="' in tag_open:
                # Append to existing class
                fixed = re.sub(r'class="([^"]*)"', r'class="\1 ' + " ".join(new_classes) + r'"', tag_open)
            else:
                fixed = tag_open + f' class="{" ".join(new_classes)}"'
            
            # Clean up duplicate classes (rudimentary)
            fixed = fixed.replace('  ', ' ').replace('active active', 'active')
            
            return f"{fixed} href=\"{href}\"{rest}"

        # Target <a> tags inside <nav class="main-nav">
        nav_pattern = r'(<nav class="main-nav">.*?</nav>)'
        nav_match = re.search(nav_pattern, html, re.DOTALL)
        if nav_match:
            nav_content = nav_match.group(1)
            # Remove any existing 'active' from all links in THIS nav first to be safe
            nav_content = re.sub(r'class="([^"]*) active([^"]*)"', r'class="\1\2"', nav_content)
            nav_content = re.sub(r'class="active "', r'class="', nav_content)
            nav_content = re.sub(r' class="active"', r'', nav_content)
            
            # Now add classes properly
            nav_content = re.sub(r'(<a\s+[^>]*?)href="([^"]*)"([^>]*>)', link_fixer, nav_content)
            
            html = html.replace(nav_match.group(1), nav_content)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)

def main():
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            print(f"Polishing {item}...")
            polished_nav_update(site_path)

if __name__ == "__main__":
    main()
