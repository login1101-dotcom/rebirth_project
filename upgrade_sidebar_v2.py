import os
import re

CHILDREN_DIR = "/Users/jono/Desktop/rebirth_project/children"

def process_child_site(child_name):
    site_path = os.path.join(CHILDREN_DIR, child_name)
    if not os.path.isdir(site_path):
        return

    index_path = os.path.join(site_path, "index.html")
    if not os.path.exists(index_path):
        print(f"Skipping {child_name}: No index.html")
        return

    print(f"Processing {child_name}...")

    # 1. Extract Categories from index.html
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the Categories widget
    # Looking for <h3 ...>Categories</h3> ... <ul ...> ... </ul>
    # This acts as a parser to find existing items
    cat_section_match = re.search(r'(<h3[^>]*>Categories</h3>\s*<ul[^>]*>)(.*?)(</ul>)', content, re.DOTALL)
    
    categories = []
    
    if cat_section_match:
        ul_content = cat_section_match.group(2)
        # Parse li items
        # Pattern: <a href="(.*?)".*?class="(.*?)".*?>(.*?)</a>
        # Handles cases with/without class
        li_pattern = re.compile(r'<a\s+(?:class="([^"]*)"\s+)?href="([^"]+)"(?:\s+class="([^"]*)")?[^>]*>(.*?)</a>')
        
        for m in li_pattern.finditer(ul_content):
            cls1 = m.group(1)
            href = m.group(2)
            cls2 = m.group(3)
            full_text = m.group(4)
            
            cls = cls1 if cls1 else (cls2 if cls2 else "")
            
            # Extract name and count from text "Name (N)"
            text_match = re.match(r'(.*?)\s*\((\d+)\)', full_text)
            if text_match:
                name = text_match.group(1).strip()
                count = text_match.group(2)
            else:
                name = full_text.strip()
                count = "0"
            
            # Clean up class (remove 'active' if present to avoid sticking it permanently)
            cls_list = [c for c in cls.split() if c != 'active']
            cls_clean = " ".join(cls_list)
            
            categories.append({
                "name": name,
                "link": href,
                "count": int(count),
                "className": cls_clean
            })
            
        print(f"  Found {len(categories)} categories.")
    else:
        print("  Could not find Categories section in index.html")
        # Fallback manual definition could go here but let's rely on extraction
        return

    # 2. Generate sidebar.js
    js_content = """document.addEventListener('DOMContentLoaded', function() {
    const categories = ["""
    
    for cat in categories:
        js_content += f"""
        {{ name: "{cat['name']}", link: "{cat['link']}", count: {cat['count']}, className: "{cat['className']}" }},"""
    
    js_content += """
    ];

    const currentPath = window.location.pathname.split('/').pop();
    const listContainer = document.getElementById('category-list');
    
    if (listContainer) {
        const ul = document.createElement('ul');
        ul.style.listStyle = 'none';
        ul.style.lineHeight = '2';
        
        categories.forEach(cat => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = cat.link;
            a.textContent = `${cat.name} (${cat.count})`;
            if (cat.className) a.className = cat.className;
            
            // Simple active check
            if (currentPath === cat.link) {
                a.classList.add('active');
            }
            
            li.appendChild(a);
            ul.appendChild(li);
        });
        
        listContainer.appendChild(ul);
    }
});
"""
    
    js_path = os.path.join(site_path, "sidebar.js")
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"  Created sidebar.js")

    # 3. Update all HTML files in the directory
    for fname in os.listdir(site_path):
        if fname.endswith(".html"):
            fpath = os.path.join(site_path, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # Replace the UL block with div
            # Use stricter regex to only target the Categories widget
            # Search for: <h3 ...>Categories</h3> ... </ul>
            
            # We need to preserve the <h3...>Categories</h3> part, but replace the <ul>...</ul> following it.
            # However, sometimes there's whitespace.
            
            pattern = r'(<h3[^>]*>Categories</h3>)(\s*)<ul[^>]*>.*?</ul>'
            replacement = r'\1\2<div id="category-list"></div>'
            
            new_html, num_subs = re.subn(pattern, replacement, html, flags=re.DOTALL)
            
            if num_subs > 0:
                # Add script tag if not present
                if "sidebar.js" not in new_html:
                    if "</body>" in new_html:
                        new_html = new_html.replace("</body>", '<script src="sidebar.js"></script>\n</body>')
                    else:
                        new_html += '\n<script src="sidebar.js"></script>'
                
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_html)
                print(f"  Updated {fname}")
            else:
                # Some files might not have sidebar (e.g. specialized pages), that's fine
                pass

def main():
    if not os.path.exists(CHILDREN_DIR):
        print("Children directory not found.")
        return

    for item in os.listdir(CHILDREN_DIR):
        process_child_site(item)

if __name__ == "__main__":
    main()
