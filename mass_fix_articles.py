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

    # Extract common components from index.html
    header_match = re.search(r'(<header>.*?</header>)', index_content, re.DOTALL)
    footer_match = re.search(r'(<footer.*?>.*?</footer>)', index_content, re.DOTALL)
    sidebar_match = re.search(r'(<aside class="sidebar">.*?</aside>)', index_content, re.DOTALL)
    if not sidebar_match:
        sidebar_match = re.search(r'(<div class="sidebar">.*?</div>)', index_content, re.DOTALL)
    
    # Also extract <head> components
    head_match = re.search(r'<head>(.*?)</head>', index_content, re.DOTALL)
    if not head_match:
        return
    
    head_inner = head_match.group(1)
    # Remove title
    head_inner = re.sub(r'<title>.*?</title>', '', head_inner)

    header = header_match.group(1) if header_match else ""
    footer = footer_match.group(1) if footer_match else ""
    sidebar = sidebar_match.group(1) if sidebar_match else ""

    for filename in os.listdir(project_path):
        if not filename.endswith(".html"):
            continue
        if filename in SKIP_FILES or filename.startswith("category_"):
            continue
            
        file_path = os.path.join(project_path, filename)

        print(f"  Refactoring: {filename}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract Article Data
        title_match = re.search(r'<title>(.*?)</title>', content)
        body_title_match = re.search(r'<h1.*?>(.*?)</h1>', content)
        
        title = body_title_match.group(1) if body_title_match else (title_match.group(1) if title_match else "No Title")
        # Clean title from HTML tags
        title = re.sub(r'<.*?>', '', title)
        
        date_match = re.search(r'<span class="post-date">(.*?)</span>', content)
        if not date_match:
            date_match = re.search(r'<div class="post-meta">.*?(\d{4}\.\d{2}\.\d{2})', content)
        if not date_match:
            date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
        date = date_match.group(1) if date_match else "Year.Month.Day"
        
        cat_match = re.search(r'<span class="post-category">(.*?)</span>', content)
        category = cat_match.group(1) if cat_match else "Log"
        
        # Extract content
        # Try to find a good container
        post_body_match = re.search(r'<div class="post-body">(.*?)</div>\s*</div>', content, re.DOTALL)
        if not post_body_match:
            post_body_match = re.search(r'<main class="content-area">.*?<div class="post-content">(.*?)</div>\s*</article>', content, re.DOTALL)
        if not post_body_match:
            post_body_match = re.search(r'</h1>(.*?)(?:<div class="post-navigation"|</body>|<!-- Footer -->)', content, re.DOTALL)
        
        post_body = post_body_match.group(1).strip() if post_body_match else "Content missing."

        # Determine BG class
        bg_class = "bg-diet" if project_name == "rebirth_child_health" else \
                   "bg-reading" if project_name == "rebirth_child_english" else \
                   "bg-novel" if project_name == "rebirth_child_novel" else \
                   "bg-manga" if project_name == "rebirth_child_manga" else \
                   "bg-youtube" if project_name == "rebirth_child_youtube" else \
                   "bg-typing" if project_name == "rebirth_child_typing" else \
                   "bg-others"
        
        proj_display_name = "Health" if "health" in project_name else \
                            "English" if "english" in project_name else \
                            "Novel" if "novel" in project_name else \
                            "Manga" if "manga" in project_name else \
                            "YouTube" if "youtube" in project_name else \
                            "Typing" if "typing" in project_name else \
                            "Reading" if "reading" in project_name else "Project"

        # Re-assemble
        new_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    {head_inner.strip()}
    <title>{title} | {proj_display_name}</title>
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
                    {post_body}

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

for project_dir in os.listdir(CHILDREN_DIR):
    full_path = os.path.join(CHILDREN_DIR, project_dir)
    if os.path.isdir(full_path):
        process_project(full_path)
