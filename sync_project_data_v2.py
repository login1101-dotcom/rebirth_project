import os
import re
import json

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

# Configuration matching the USER's viewed CSS and Nav structure
PROJECT_CONFIG = {
    "rebirth_child_health": {
        "title": "Body Logic",
        "categories": [
            {"name": "食事", "id": "diet", "keywords": ["食事", "おにぎり", "パン", "オートミール", "腹", "食", "ダイエット", "暴食", "いもパン", "サンドイッチ"]},
            {"name": "筋トレ", "id": "muscle", "keywords": ["筋トレ", "トレーニング", "ダンベル", "ウォーキング", "散歩", "筋肉"]},
            {"name": "睡眠", "id": "sleep", "keywords": ["睡眠", "枕", "寝", "疲れ"]},
            {"name": "その他", "id": "others", "keywords": ["サプリ", "姿勢", "腰", "幸福"]}
        ],
        "default_cat": "食事",
        "logo_map": {"diet": "🥗", "muscle": "💪", "sleep": "💤", "others": "⚙️"}
    },
    "rebirth_child_english": {
        "title": "English Gym",
        "categories": [
            {"name": "リーディング", "id": "reading", "keywords": ["Reading", "多読", "洋書", "Kindle", "リーディング"]},
            {"name": "リスニング", "id": "listening", "keywords": ["Listening", "リスニング", "聴", "Podcast", "ポッドキャスト", "Let It Be", "CNN"]},
            {"name": "ライティング", "id": "writing", "keywords": ["Writing", "ライティング", "書く", "日記", "To-Do", "Essay"]},
            {"name": "スピーキング", "id": "speaking", "keywords": ["Speaking", "スピーキング", "独り言", "会話"]}
        ],
        "default_cat": "リーディング",
        "logo_map": {"reading": "📖", "listening": "🎵", "writing": "✍️", "speaking": "🗣️"}
    },
    "rebirth_child_reading": {
        "title": "Deep Reading",
        "categories": [
            {"name": "善の研究", "id": "nishida", "keywords": ["善の研究", "西田", "純粋経験", "主客未分"]},
            {"name": "生命とは何か", "id": "schrodinger", "keywords": ["生命とは何か", "シュレーディンガー", "エントロピー", "生命"]},
            {"name": "日本はなぜ", "id": "yamamoto", "keywords": ["日本はなぜ", "山本七平", "精神主義", "合理的"]}
        ],
        "default_cat": "善の研究",
        "logo_map": {"nishida": "📘", "schrodinger": "🧬", "yamamoto": "🇯🇵"}
    },
    "rebirth_child_novel": {
        "title": "Writer's Desk",
        # Aligned with CSS (.essay, .short, .other) and Nav
        "categories": [
            {"name": "エッセイ", "id": "essay", "keywords": ["考察", "思考", "エッセイ", "雑記", "食", "ストレス", "考え", "日々", "台本"]}, 
            {"name": "小説", "id": "short", "keywords": ["小説", "短編", "連載", "第", "話", "物語", "ストーリー"]},
            {"name": "その他", "id": "others", "keywords": ["メモ", "設定", "プロット", "その他"]}
        ],
        "default_cat": "エッセイ",
        "logo_map": {"essay": "✒️", "short": "📚", "others": "📝"}
    },
    "rebirth_child_youtube": {
        "title": "Movie Studio",
        "categories": [
            {"name": "動画", "id": "movie", "keywords": ["動画", "Vlog", "再生"]},
            {"name": "機材", "id": "tools", "keywords": ["機材", "カメラ", "マイク", "ツール", "編集"]},
            {"name": "分析", "id": "analysis", "keywords": ["分析", "データ", "登録者"]}
        ],
        "default_cat": "動画",
        "logo_map": {"movie": "🎬", "tools": "🛠️", "analysis": "📈"}
    },
    "rebirth_child_manga": {
        "title": "Comic Atelier",
        "categories": [
            {"name": "レビュー", "id": "review", "keywords": ["レビュー", "感想", "読了"]},
            {"name": "おすすめ本", "id": "list", "keywords": ["おすすめ", "厳選", "ベスト"]},
            {"name": "ニュース", "id": "news", "keywords": ["ニュース", "新刊", "発売日"]}
        ],
        "default_cat": "レビュー",
        "logo_map": {"review": "📚", "list": "📑", "news": "📰"}
    },
    "rebirth_child_typing": {
        "title": "Typing Lab",
        "categories": [
            {"name": "練習", "id": "daily", "keywords": ["記録", "スコア", "練習", "苦戦", "矯正"]},
            {"name": "分析", "id": "analysis", "keywords": ["分析", "データ", "推移", "効率化"]},
            {"name": "キーボード", "id": "hardware", "keywords": ["キーボード", "軸", "メカニカル"]}
        ],
        "default_cat": "練習",
        "logo_map": {"daily": "⌨️", "analysis": "📈", "hardware": "🔌"}
    }
}

