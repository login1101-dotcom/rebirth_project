
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def force_sync_colors(current_dir):
    index_path = os.path.join(current_dir, "index.html")
    if not os.path.exists(index_path): return

    with open(index_path, 'r', encoding='utf-8') as f:
        idx_content = f.read()
    
    # Extract cards and their links + category color
    # We look for <article class="article-card"> ... href="LINK" ... class="cat text-COLOR"
    cards = re.findall(r'<article class="article-card".*?</article>', idx_content, re.DOTALL)
    
    for card in cards:
        # Get the link in this card
        href_match = re.search(r'href="([^"]*\.html)"', card)
        # Get the color class (text-xxx)
        color_match = re.search(r'class="cat text-([a-z0-9_-]+)"', card)
        
        if href_match and color_match:
            target_file = href_match.group(1)
            cat_slug = color_match.group(1)
            bg_class = f"bg-{cat_slug}"
            
            fpath = os.path.join(current_dir, target_file)
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Force replace the header class
                # Find the article header (the one inside .single-post)
                if 'class="bg-styled' in content:
                    # Update existing
                    new_content = re.sub(r'class="bg-styled bg-[a-z0-9_-]+"', f'class="bg-styled {bg_class}"', content)
                else:
                    # Inject into the second header (article header)
                    parts = re.split(r'(<main[^>]*>)', content)
                    if len(parts) > 2:
                        parts[2] = parts[2].replace('<header>', f'<header class="bg-styled {bg_class}">', 1)
                        new_content = "".join(parts)
                    else:
                        new_content = content # skip
                
                if new_content != content:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"  Fixed {target_file} -> {bg_class}")

def main():
    for item in os.listdir(base_dir):
        full = os.path.join(base_dir, item)
        if os.path.isdir(full):
            print(f"Checking {item}...")
            force_sync_colors(full)

if __name__ == "__main__":
    main()
