import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

SKIP_FILES = ["index.html", "view_data.html", "article.html", "articles.html"]

def process_project(project_path):
    project_name = os.path.basename(project_path)
    index_path = os.path.join(project_path, "index.html")
    if not os.path.exists(index_path):
        return

    print(f"Processing project: {project_name}")
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    header_match = re.search(r'(<header>.*?</header>)', index_content, re.DOTALL)
    footer_match = re.search(r'(<footer.*?>.*?</footer>)', index_content, re.DOTALL)
    sidebar_match = re.search(r'(<aside class="sidebar">.*?</aside>)', index_content, re.DOTALL) or \
                    re.search(r'(<div class="sidebar">.*?</div>)', index_content, re.DOTALL)
    
    head_match = re.search(r'<head>(.*?)</head>', index_content, re.DOTALL)
    if not head_match: return
    head_inner = re.sub(r'<title>.*?</title>', '', head_match.group(1))

    header = header_match.group(1) if header_match else ""
    footer = footer_match.group(1) if footer_match else ""
    sidebar = sidebar_match.group(1) if sidebar_match else ""

    for filename in os.listdir(project_path):
        if not filename.endswith(".html") or filename in SKIP_FILES or filename.startswith("category_"):
            continue
            
        file_path = os.path.join(project_path, filename)
        print(f"  Refactoring: {filename}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract Title
        title_match = re.search(r'<h1.*?>(.*?)</h1>', content, re.DOTALL)
        title = title_match.group(1) if title_match else "No Title"
        title = re.sub(r'<.*?>', '', title).strip()
        
        # Extract Date
        date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
        date = date_match.group(1) if date_match else "2026.01.06"
        
        # Extract Category
        cat_match = re.search(r'<span class="post-category">(.*?)</span>', content)
        category = cat_match.group(1) if cat_match else "Daily Log"
        
        # EXTRACT CLEAN CONTENT
        # Logic: find the widest div that contains the actual text and isn't the whole page.
        # Try to find <div class="post-body"> or <div class="post-content">
        body_content = ""
        body_match = re.search(r'<div class="post-body">(.*?)</div>\s*(?:</div>|</article>|<!-- Nav)', content, re.DOTALL)
        if not body_match:
            body_match = re.search(r'<div class="post-content">(.*?)</div>\s*(?:</div>|</article>|<!-- Nav)', content, re.DOTALL)
        if not body_match:
            # If already using new layout but broken, extract from post-content
            body_match = re.search(r'<div class="post-content">(.*?)<div style="margin-top: 3rem;', content, re.DOTALL)
        
        if body_match:
            body_content = body_match.group(1).strip()
        else:
            # Fallback for very raw files
            body_content = re.sub(r'.*?</h1>', '', content, flags=re.DOTALL)
            body_content = re.sub(r'<div class="post-navigation".*', '', body_content, flags=re.DOTALL)
            body_content = re.sub(r'</body>.*', '', body_content, flags=re.DOTALL)

        # Remove stray formatting tags from another layout if they leaked in
        body_content = re.sub(r'</header>\s*<div class="post-content">', '', body_content)

        bg_class = "bg-diet" if "health" in project_name else \
                   "bg-reading" if "english" in project_name else \
                   "bg-novel" if "novel" in project_name else \
                   "bg-manga" if "manga" in project_name else \
                   "bg-youtube" if "youtube" in project_name else \
                   "bg-typing" if "typing" in project_name else \
                   "bg-others"
        
        new_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    {head_inner.strip()}
    <title>{title} | Project</title>
</head>
<body>
    {header}
    <div class="container main-layout">
        <main class="content-area">
            <div class="breadcrumb" style="font-size:0.9rem; color:var(--text-light); margin-bottom:1.5rem;">
                <a href="index.html" style="color:inherit; text-decoration:none;">ホーム</a> &gt; 記事詳細
            </div>
            <article class="single-post">
                <header class="bg-styled {bg_class}">
                    <div style="font-size: 0.85rem; margin-bottom: 0.5rem; opacity: 0.8;">{date} • {category}</div>
                    <h1>{title}</h1>
                </header>
                <div class="post-content">
                    {body_content}
                    <div style="margin-top: 3rem; display: flex; justify-content: flex-end;">
                        <a href="index.html" class="btn-primary">一覧に戻る</a>
                    </div>
                </div>
            </article>
        </main>
        {sidebar}
    </div>
    {footer}
    <script src="sidebar.js"></script>
    <script src="counter.js"></script>
</body>
</html>"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)

for d in os.listdir(CHILDREN_DIR):
    p = os.path.join(CHILDREN_DIR, d)
    if os.path.isdir(p): process_project(p)
