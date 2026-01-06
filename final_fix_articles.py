import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

# Category to CSS class mapping
CAT_MAP = {
    # Health
    "食事": "diet", "筋トレ": "muscle", "睡眠": "sleep", "その他": "others",
    # English
    "リーディング": "reading", "リスニング": "listening", "ライティング": "writing", "スピーキング": "speaking",
    # Novel
    "連載": "series", "短編": "short", "執筆メモ": "memo",
    # YouTube
    "チャンネル紹介": "channel", "機材・ツール": "tools", "運営分析": "analysis",
    # Manga
    "レビュー": "review", "おすすめ本": "list", "ニュース": "news",
    # Typing
    "記録": "log", "上達のコツ": "tips", "キーボード": "hardware"
}

def get_project_base_class(project_name):
    if "health" in project_name: return "diet"
    if "english" in project_name: return "reading"
    if "novel" in project_name: return "series"
    if "youtube" in project_name: return "channel"
    if "manga" in project_name: return "review"
    if "typing" in project_name: return "log"
    return "others"

def fix_file(file_path, project_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extract clean info
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    title = re.sub(r'<.*?>', '', title_match.group(1)).strip() if title_match else "No Title"
    
    date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
    date = date_match.group(1) if date_match else "2026.01.01"
    
    cat_match = re.search(r'•\s*(.*?)\s*</div>', content)
    category_name = cat_match.group(1).strip() if cat_match else "Log"
    cat_class = CAT_MAP.get(category_name, get_project_base_class(project_name))

    # 2. Extract Header, Sidebar, Footer from index.html (Project Source)
    index_path = os.path.join(os.path.dirname(file_path), "index.html")
    if not os.path.exists(index_path): return
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    header = (re.search(r'(<header>.*?</header>)', index_content, re.DOTALL) or [""])[0]
    footer = (re.search(r'(<footer.*?>.*?</footer>)', index_content, re.DOTALL) or [""])[0]
    # Keep sidebar as dynamic div
    sidebar = '<aside class="sidebar">\n            <div id="category-list"></div>\n        </aside>'
    
    # Check if index has a profile widget
    profile_match = re.search(r'(<div class="widget profile-widget">.*?</div>)', index_content, re.DOTALL)
    if profile_match:
        sidebar = f'<aside class="sidebar">\n            {profile_match.group(1)}\n            <div class="widget">\n                <h4 class="widget-label" style="font-size:0.7rem; color:#999; margin-bottom:0.5rem; text-transform:uppercase;">Sponsored</h4>\n                <div class="adsense-placeholder">Ads Display</div>\n            </div>\n            <div class="widget">\n                <h3 class="widget-title">Categories</h3>\n                <div id="category-list"></div>\n            </div>\n        </aside>'

    # 3. Extract Body Content
    # We look for the main content area and extract everything after the article header
    body_content = ""
    parts = re.split(r'</header>\s*<div class="post-content">', content, flags=re.DOTALL)
    if len(parts) > 1:
        # Take everything from <div class="post-content"> until the navigation/footer
        body_parts = re.split(r'<div style="margin-top: 3rem;', parts[1], flags=re.DOTALL)
        body_content = body_parts[0].strip()
    else:
        # Fallback extraction
        inner_content = re.search(r'<div class="post-content">(.*?)<div style="margin-top: 3rem;', content, re.DOTALL)
        if inner_content:
            body_content = inner_content.group(1).strip()

    # 4. Reconstruct with correct Flex/Grid Structure
    new_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-1F416P0VQS"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'G-1F416P0VQS');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Re:Birth</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
</head>
<body>
    {header}
    <div class="container main-layout">
        <main class="content-area">
            <div class="breadcrumb" style="font-size:0.9rem; color:var(--text-light); margin-bottom:1.5rem;">
                <a href="index.html" style="color:inherit; text-decoration:none;">ホーム</a> &gt; 記事詳細
            </div>
            <article class="single-post">
                <header class="bg-styled bg-{cat_class}">
                    <div style="font-size: 0.85rem; margin-bottom: 0.5rem; opacity: 0.8;">{date} • {category_name}</div>
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
    if not os.path.isdir(p): continue
    for f in os.listdir(p):
        if f.startswith("post_") and f.endswith(".html"):
            print(f"Fixing: {d}/{f}")
            fix_file(os.path.join(p, f), d)
