
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def extract_card_info(index_content):
    # Map title to (cat_name, cat_slug)
    # Using regex to find cards
    cards = re.findall(r'<article class="article-card".*?</article>', index_content, re.DOTALL)
    mapping = {}
    for card in cards:
        t_m = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card, re.DOTALL)
        c_m = re.search(r'class="cat text-([a-z0-9_-]+)".*?>\s*(.*?)\s*</a>', card, re.DOTALL)
        href_m = re.search(r'href="([^"]*\.html)"', card)
        
        if t_m and c_m and href_m:
            title = t_m.group(1).strip()
            slug = c_m.group(1).strip()
            name = c_m.group(2).strip()
            href = href_m.group(1).strip()
            mapping[href] = {"title": title, "slug": slug, "name": name}
    return mapping

def sync_all_articles():
    for item in os.listdir(base_dir):
        site_dir = os.path.join(base_dir, item)
        if not os.path.isdir(site_dir): continue
        
        index_p = os.path.join(site_dir, "index.html")
        if not os.path.exists(index_p): continue
        
        with open(index_p, 'r', encoding='utf-8') as f:
            idx_c = f.read()
        
        info_map = extract_card_info(idx_c)
        
        for href, data in info_map.items():
            fpath = os.path.join(site_dir, href)
            if not os.path.exists(fpath): continue
            
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. Update Header Background
            content = re.sub(r'class="bg-styled bg-[a-z0-9_-]+"', f'class="bg-styled bg-{data["slug"]}"', content)
            
            # 2. Update Category Text and Link
            # Pattern: class="cat text-[a-z0-9_-]+".*?>.*?</a>
            content = re.sub(r'class="cat text-[a-z0-9_-]+"(.*?>).*?</a>', 
                             f'class="cat text-{data["slug"]}"\\1{data["name"]}</a>', content)
            
            # 3. Update Breadcrumb if exists
            # Example: Home > Daily Log > Day 14
            # We can't perfectly guess this but we can try to replace the category link part
            # Look for </a> > CategoryName > ...
            
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Synced {item}/{href} to {data['slug']} ({data['name']})")

if __name__ == "__main__":
    sync_all_articles()
