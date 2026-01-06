import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

SKIP_FILES = ["index.html", "view_data.html", "article.html", "articles.html"]

def process_project(project_path):
    project_name = os.path.basename(project_path)
    index_path = os.path.join(project_path, "index.html")
    if not os.path.exists(index_path): return

    print(f"Processing project: {project_name}")
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    header = (re.search(r'(<header>.*?</header>)', index_content, re.DOTALL) or [""])[0]
    footer = (re.search(r'(<footer.*?>.*?</footer>)', index_content, re.DOTALL) or [""])[0]
    sidebar = (re.search(r'(<aside class="sidebar">.*?</aside>)', index_content, re.DOTALL) or \
               re.search(r'(<div class="sidebar">.*?</div>)', index_content, re.DOTALL) or [""])[0]
    
    head_match = re.search(r'<head>(.*?)</head>', index_content, re.DOTALL)
    if not head_match: return
    head_inner = re.sub(r'<title>.*?</title>', '', head_match.group(1))

    for filename in os.listdir(project_path):
        if not filename.endswith(".html") or filename in SKIP_FILES or filename.startswith("category_"):
            continue
            
        file_path = os.path.join(project_path, filename)
        print(f"  Refactoring: {filename}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        title_match = re.search(r'<h1.*?>(.*?)</h1>', content, re.DOTALL)
        title = re.sub(r'<.*?>', '', title_match.group(1)).strip() if title_match else "No Title"
        date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
        date = date_match.group(1) if date_match else "2026.01.01"
        cat_match = re.search(r'<span class="post-category">(.*?)</span>', content)
        category = cat_match.group(1) if cat_match else "Daily Log"
        
        # EXTRACT CLEAN CONTENT: Try to find common content containers
        # Look for the last <header> and take everything after it until sidebar or footer
        parts = re.split(r'</header>', content)
        if len(parts) > 1:
            # Take everything after the last </header> excluding navigation/footer/sidebar
            body_content = parts[-1]
        else:
            body_content = content

        # Strip standard wrapper components if they leaked into body_content
        body_content = re.sub(r'<div class="post-navigation".*', '', body_content, flags=re.DOTALL)
        body_content = re.sub(r'<aside class="sidebar".*', '', body_content, flags=re.DOTALL)
        body_content = re.sub(r'<footer.*', '', body_content, flags=re.DOTALL)
        body_content = re.sub(r'</body>.*', '', body_content, flags=re.DOTALL)
        body_content = re.sub(r'</html>.*', '', body_content, flags=re.DOTALL)
        # Remove repeated intro tags
        body_content = re.sub(r'^.*?<div class="post-content">', '', body_content, flags=re.DOTALL)
        body_content = re.sub(r'<div class="breadcrumb".*?</div>', '', body_content, flags=re.DOTALL)
        body_content = re.sub(r'<div style="margin-top: 3rem;.*', '', body_content, flags=re.DOTALL)
        body_content = body_content.replace('<article class="single-post">', '').replace('</article>', '')
        
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
    <title>{title} | Re:Birth</title>
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
                    {body_content.strip()}
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
