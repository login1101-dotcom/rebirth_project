import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

def get_article_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    title = re.sub(r'<.*?>', '', title_match.group(1)).strip() if title_match else "No Title"
    
    date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
    date = date_match.group(1) if date_match else "0000.00.00"
    
    # Try to find category from the text in the opacity:0.8 div
    cat_match = re.search(r'•\s*(.*?)\s*</div>', content)
    category_name = cat_match.group(1).strip() if cat_match else "Other"
    
    # Excerpt (first <p> after post-content)
    excerpt_match = re.search(r'<div class="post-content">.*?<p.*?>(.*?)</p>', content, re.DOTALL)
    excerpt = re.sub(r'<.*?>', '', excerpt_match.group(1)).strip() if excerpt_match else ""
    if len(excerpt) > 100: excerpt = excerpt[:97] + "..."
    
    return {
        "filename": os.path.basename(file_path),
        "title": title,
        "date": date,
        "category_name": category_name,
        "excerpt": excerpt
    }

def update_project(project_path):
    project_name = os.path.basename(project_path)
    print(f"Updating project: {project_name}")
    
    articles = []
    for filename in os.listdir(project_path):
        if filename.startswith("post_") and filename.endswith(".html"):
            articles.append(get_article_data(os.path.join(project_path, filename)))
    
    # Sort by date descending
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Update index.html
    index_path = os.path.join(project_path, "index.html")
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        # Build article list HTML
        list_html = '<div class="article-list">\n'
        for art in articles[:8]: # Show top 8
            # Simple category logic for class
            cat_class = "diet" if "health" in project_name else "reading" if "english" in project_name else "novel" if "novel" in project_name else "others"
            # Try to be more specific if possible (dummy mapping)
            map_cat = {"リーディング": "reading", "リスニング": "listening", "ライティング": "writing", "スピーキング": "speaking",
                       "食事": "diet", "筋トレ": "muscle", "睡眠": "sleep", "その他": "others"}
            for k, v in map_cat.items():
                if k in art['category_name']:
                    cat_class = v
                    break
            
            logo = "🥗" if cat_class == "diet" else "💪" if cat_class == "muscle" else "💤" if cat_class == "sleep" else "📖" if cat_class == "reading" else "🎵" if cat_class == "listening" else "✍️" if cat_class == "writing" else "🗣️" if cat_class == "speaking" else "📄"
            
            list_html += f"""                <article class="article-item {cat_class}">
                    <a href="{art['filename']}">
                        <div class="item-meta-group">
                            <div class="item-meta">{art['date']} • <span class="text-{cat_class}">{art['category_name']}</span></div>
                            <div class="item-logo-row">
                                <div class="item-logo">{logo}</div>
                                <div class="item-click-hint">LEARN MORE</div>
                            </div>
                        </div>
                        <div class="item-title-box">
                            <h3 class="article-title">{art['title']}</h3>
                            <p class="item-excerpt">{art['excerpt']}</p>
                        </div>
                    </a>
                </article>\n"""
        list_html += '            </div>'
        
        new_index = re.sub(r'<div class="article-list">.*?            </div>', list_html, index_content, flags=re.DOTALL)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_index)

    # Category Counts
    counts = {}
    for art in articles:
        counts[art['category_name']] = counts.get(art['category_name'], 0) + 1
    
    # Update sidebar.js
    sidebar_path = os.path.join(project_path, "sidebar.js")
    if os.path.exists(sidebar_path):
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            sidebar_content = f.read()
            
        # This is harder because sidebar.js has hardcoded category list.
        # Let's just update the 'count: X' values if they match.
        for cat_name, count in counts.items():
            # Try to find the line in sidebar.js that has this category name
            sidebar_content = re.sub(rf'{{ name: "{cat_name}", (.*?) count: \d+,', f'{{ name: "{cat_name}", \\1 count: {count},', sidebar_content)
        
        with open(sidebar_path, 'w', encoding='utf-8') as f:
            f.write(sidebar_content)

for d in os.listdir(CHILDREN_DIR):
    p = os.path.join(CHILDREN_DIR, d)
    if os.path.isdir(p): update_project(p)
