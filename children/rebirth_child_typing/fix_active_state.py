import os
import re

LAB_DIR = "/Users/jono/Desktop/rebirth_project/children/rebirth_child_typing"

def determine_active_category(content, filename):
    # If it's a category page, self-evident
    if filename == 'category_daily.html': return 'category_daily.html'
    if filename == 'category_analysis.html': return 'category_analysis.html'
    if filename == 'category_tools.html': return 'category_tools.html'
    if filename == 'index.html': return 'index.html'

    # If it's a post, look for breadcrumbs or tags
    # Breadcrumb pattern: <a href="category_daily.html">
    # Tag pattern: <span class="cat text-daily">
    
    if 'href="category_daily.html"' in content or 'text-daily' in content:
        return 'category_daily.html'
    if 'href="category_analysis.html"' in content or 'text-analysis' in content:
        return 'category_analysis.html'
    if 'href="category_tools.html"' in content or 'text-tools' in content:
        return 'category_tools.html'
        
    return None

def get_nav_items(active_target):
    def is_active(target):
        # active class logic (assuming 'active' class makes it bold/large)
        return "active" if active_target == target else ""

    # Classes: nav-daily, nav-analysis, nav-tools are likely needed for color hooks in CSS
    # AND 'active' for state.
    
    # Home
    home_cls = f"{is_active('index.html')}"
    
    # Practice
    daily_cls = f"nav-daily {is_active('category_daily.html')}"
    
    # Analysis
    analysis_cls = f"nav-analysis {is_active('category_analysis.html')}"
    
    # Tools
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

def update_active_states():
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
        
        # 1. Determine which category should be active based on content
        active_target = determine_active_category(content, filename)
        
        # 2. Re-generatre Nav
        # Regex to capture the NAV block (unified format now)
        # <nav class="main-nav"> ... <ul> ... </ul> ... </nav>
        # OR just find the <ul> inside .main-nav if we trust the outer structure
        # Let's target the inner <ul> content to be safe, assuming <nav class="main-nav"> exists.
        
        pattern = re.compile(r'(<nav class="main-nav">.*?<ul>)(.*?)(</ul>)', re.DOTALL | re.IGNORECASE)
        match = pattern.search(content)
        
        if match:
            new_items = get_nav_items(active_target)
            new_block = f"{match.group(1)}\n                    {new_items}\n                {match.group(3)}"
            
            content = pattern.sub(new_block, content)
            
            if content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                updates.append(filename)
                count += 1

    print(f"Updated active states in {count} files: {updates}")

if __name__ == "__main__":
    update_active_states()
