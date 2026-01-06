import os
import re

LAB_DIR = "/Users/jono/Desktop/rebirth_project/children/rebirth_child_typing"

def determine_active_category(content, filename):
    # 1. Self-Check (Category Pages)
    if filename == 'category_daily.html': return 'category_daily.html'
    if filename == 'category_analysis.html': return 'category_analysis.html'
    if filename == 'category_tools.html': return 'category_tools.html'
    if filename == 'index.html': return 'index.html'

    # 2. Strong signals (Header Tags)
    # text-analysis, text-daily, text-tools are unique to headers/lists
    if 'text-analysis' in content: return 'category_analysis.html'
    if 'text-daily' in content: return 'category_daily.html'
    if 'text-tools' in content: return 'category_tools.html'

    # 3. Breadcrumbs (Specific Pattern)
    # <a class="active" href="category_analysis.html">
    if 'href="category_analysis.html"' in content and 'active' in content:
        # Check if they are close? Regex is safer.
        if re.search(r'<a[^>]*active[^>]*href="category_analysis\.html"', content):
            return 'category_analysis.html'
    
    if re.search(r'<a[^>]*active[^>]*href="category_daily\.html"', content):
        return 'category_daily.html'
        
    if re.search(r'<a[^>]*active[^>]*href="category_tools\.html"', content):
        return 'category_tools.html'

    # Default fallback
    return None

def get_nav_items(active_target):
    def is_active(target):
        return "active" if active_target == target else ""

    home_cls = f"{is_active('index.html')}"
    daily_cls = f"nav-daily {is_active('category_daily.html')}"
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

def fix_active_strict():
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
        
        # Determine strict active target
        active_target = determine_active_category(content, filename)
        
        # Generate new menu
        pattern = re.compile(r'(<nav class="main-nav">.*?<ul>)(.*?)(</ul>)', re.DOTALL | re.IGNORECASE)
        match = pattern.search(content)
        
        if match:
            new_items = get_nav_items(active_target)
            new_inner = new_items # Just the items string
            
            # Reconstruct
            new_block = f"{match.group(1)}\n                    {new_items}\n                {match.group(3)}"
            
            content = pattern.sub(new_block, content)
            
            if content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                updates.append(filename)
                count += 1

    print(f"Fixed active states in {count} files: {updates}")

if __name__ == "__main__":
    fix_active_strict()
