
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def fix_title_colors_final(site_dir):
    # 1. Collect category info from index.html (Source of Truth)
    index_path = os.path.join(site_dir, "index.html")
    if not os.path.exists(index_path): return

    with open(index_path, 'r', encoding='utf-8') as f:
        idx_content = f.read()
    
    # Map title to category slug
    cards = re.findall(r'<article class="article-card".*?</article>', idx_content, re.DOTALL)
    title_to_slug = {}
    for card in cards:
        t_m = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card, re.DOTALL)
        c_m = re.search(r'class="cat text-([a-z0-9_-]+)"', card)
        href_m = re.search(r'href="([^"]*\.html)"', card)
        
        if t_m and c_m and href_m:
            title = t_m.group(1).strip()
            slug = c_m.group(1).strip()
            href = href_m.group(1)
            title_to_slug[href] = slug # Use href as key to be safer

    # 2. Update all html files based on this mapping
    for fname in os.listdir(site_dir):
        if not fname.endswith(".html") or not (fname.startswith("post_") or fname.startswith("article")): continue
        
        fpath = os.path.join(site_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the slug for this specific file
        # We check mapping by filename
        if fname in title_to_slug:
            correct_slug = title_to_slug[fname]
            header_class = f"bg-{correct_slug}"
            
            # Force update the header class
            # Pattern: <header class="bg-styled ...">
            # We want to ensure it is <header class="bg-styled {header_class}">
            if 'class="bg-styled' in content:
                content = re.sub(r'class="bg-styled [^"]*"', f'class="bg-styled {header_class}"', content)
            
            # Also ensure the meta text color is updated if it exists
            # e.g. <span class="cat text-diet">
            content = re.sub(r'class="cat text-[a-z0-9_-]+"', f'class="cat text-{correct_slug}"', content)

            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            print(f"Fixing {item}...")
            fix_title_colors_final(site_path)
