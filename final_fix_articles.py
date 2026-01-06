import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

CAT_MAP = {
    "食事": "diet", "筋トレ": "muscle", "睡眠": "sleep", "その他": "others",
    "リーディング": "reading", "リスニング": "listening", "ライティング": "writing", "スピーキング": "speaking",
    "連載": "series", "短編": "short", "執筆メモ": "memo",
    "チャンネル紹介": "channel", "機材・ツール": "tools", "運営分析": "analysis",
    "レビュー": "review", "おすすめ本": "list", "ニュース": "news",
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

def fix_project(project_path):
    project_name = os.path.basename(project_path)
    index_path = os.path.join(project_path, "index.html")
    if not os.path.exists(index_path): return

    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    # Get Site Brand / Header
    header = (re.search(r'(<header>.*?</header>)', index_content, re.DOTALL) or [""])[0]
    footer = (re.search(r'(<footer.*?>.*?</footer>)', index_content, re.DOTALL) or [""])[0]
    
    # Robust Profile Widget Extraction (between markers)
    profile_widget = ""
    profile_match = re.search(r'<!-- Author Widget -->(.*?)<!-- AdSense Widget', index_content, re.DOTALL)
    if profile_match:
        profile_widget = profile_match.group(1).strip()
    else:
        # Fallback to class-based but with balanced tag awareness (simplified)
        profile_match = re.search(r'<div class="widget profile-widget">.*?</div>\s*</div>', index_content, re.DOTALL)
        if profile_match: profile_widget = profile_match.group(0)

    # Get all post files
    posts = [f for f in os.listdir(project_path) if f.startswith("post_") and f.endswith(".html")]
    # Sort logically: by number if possible
    def sort_key(f):
        nums = re.findall(r'\d+', f)
        return int(nums[0]) if nums else f
    posts.sort(key=sort_key)

    for i, post_file in enumerate(posts):
        file_path = os.path.join(project_path, post_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Meta info
        title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
        title = re.sub(r'<.*?>', '', title_match.group(1)).strip() if title_match else "No Title"
        
        date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
        date = date_match.group(1) if date_match else "2026.01.01"
        
        cat_match = re.search(r'•\s*(.*?)\s*</div>', content)
        category_name = cat_match.group(1).strip() if cat_match else "Log"
        cat_class = CAT_MAP.get(category_name, get_project_base_class(project_name))

        # Content extraction (everything between <div class="post-content"> and <div style="margin-top: 3rem;)
        # We need to be careful with the trailing </div> of post-content
        body_content = ""
        body_match = re.search(r'<div class="post-content">(.*?)<div style="margin-top: 3rem;', content, re.DOTALL)
        if body_match:
            body_content = body_match.group(1).strip()
            # If body_content ends with a loose </div>, remove it (it belonged to the old post-content wrapper)
            if body_content.endswith("</div>"):
                body_content = body_content[:-6].strip()
        else:
            # Last ditch effort
            body_parts = re.split(r'<div class="post-content">', content)
            if len(body_parts) > 1:
                body_end_split = re.split(r'</div>\s*<div style="margin-top: 3rem;', body_parts[1])
                body_content = body_end_split[0].strip()

        # Prev/Next Nav
        prev_link = f'<a href="{posts[i-1]}" class="nav-prev">← 前の記事</a>' if i > 0 else '<span></span>'
        next_link = f'<a href="{posts[i+1]}" class="nav-next">次の記事 →</a>' if i < len(posts) - 1 else '<span></span>'
        
        nav_html = f"""
            <div class="post-navigation" style="margin-top: 3rem; display: flex; justify-content: space-between; align-items: center; padding-top: 2rem; border-top: 1px solid var(--border);">
                {prev_link}
                <a href="index.html" class="btn-primary">一覧に戻る</a>
                {next_link}
            </div>"""

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
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>✨</text></svg>">
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
                </div>
                {nav_html}
            </article>
        </main>
        <aside class="sidebar">
            {profile_widget}
            <div class="widget">
                <h4 class="widget-label" style="font-size:0.7rem; color:#999; margin-bottom:0.5rem; text-transform:uppercase;">Sponsored</h4>
                <div class="adsense-placeholder">Ads Display</div>
            </div>
            <div class="widget">
                <h3 class="widget-title">Categories</h3>
                <div id="category-list"></div>
            </div>
        </aside>
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
    if os.path.isdir(p): fix_project(p)
