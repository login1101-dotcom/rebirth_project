import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

PROJECT_CONFIG = {
    "rebirth_child_health": {
        "title": "Body Logic",
        "tagline": "見た目のいい健康な体を手にいれる",
        "icon": "🥗",
        "user_name": "Bio 55",
        "user_desc": "健康寿命を延ばす実験中。<br>現在の目標：体脂肪率 20%以下",
        "categories": [
            {"name": "食事", "id": "diet", "keywords": ["食事", "おにぎり", "パン", "オートミール", "腹", "食", "ダイエット", "暴食", "いもパン"]},
            {"name": "筋トレ", "id": "muscle", "keywords": ["筋トレ", "トレーニング", "ダンベル", "ウォーキング", "散歩", "筋肉"]},
            {"name": "睡眠", "id": "sleep", "keywords": ["睡眠", "枕", "寝", "疲れ"]},
            {"name": "その他", "id": "others", "keywords": ["サプリ", "姿勢", "腰", "幸福"]}
        ],
        "default_cat": "食事",
        "logo_map": {"diet": "🥗", "muscle": "💪", "sleep": "💤", "others": "⚙️"}
    },
    "rebirth_child_english": {
        "title": "English Gym",
        "tagline": "使える英語を身につける",
        "icon": "🇬🇧",
        "user_name": "Polyglot 55",
        "user_desc": "51歳からの英語脳構築中。<br>現在の目標：IELTS 7.0",
        "categories": [
            {"name": "リーディング", "id": "reading", "keywords": ["Reading", "多読", "洋書", "Kindle", "リーディング"]},
            {"name": "リスニング", "id": "listening", "keywords": ["Listening", "リスニング", "聴", "Podcast", "ポッドキャスト", "Let It Be", "CNN"]},
            {"name": "ライティング", "id": "writing", "keywords": ["Writing", "ライティング", "書く", "日記", "To-Do", "Essay"]},
            {"name": "スピーキング", "id": "speaking", "keywords": ["Speaking", "スピーキング", "独り言", "会話"]}
        ],
        "default_cat": "リーディング",
        "logo_map": {"reading": "📖", "listening": "🎵", "writing": "✍️", "speaking": "🗣️"}
    },
    "rebirth_child_typing": {
        "title": "Typing Lab",
        "tagline": "ブラインドタッチを習得する",
        "icon": "⌨️",
        "user_name": "Admin 55",
        "user_desc": "51歳からのスキル獲得実験中。<br>現在の目標：WPM 100",
        "categories": [
            {"name": "Practice", "id": "daily", "keywords": ["記録", "スコア", "練習", "苦戦", "矯正"]},
            {"name": "Analysis", "id": "analysis", "keywords": ["分析", "データ", "推移", "効率化"]},
            {"name": "Tools", "id": "tools", "keywords": ["キーボード", "HHKB", "Neo"]}
        ],
        "default_cat": "Practice",
        "logo_map": {"daily": "⌨️", "analysis": "📈", "tools": "🛠️"}
    },
    "rebirth_child_novel": {
        "title": "Story Forge",
        "tagline": "物語を紡ぎ出す",
        "icon": "📚",
        "user_name": "Author 55",
        "user_desc": "51歳からの小説執筆ログ。<br>目標：処女作完成",
        "categories": [
            {"name": "連載", "id": "series", "keywords": ["第", "話", "連載"]},
            {"name": "短編", "id": "short", "keywords": ["短編", "読切"]},
            {"name": "メモ", "id": "memo", "keywords": ["メモ", "設定", "プロット", "考察", "時間税", "ストレス"]}
        ],
        "default_cat": "連載",
        "logo_map": {"series": "📚", "short": "📝", "memo": "🖋️"}
    },
    "rebirth_child_youtube": {
        "title": "Movie Studio",
        "tagline": "動画で伝える",
        "icon": "📺",
        "user_name": "Editor 55",
        "user_desc": "51歳からのYouTube運営。<br>目標：登録者1000人",
        "categories": [
            {"name": "動画", "id": "movie", "keywords": ["動画", "Vlog", "再生"]},
            {"name": "機材", "id": "tools", "keywords": ["機材", "カメラ", "マイク"]},
            {"name": "分析", "id": "analysis", "keywords": ["分析", "データ"]}
        ],
        "default_cat": "動画",
        "logo_map": {"movie": "🎬", "tools": "🛠️", "analysis": "📈"}
    }
}