def get_article_info(file_path, project_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    title = re.sub(r'<.*?>', '', title_match.group(1)).strip() if title_match else "No Title"
    
    date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
    date = date_match.group(1) if date_match else "2026.01.01"
    
    excerpt_match = re.search(r'<div class="post-content">.*?<p.*?>(.*?)</p>', content, re.DOTALL)
    excerpt = re.sub(r'<.*?>', '', excerpt_match.group(1)).strip() if excerpt_match else ""
    if len(excerpt) > 80: excerpt = excerpt[:77] + "..."
    if not excerpt: excerpt = "記事の内容..."

    config = PROJECT_CONFIG.get(project_name)
    category = None
    if config:
        for cat in config['categories']:
            # Check keywords against title AND content snippet for better accuracy
            check_text = title + " " + excerpt
            if any(kw.lower() in check_text.lower() for kw in cat['keywords']):
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
    cat_name = art['category']['name'] if art['category'] else "Blog"
    logo = PROJECT_CONFIG.get(proj_name, {}).get('logo_map', {}).get(cat_id, "📄")
    
    # Matches CSS classes like .essay, .short, .other
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

def clean_and_update_file(file_path, articles, proj_name):
    if not os.path.exists(file_path): return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    prefix_match = re.search(r'(.*?)<div class="article-list">', content, re.DOTALL)
    if not prefix_match: return
    prefix = prefix_match.group(1)
    
    suffix_match = re.search(r'</main>(.*)', content, re.DOTALL)
    if not suffix_match:
        suffix_match = re.search(r'<!-- Sidebar -->(.*)', content, re.DOTALL)
    if not suffix_match:
        suffix_match = re.search(r'<aside(.*)', content, re.DOTALL)
    
    if not suffix_match: return
    suffix = suffix_match.group(0)
    
    items_html = "\n".join([build_article_item_html(a, proj_name) for a in articles])
    new_content = f"{prefix}<div class=\"article-list\">\n{items_html}\n            </div>\n\n        {suffix}"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def update_sidebar_js(project_path, counts, config):
    # Completely rebuild sidebar.js to ensure consistency
    sidebar_path = os.path.join(project_path, "sidebar.js")
    
    cats_data = []
    for cat in config['categories']:
        cats_data.append({
            "name": cat['name'],
            "link": f"category_{cat['id']}.html",
            "count": counts.get(cat['id'], 0),
            "className": f"text-{cat['id']}"
        })
    
    js_content = f"""document.addEventListener('DOMContentLoaded', function () {{
    const categories = {json.dumps(cats_data, ensure_ascii=False, indent=4)};

    const currentPath = window.location.pathname.split('/').pop();
    const listContainer = document.getElementById('category-list');

    if (listContainer) {{
        const ul = document.createElement('ul');
        ul.style.listStyle = 'none';
        ul.style.lineHeight = '2';

        categories.forEach(cat => {{
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = cat.link;
            a.textContent = `${{cat.name}} (${{cat.count}})`;
            if (cat.className) a.className = cat.className;

            if (currentPath === cat.link) {{
                a.classList.add('active');
            }}

            li.appendChild(a);
            ul.appendChild(li);
        }});

        listContainer.appendChild(ul);
    }}
}});"""
    
    with open(sidebar_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

def update_project(project_path):
    project_name = os.path.basename(project_path)
    if project_name not in PROJECT_CONFIG: return
    
    print(f"Syncing: {project_name}")
    config = PROJECT_CONFIG[project_name]
    
    # 1. Gather all articles
    articles = []
    for f in os.listdir(project_path):
        if (f.startswith("post_") or f.startswith("read_")) and f.endswith(".html"):
            articles.append(get_article_info(os.path.join(project_path, f), project_name))
    
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # 2. Count for sidebar
    cat_counts = {} # by ID
    for cat in config['categories']:
        cat_counts[cat['id']] = 0
        
    for art in articles:
        cid = art['category']['id']
        cat_counts[cid] = cat_counts.get(cid, 0) + 1

    # 3. Update index.html
    clean_and_update_file(os.path.join(project_path, "index.html"), articles[:8], project_name)

    # 4. Update/Create category_*.html
    for cat in config['categories']:
        cat_file = os.path.join(project_path, f"category_{cat['id']}.html")
        cat_arts = [a for a in articles if a['category']['id'] == cat['id']]
        
        # Ensure file exists or create it from template if missing (rebuild logic)
        # For now, simplistic update if exists. If not, we might need to copy index.html
        if not os.path.exists(cat_file):
            # Create a simple category page by copying index and stripping content
            # This is a fallback to ensure links don't break
            if os.path.exists(os.path.join(project_path, "index.html")):
                with open(os.path.join(project_path, "index.html"), 'r', encoding='utf-8') as f:
                    base_html = f.read()
                # Basic cleanup to make it a category page title
                base_html = base_html.replace("<title>Re:Birth", f"<title>{cat['name']} | Re:Birth")
                with open(cat_file, 'w', encoding='utf-8') as f:
                    f.write(base_html)

        clean_and_update_file(cat_file, cat_arts, project_name)

    # 5. Update sidebar.js (REBUILD it, don't just replace)
    update_sidebar_js(project_path, cat_counts, config)

    # 6. Update individual posts metadata (Category Tag in Header)
    for art in articles:
        f_path = os.path.join(project_path, art['filename'])
        with open(f_path, 'r', encoding='utf-8') as f: c = f.read()
        # Regex to locate the metadata line: 2026.01.06 • CategoryClassName
        # We want to force update it.
        # Pattern: <div style="font-size: 0.85rem; ...">DATE • .*?</div>
        
        # Try a robust regex
        c = re.sub(r'(<div style="font-size: 0\.85rem;.*?opacity: 0\.8;">.*? • ).*?(</div>)', 
                   f'\\1{art["category"]["name"]}\\2', c)
        
        with open(f_path, 'w', encoding='utf-8') as f: f.write(c)

if __name__ == "__main__":
    for d in os.listdir(CHILDREN_DIR):
        p = os.path.join(CHILDREN_DIR, d)
        if os.path.isdir(p): update_project(p)
