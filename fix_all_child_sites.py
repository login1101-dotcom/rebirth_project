import os
import re

site_configs = {
    'rebirth_child_english': {
        'brand': 'English Gym',
        'icon': '🇬🇧',
        'tagline': '世界と繋がる新しい力',
        'nav': [
            ('ホーム', 'index.html', ''),
            ('リーディング', 'category_reading.html', 'nav-reading'),
            ('リスニング', 'category_listening.html', 'nav-listening'),
            ('ライティング', 'category_writing.html', 'nav-writing'),
            ('スピーキング', 'category_speaking.html', 'nav-speaking'),
            ('データ表示', 'view_data.html', 'nav-view-data'),
            ('← Project Hub', '../../rebirth_parent/index.html', '')
        ],
        'author': 'Neo Eng 55',
        'author_desc': '字幕なしで映画を観るのが夢。<br>現在の目標：TOEIC 700',
        'cat_map': {'reading': 'リーディング', 'listening': 'リスニング', 'writing': 'ライティング', 'speaking': 'スピーキング'}
    },
    'rebirth_child_health': {
        'brand': 'Body Logic',
        'icon': '🥗',
        'tagline': '自分を愛する最初の力',
        'nav': [
            ('ホーム', 'index.html', ''),
            ('食事', 'category_diet.html', 'nav-diet'),
            ('筋トレ', 'category_muscle.html', 'nav-muscle'),
            ('睡眠', 'category_sleep.html', 'nav-sleep'),
            ('その他', 'category_others.html', 'nav-others'),
            ('データ表示', 'view_data.html', 'nav-view-data'),
            ('← Project Hub', '../../rebirth_parent/index.html', '')
        ],
        'author': 'Bio 55',
        'author_desc': '健康寿命を延ばす実験中。<br>現在の目標：体脂肪率 20%以下',
        'cat_map': {'diet': '食事', 'muscle': '筋トレ', 'sleep': '睡眠', 'others': 'その他'}
    },
    'rebirth_child_manga': {
        'brand': 'Manga Lab',
        'icon': '🎨',
        'tagline': '表現を広げる自由の翼',
        'nav': [
            ('ホーム', 'index.html', ''),
            ('練習', 'category_practice.html', 'nav-practice'),
            ('作品', 'category_works.html', 'nav-works'),
            ('データ表示', 'view_data.html', 'nav-view-data'),
            ('← Project Hub', '../../rebirth_parent/index.html', '')
        ],
        'author': 'Artist 55',
        'author_desc': '絵心ゼロからの挑戦。<br>現在の目標：LINEスタンプ販売',
        'cat_map': {'practice': '練習', 'works': '作品'}
    },
    'rebirth_child_typing': {
        'brand': 'Typing Lab',
        'icon': '⌨️',
        'tagline': 'アイデアを逃さない、ストレスフリーな指先へ。',
        'nav': [
            ('ホーム', 'index.html', ''),
            ('練習', 'category_daily.html', 'nav-daily'),
            ('分析', 'category_analysis.html', 'nav-analysis'),
            ('使用サイト・ツール', 'category_tools.html', 'nav-tools'),
            ('データ表示', 'view_data.html', 'nav-view-data'),
            ('← Project Hub', '../../rebirth_parent/index.html', '')
        ],
        'author': 'Admin 55',
        'author_desc': '51歳からのスキル獲得実験中。<br>現在の目標：WPM 100',
        'cat_map': {'daily': '練習', 'analysis': '分析', 'tools': 'ツール'}
    },
    'rebirth_child_novel': {
        'brand': "Writer's Desk",
        'icon': '✒️',
        'tagline': '物語を心から世界へ',
        'nav': [
            ('ホーム', 'index.html', ''),
            ('エッセイ', 'category_essay.html', 'nav-essay'),
            ('小説', 'category_short.html', 'nav-short'),
            ('その他', 'category_others.html', 'nav-others'),
            ('データ表示', 'view_data.html', 'nav-view-data'),
            ('← Project Hub', '../../rebirth_parent/index.html', '')
        ],
        'author': 'Novelist 55',
        'author_desc': '世界を創る実験中。<br>現在の目標：新人賞応募',
        'cat_map': {'essay': 'エッセイ', 'short': '小説', 'others': 'その他'}
    },
    'rebirth_child_youtube': {
        'brand': 'My YouTube Studio',
        'icon': '🎬',
        'tagline': 'もっといい世界へ',
        'nav': [
            ('ホーム', 'index.html', ''),
            ('撮影編集過程記録', 'category_process.html', 'nav-process'),
            ('使用ツール', 'category_tools.html', 'nav-tools'),
            ('完成作品', 'category_works.html', 'nav-works'),
            ('データ表示', 'view_data.html', 'nav-view-data'),
            ('← Project Hub', '../../rebirth_parent/index.html', '')
        ],
        'author': 'Vlogger 55',
        'author_desc': '映像で語る実験中。<br>現在の目標：収益化ライン到達',
        'cat_map': {'process': '記録', 'tools': 'ツール', 'works': '作品'}
    },
    'rebirth_child_reading': {
        'brand': 'Deep Reading',
        'icon': '📖',
        'tagline': '時空を超えて会いたい人たち',
        'nav': [
            ('ホーム', 'index.html', ''),
            ('データ表示', 'view_data.html', 'nav-view-data'),
            ('← All Projects', '../../rebirth_parent/index.html', '')
        ],
        'author': 'Reader 55',
        'author_desc': '時空を超えた対話中。<br>魂の読書記録。',
        'cat_map': {}
    }
}