def get_article_info(file_path, project_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    title = re.sub(r'<.*?>', '', title_match.group(1)).strip() if title_match else "No Title"
    
    date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
    date = date_match.group(1) if date_match else "2026.01.01"
    
    excerpt = ""
    excerpt_match = re.search(r'<div class="post-content">(.*?)</div>', content, re.DOTALL)
    if excerpt_match:
        text = re.sub(r'<.*?>', '', excerpt_match.group(1)).strip()
        excerpt = text[:100] + "..." if len(text) > 100 else text

    config = PROJECT_CONFIG.get(project_name)
    category = None
    if config:
        for cat in config['categories']:
            if any(kw.lower() in title.lower() for kw in cat['keywords']):
                category = cat
                break
        if not category:
            category = [c for c in config['categories'] if c['name'] == config['default_cat']][0]
    
    return {
        "filename": os.path.basename(file_path),
        "title": title,
        "date": date,
        "excerpt": excerpt,
        "category": category
    }

def rebuild_category_pages(project_path):
    project_name = os.path.basename(project_path)
    if project_name not in PROJECT_CONFIG: return
    config = PROJECT_CONFIG[project_name]
    
    articles = []
    for f in os.listdir(project_path):
        if f.startswith("post_") and f.endswith(".html"):
            articles.append(get_article_info(os.path.join(project_path, f), project_name))
    articles.sort(key=lambda x: x['date'], reverse=True)

    header_html = f"""    <header>
        <div class="container header-inner">
            <a href="index.html" class="site-brand"><span>{config['icon']}</span> {config['title']}<span style="font-size: 0.8rem; color: #64748b; margin-left: 10px; font-weight: normal;">{config['tagline']}</span></a>
            <nav class="main-nav">
                <ul>
                    <li><a href="index.html">ホーム</a></li>
                    {" ".join([f'<li><a class="nav-{cat["id"]}" href="category_{cat["id"]}.html">{cat["name"]}</a></li>' for cat in config['categories']])}
                    <li><a href="../../index.html">← Project Hub</a></li>
                </ul>
            </nav>
        </div>
    </header>"""

    for cat in config['categories']:
        cat_file = os.path.join(project_path, f"category_{cat['id']}.html")
        cat_arts = [a for a in articles if a['category']['id'] == cat['id']]
        
        items_html = ""
        for art in cat_arts:
            logo = config['logo_map'].get(cat['id'], "📄")
            items_html += f"""
                <article class="article-item {cat['id']}">
                    <a href="{art['filename']}">
                        <div class="item-meta-group">
                            <div class="item-meta">{art['date']} • <span class="text-{cat['id']}">{cat['name']}</span></div>
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
                </article>"""

        new_page = f"""<!DOCTYPE html>
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
    <title>{cat['name']} | {config['title']}</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
</head>
<body>
{header_html}
    <div class="container main-layout">
        <main class="content-area">
            <div class="breadcrumb" style="font-size:0.9rem; color:var(--text-light); margin-bottom:1.5rem;">
                <a href="index.html">ホーム</a> &gt; {cat['name']}
            </div>
            <div class="article-list">
                {items_html if items_html else "<p>記事がありません。</p>"}
            </div>
        </main>
        <aside class="sidebar">
            <div class="widget profile-widget">
                <div class="profile-img"></div>
                <h3 style="font-size:1.1rem; margin-bottom:0.5rem;">{config['user_name']}</h3>
                <p style="font-size:0.9rem; color:var(--text-light); line-height:1.6;">{config['user_desc']}</p>
            </div>
            <div class="widget">
                <h3 class="widget-title">Categories</h3>
                <div id="category-list"></div>
            </div>
        </aside>
    </div>
    <footer class="child-footer">
        <div class="container"><p>&copy; 2025 {config['title']} | Re:Birth 55 Project</p></div>
    </footer>
    <script src="sidebar.js"></script>
</body>
</html>"""
        with open(cat_file, 'w', encoding='utf-8') as f:
            f.write(new_page)

for d in os.listdir(CHILDREN_DIR):
    p = os.path.join(CHILDREN_DIR, d)
    if os.path.isdir(p): rebuild_category_pages(p)
