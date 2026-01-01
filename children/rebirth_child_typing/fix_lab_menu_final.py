import os
import re

LAB_DIR = "/Users/jono/Desktop/rebirth_project/children/rebirth_child_typing"

def get_nav_items(current_filename):
    # Helper to check active state
    def is_active(target):
        return "active" if current_filename == target else ""

    # Items definitions
    # (Label, href, class_list)
    # We want to preserve specific classes like 'nav-daily' if they are essential.
    # From previous observation: 
    # Practice -> nav-daily
    # Tools -> nav-tools
    
    # Home
    home_cls = f" {is_active('index.html')}"
    
    # Practice
    daily_cls = f"nav-daily {is_active('category_daily.html')}"
    
    # Tools (Typing Master Neo)
    tools_cls = f"nav-tools {is_active('category_tools.html')}"

    items = [
        f'<li><a class="{home_cls}" href="index.html">ホーム</a></li>',
        f'<li><a class="{daily_cls}" href="category_daily.html">練習</a></li>',
        # Analysis removed
        f'<li><a class="{tools_cls}" href="category_tools.html">Typing Master Neo</a></li>',
        # NEO Button
        '<li><a href="http://localhost:8000" target="_blank" style="background:#00796b; color:white; padding:5px 12px; border-radius:4px; font-weight:bold; display:inline-block; line-height:normal; margin-left:5px;">NEO</a></li>',
        f'<li><a class="" href="../../rebirth_parent/index.html">← Project Hub</a></li>'
    ]
    
    return "\n                    ".join(items)

def update_all_lab_menus():
    count = 0
    updates = []
    
    for filename in os.listdir(LAB_DIR):
        if not filename.endswith(".html"):
            continue
            
        filepath = os.path.join(LAB_DIR, filename)
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            continue
            
        original = content
        
        # Regex to capture the UL block inside nav
        # <nav class="main-nav">\s*<ul>(.*?)</ul>
        pattern = re.compile(r'(<nav class="main-nav">\s*<ul>)(.*?)(</ul>)', re.DOTALL | re.IGNORECASE)
        
        match = pattern.search(content)
        if match:
            # Generate new list items
            new_items = get_nav_items(filename)
            
            # Reconstruct the block
            # group(1) is "<nav ... <ul>"
            # group(3) is "</ul>"
            new_block = f"{match.group(1)}\n                    {new_items}\n                {match.group(3)}"
            
            # Replace
            content = pattern.sub(new_block, content)
            
            if content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                updates.append(filename)
                count += 1
        else:
            print(f"Skipping {filename} (Nav structure not found)")

    print(f"Updated {count} files: {updates}")

if __name__ == "__main__":
    update_all_lab_menus()
