import os
import re

LAB_DIR = "/Users/jono/Desktop/rebirth_project/children/rebirth_child_typing"

def get_nav_items(current_filename):
    def is_active(target):
        return "active" if current_filename == target else ""

    home_cls = f" {is_active('index.html')}"
    daily_cls = f"nav-daily {is_active('category_daily.html')}"
    analysis_cls = f"nav-analysis {is_active('category_analysis.html')}"
    tools_cls = f"nav-tools {is_active('category_tools.html')}"

    # Standardized LI items
    items = [
        f'<li><a class="{home_cls}" href="index.html">ホーム</a></li>',
        f'<li><a class="{daily_cls}" href="category_daily.html">練習</a></li>',
        f'<li><a class="{analysis_cls}" href="category_analysis.html">分析</a></li>',
        f'<li><a class="{tools_cls}" href="category_tools.html">Typing Master Neo</a></li>',
        '<li><a href="http://localhost:8000" target="_blank" style="background:#00796b; color:white; padding:5px 12px; border-radius:4px; font-weight:bold; display:inline-block; line-height:normal; margin-left:5px;">NEO</a></li>',
        f'<li><a class="" href="../../rebirth_parent/index.html">← Project Hub</a></li>'
    ]
    
    return "\n                    ".join(items)

def unify_lab_menus():
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
        
        # Regex to capture the whole NAV block
        # <nav class="main-nav"> ... </nav>
        # We replace the content inside <nav ...> with a standard <ul>...</ul>
        # We ignore what attributes the original <ul> had, to force uniformity.
        
        pattern = re.compile(r'(<nav class="main-nav">)(.*?)(</nav>)', re.DOTALL | re.IGNORECASE)
        
        match = pattern.search(content)
        if match:
            new_items = get_nav_items(filename)
            # We reconstruct the inner part. Use a standard <ul>.
            # If style.css expects .main-nav ul, this will work.
            new_inner = f"""
                <ul>
                    {new_items}
                </ul>
            """
            
            new_block = f"{match.group(1)}{new_inner}{match.group(3)}"
            
            content = pattern.sub(new_block, content)
            
            if content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                updates.append(filename)
                count += 1
        else:
             print(f"Skipping {filename} (No main-nav found)")

    print(f"Unified menu in {count} files: {updates}")

if __name__ == "__main__":
    unify_lab_menus()
