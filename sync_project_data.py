import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

PROJECT_CONFIG = {
    "rebirth_child_health": {
        "categories": [
            {"name": "食事", "id": "diet", "keywords": ["食事", "おにぎり", "パン", "オートミール", "腹", "食", "ダイエット"]},
            {"name": "筋トレ", "id": "muscle", "keywords": ["筋トレ", "トレーニング", "ダンベル", "ウォーキング", "散歩", "筋肉"]},
            {"name": "睡眠", "id": "sleep", "keywords": ["睡眠", "枕", "寝", "疲れ"]},
            {"name": "その他", "id": "others", "keywords": ["サプリ", "姿勢", "腰", "幸福"]}
        ],
        "default_cat": "食事",
        "logo_map": {"diet": "🥗", "muscle": "💪", "sleep": "💤", "others": "⚙️"}
    },
    "rebirth_child_english": {
        "categories": [
            {"name": "リーディング", "id": "reading", "keywords": ["Reading", "多読", "洋書", "Kindle", "リーディング"]},
            {"name": "リスニング", "id": "listening", "keywords": ["Listening", "リスニング", "聴", "Podcast", "ポッドキャスト", "Let It Be"]},
            {"name": "ライティング", "id": "writing", "keywords": ["Writing", "ライティング", "書く", "日記", "To-Do"]},
            {"name": "スピーキング", "id": "speaking", "keywords": ["Speaking", "スピーキング", "独り言", "会話"]}
        ],
        "default_cat": "リーディング",
        "logo_map": {"reading": "📖", "listening": "🎵", "writing": "✍️", "speaking": "🗣️"}
    },
    "rebirth_child_novel": {
        "categories": [
            {"name": "連載", "id": "series", "keywords": ["第", "話", "連載"]},
            {"name": "短編", "id": "short", "keywords": ["短編", "読切"]},
            {"name": "執筆メモ", "id": "memo", "keywords": ["メモ", "設定", "プロット"]}
        ],
        "default_cat": "連載",
        "logo_map": {"series": "📚", "short": "📝", "memo": "🖋️"}
    },
    "rebirth_child_youtube": {
        "categories": [
            {"name": "チャンネル紹介", "id": "channel", "keywords": ["チャンネル", "紹介", "おすすめ"]},
            {"name": "機材・ツール", "id": "tools", "keywords": ["機材", "カメラ", "マイク", "ツール", "編集"]},
            {"name": "運営分析", "id": "analysis", "keywords": ["分析", "データ", "再生数", "登録者"]}
        ],
        "default_cat": "チャンネル紹介",
        "logo_map": {"channel": "📺", "tools": "🛠️", "analysis": "📈"}
    },
    "rebirth_child_manga": {
        "categories": [
            {"name": "レビュー", "id": "review", "keywords": ["レビュー", "感想", "読了"]},
            {"name": "おすすめ本", "id": "list", "keywords": ["おすすめ", "厳選", "ベスト"]},
            {"name": "ニュース", "id": "news", "keywords": ["ニュース", "新刊", "発売日"]}
        ],
        "default_cat": "レビュー",
        "logo_map": {"review": "📚", "list": "📑", "news": "📰"}
    },
    "rebirth_child_typing": {
        "categories": [
            {"name": "記録", "id": "log", "keywords": ["記録", "スコア", "練習"]},
            {"name": "上達のコツ", "id": "tips", "keywords": ["コツ", "手法", "指", "配置"]},
            {"name": "キーボード", "id": "hardware", "keywords": ["キーボード", "軸", "メカニカル"]}
        ],
        "default_cat": "記録",
        "logo_map": {"log": "⌨️", "tips": "💡", "hardware": "🔌"}
    }
}

def get_article_info(file_path, project_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    title = re.sub(r'<.*?>', '', title_match.group(1)).strip() if title_match else "No Title"
    
    date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
    date = date_match.group(1) if date_match else "2026.01.01"
    
    # Excerpt
    excerpt_match = re.search(r'<div class="post-content">.*?<p.*?>(.*?)</p>', content, re.DOTALL)
    excerpt = re.sub(r'<.*?>', '', excerpt_match.group(1)).strip() if excerpt_match else ""
    if len(excerpt) > 80: excerpt = excerpt[:77] + "..."

    # Infer Category
    config = PROJECT_CONFIG.get(project_name)
    category = None
    if config:
        for cat in config['categories']:
            if any(kw in title for kw in cat['keywords']):
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

def build_article_item_html(art, proj_name):
    cat_id = art['category']['id'] if art['category'] else "others"
    cat_name = art['category']['name'] if art['category'] else "Log"
    logo = PROJECT_CONFIG.get(proj_name, {}).get('logo_map', {}).get(cat_id, "📄")
    
    return f"""                <article class="article-item {cat_id}">
                    <a href="{art['filename']}">
                        <div class="item-meta-group">
                            <div class="item-meta">{art['date']} • <span class="text-{cat_id}">{cat_name}</span></div>
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

def update_project(project_path):
    project_name = os.path.basename(project_path)
    if project_name not in PROJECT_CONFIG: return
    
    print(f"Syncing: {project_name}")
    articles = []
    for f in os.listdir(project_path):
        if f.startswith("post_") and f.endswith(".html"):
            articles.append(get_article_info(os.path.join(project_path, f), project_name))
    
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # 1. Update index.html
    index_path = os.path.join(project_path, "index.html")
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        items_html = "\n".join([build_article_item_html(a, project_name) for a in articles[:8]])
        new_list = f'<div class="article-list">\n{items_html}\n            </div>'
        content = re.sub(r'<div class="article-list">.*?            </div>', new_list, content, flags=re.DOTALL)
        with open(index_path, 'w', encoding='utf-8') as f: f.write(content)

    # 2. Update category_*.html
    config = PROJECT_CONFIG[project_name]
    cat_counts = {}
    for cat in config['categories']:
        cat_file = os.path.join(project_path, f"category_{cat['id']}.html")
        cat_arts = [a for a in articles if a['category']['id'] == cat['id']]
        cat_counts[cat['name']] = len(cat_arts)
        
        if os.path.exists(cat_file):
            with open(cat_file, 'r', encoding='utf-8') as f:
                content = f.read()
            items_html = "\n".join([build_article_item_html(a, project_name) for a in cat_arts])
            new_list = f'<div class="article-list">\n{items_html}\n            </div>'
            content = re.sub(r'<div class="article-list">.*?            </div>', new_list, content, flags=re.DOTALL)
            with open(cat_file, 'w', encoding='utf-8') as f: f.write(content)

    # 3. Update sidebar.js
    sidebar_path = os.path.join(project_path, "sidebar.js")
    if os.path.exists(sidebar_path):
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        for name, count in cat_counts.items():
            content = re.sub(rf'{{ name: "{name}", (.*?) count: \d+,', f'{{ name: "{name}", \\1 count: {count},', content)
        with open(sidebar_path, 'w', encoding='utf-8') as f: f.write(content)

    # 4. Update the actual post flies with correct category name
    for art in articles:
        file_path = os.path.join(project_path, art['filename'])
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        cat_name = art['category']['name']
        # Try to find the category span in the mass-fixed layout
        content = re.sub(r'(<div style="font-size: 0.85rem; margin-bottom: 0.5rem; opacity: 0.8;">.*? • ).*?(</div>)', 
                         f'\\1{cat_name}\\2', content)
        with open(file_path, 'w', encoding='utf-8') as f: f.write(content)

for d in os.listdir(CHILDREN_DIR):
    p = os.path.join(CHILDREN_DIR, d)
    if os.path.isdir(p): update_project(p)
