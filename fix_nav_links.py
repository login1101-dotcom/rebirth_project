import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

def fix_navigation_links(project_path):
    project_name = os.path.basename(project_path)
    
    # Get all real article files
    articles = []
    for f in os.listdir(project_path):
        if f.startswith("post_") and f.endswith(".html"):
            path = os.path.join(project_path, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Extract date for sorting
            date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
            date = date_match.group(1) if date_match else "2026.01.01"
            
            articles.append({
                "filename": f,
                "date": date,
                "path": path
            })
    
    # Sort by date descending (Newest first)
    # But usually "Next" means Newer and "Prev" means Older? Or vice versa in blog?
    # Usually: < Prev (Newer)   |   Next (Older) > OR < Prev (Older) | Next (Newer) >
    # Let's stick to simple chronological ID order if dates are same? No, date is better.
    # Let's sort by date ascending (Oldest first) so index 0 is oldest.
    # index i: Prev = i-1, Next = i+1
    
    articles.sort(key=lambda x: x['date']) 
    
    for i, art in enumerate(articles):
        prev_art = articles[i-1] if i > 0 else None
        next_art = articles[i+1] if i < len(articles) - 1 else None
        
        # HTML template for navigation
        nav_html = '<div class="post-navigation" style="margin-top: 3rem; display: flex; justify-content: space-between; align-items: center; padding-top: 2rem; border-top: 1px solid var(--border);">'
        
        if prev_art:
            nav_html += f'<a href="{prev_art["filename"]}" class="nav-prev">← 前の記事</a>'
        else:
            nav_html += '<span></span>' # Spacer
            
        nav_html += '<a href="index.html" class="btn-primary">一覧に戻る</a>'
        
        if next_art:
            nav_html += f'<a href="{next_art["filename"]}" class="nav-next">次の記事 →</a>'
        else:
            nav_html += '<span></span>' # Spacer
            
        nav_html += '</div>'
        
        with open(art['path'], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace existing navigation div
        # Regex to find the div class="post-navigation" ... </div>
        # Be careful with nested divs, but post-navigation usually doesn't have nested divs widely
        
        pattern = r'<div class="post-navigation".*?>.*?</div>'
        # Match dotall
        new_content = re.sub(pattern, nav_html, content, flags=re.DOTALL)
        
        with open(art['path'], 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    print(f"Fixed navigation for {len(articles)} articles in {project_name}")

for d in os.listdir(CHILDREN_DIR):
    p = os.path.join(CHILDREN_DIR, d)
    if os.path.isdir(p):
        fix_navigation_links(p)