def upgrade_file(dir_path, filename, config):
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    is_index = filename == 'index.html'
    
    # Check if upgrade is needed (either tagline or sidebar or breadcrumb missing)
    has_tagline = config['tagline'] in content
    has_sidebar = '<aside class="sidebar">' in content or is_index
    has_breadcrumb = 'class="breadcrumb"' in content or is_index
    
    if has_tagline and has_sidebar and has_breadcrumb:
        return

    print(f"Upgrading {filepath}")

    # Ensure Google Fonts
    if 'fonts.googleapis.com' not in content:
        fonts_code = """    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
"""
        content = re.sub(r'(<meta charset="UTF-8">)', r'\1\n' + fonts_code, content)

    # Ensure Favicon
    if '<link rel="icon"' not in content:
        icon_code = f"""    <link rel="icon"
        href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>{config['icon']}</text></svg>">"""
        content = re.sub(r'(</head>)', r'    ' + icon_code + r'\n\1', content)

    # Replace Header
    header_pattern = re.compile(r'<header>.*?</header>', re.DOTALL)
    
    nav_items = []
    for label, link, css_class in config['nav']:
        active_class = ""
        if css_class:
            short_class = css_class.replace('nav-', '')
            if f'bg-{short_class}' in content or f'text-{short_class}' in content or f'category_{short_class}' in filename:
                active_class = "active"
        elif label == 'ホーム' and is_index:
            active_class = "active"
        
        nav_items.append(f'<li><a class="{css_class} {active_class}" href="{link}">{label}</a></li>')
    
    nav_html = "\n                    ".join(nav_items)
    
    full_header = f"""    <header>
        <div class="container header-inner">
            <a href="index.html" class="site-brand"><span>{config['icon']}</span> {config['brand']}<span
                    style="font-size: 1.0rem; color: #334155; margin-left: 15px; font-weight: 600; letter-spacing: 0.05em;">{config['tagline']}</span></a>
            <nav class="main-nav">
                <ul>
                    {nav_html}
                </ul>
            </nav>
        </div>
    </header>"""
    content = header_pattern.sub(full_header, content)

    # Ensure Breadcrumb in single posts
    if not is_index and 'class="breadcrumb"' not in content and '<article' in content:
        # Detect category
        found_cat = None
        for key, val in config['cat_map'].items():
            if f'bg-{key}' in content or f'text-{key}' in content or f'category_{key}' in filename:
                found_cat = (key, val)
                break
        
        if found_cat:
            breadcrumb_code = f"""                    <div class="breadcrumb" style="font-size:0.9rem; color:var(--text-light); margin-bottom:1rem;">
                        <a href="index.html">ホーム</a> &gt; <a class="active" href="category_{found_cat[0]}.html">{found_cat[1]}</a>
                    </div>\n"""
            # Insert after the article header start
            content = re.sub(r'(<article class="single-post">\s*<header[^>]*>)', r'\1\n' + breadcrumb_code, content)

    # Ensure Sidebar
    if not is_index and '<aside class="sidebar">' not in content and 'main-layout' in content:
        cat_items = []
        for label, link, css_class in config['nav']:
            if css_class and 'nav-' in css_class and 'view-data' not in css_class:
                short_class = css_class.replace('nav-', '')
                active_class = "active" if f'bg-{short_class}' in content or f'text-{short_class}' in content else ""
                # Count placeholder
                count = "(2)"
                cat_items.append(f'<li><a href="{link}" class="{active_class} text-{short_class}">{label} {count}</a></li>')
        cat_html = "\n                    ".join(cat_items)

        sidebar_code = f"""
        <!-- Sidebar (Right) -->
        <aside class="sidebar">

            <!-- Author Widget -->
            <div class="widget profile-widget">
                <div class="profile-img"></div>
                <h3 style="font-size:1.1rem; margin-bottom:0.5rem;">{config['author']}</h3>
                <p style="font-size:0.9rem; color:var(--text-light); line-height:1.6;">
                    {config['author_desc']}
                </p>
            </div>

            <!-- AdSense Widget (Top) -->
            <div class="widget">
                <h4 class="widget-label"
                    style="font-size:0.7rem; color:#999; margin-bottom:0.5rem; text-transform:uppercase;">Sponsored</h4>
                <div class="adsense-placeholder">
                    Ads Display
                </div>
            </div>

            <!-- Categories -->
            <div class="widget">
                <h3 class="widget-title">Categories</h3>
                <ul style="list-style:none; line-height:2.2;">
                    {cat_html}
                </ul>
            </div>

        </aside>"""
        if '</main>' in content:
            content = re.sub(r'(</main>)', r'\1' + sidebar_code, content)

    # Ensure Footer
    if 'child-footer' not in content:
        footer_code = f"""
    <footer class="child-footer">
        <div class="container">
            <p>&copy; 2025 {config['brand']} | Re:Birth 55 Project</p>
        </div>
    </footer>
"""
        content = re.sub(r'(</body>)', footer_code + r'\1', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

base_path = '/Users/jono/Desktop/rebirth_project/children'
for dir_name, config in site_configs.items():
    dir_path = os.path.join(base_path, dir_name)
    if os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            if filename.endswith('.html'):
                upgrade_file(dir_path, filename, config)
