import os
import re

LAB_DIR = "/Users/jono/Desktop/rebirth_project/children/rebirth_child_typing"

def get_nav_items(current_filename):
    def is_active(target):
        return "active" if current_filename == target else ""

    home_cls = f" {is_active('index.html')}"
    daily_cls = f"nav-daily {is_active('category_daily.html')}"
    
    # Analysis (Restored)
    analysis_cls = f"nav-analysis {is_active('category_analysis.html')}"
    
    tools_cls = f"nav-tools {is_active('category_tools.html')}"

    items = [
        f'<li><a class="{home_cls}" href="index.html">ホーム</a></li>',
        f'<li><a class="{daily_cls}" href="category_daily.html">練習</a></li>',
        f'<li><a class="{analysis_cls}" href="category_analysis.html">分析</a></li>',
        f'<li><a class="{tools_cls}" href="category_tools.html">Typing Master Neo</a></li>',
        '<li><a href="http://localhost:8000" target="_blank" style="background:#00796b; color:white; padding:5px 12px; border-radius:4px; font-weight:bold; display:inline-block; line-height:normal; margin-left:5px;">NEO</a></li>',
        f'<li><a class="" href="../../index.html">← Project Hub</a></li>'
    ]
    
    return "\n                    ".join(items)

def restore_analysis_menu():
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
        pattern = re.compile(r'(<nav class="main-nav">\s*<ul>)(.*?)(</ul>)', re.DOTALL | re.IGNORECASE)
        
        match = pattern.search(content)
        if match:
            new_items = get_nav_items(filename)
            new_block = f"{match.group(1)}\n                    {new_items}\n                {match.group(3)}"
            content = pattern.sub(new_block, content)
            
            if content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                updates.append(filename)
                count += 1
        else:
             pass 

    print(f"Restored 'Analysis' in {count} files: {updates}")

if __name__ == "__main__":
    restore_analysis_menu()
