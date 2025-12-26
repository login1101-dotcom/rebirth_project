import os
import re

def upgrade_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already upgraded
    if '世界と繋がる新しい力' in content:
        return

    print(f"Upgrading {filepath}")

    # Add Google Fonts if missing
    if 'fonts.googleapis.com' not in content:
        fonts_code = """    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
"""
        content = re.sub(r'(<meta charset="UTF-8">)', r'\1\n' + fonts_code, content)

    # Add Icon if missing
    if '<link rel="icon"' not in content:
        icon_code = """    <link rel="icon"
        href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🇬🇧</text></svg>">"""
        content = re.sub(r'(</head>)', r'    ' + icon_code + r'\n\1', content)

    # Replace Header
    header_pattern = re.compile(r'<header>.*?</header>', re.DOTALL)
    
    # Determine active classes based on content or filename
    active_reading = 'active' if 'bg-reading' in content or 'category_reading' in filepath else ''
    active_listening = 'active' if 'bg-listening' in content or 'category_listening' in filepath else ''
    active_writing = 'active' if 'bg-writing' in content or 'category_writing' in filepath else ''
    active_speaking = 'active' if 'bg-speaking' in content or 'category_speaking' in filepath else ''

    full_header = f"""    <header>
        <div class="container header-inner">
            <a href="index.html" class="site-brand"><span>🇬🇧</span> English Gym<span
                    style="font-size: 1.0rem; color: #334155; margin-left: 15px; font-weight: 600; letter-spacing: 0.05em;">世界と繋がる新しい力</span></a>
            <nav class="main-nav">
                <ul>
                    <li><a href="index.html">ホーム</a></li>
                    <li><a class="nav-reading {active_reading}" href="category_reading.html">リーディング</a></li>
                    <li><a class="nav-listening {active_listening}" href="category_listening.html">リスニング</a></li>
                    <li><a class="nav-writing {active_writing}" href="category_writing.html">ライティング</a></li>
                    <li><a class="nav-speaking {active_speaking}" href="category_speaking.html">スピーキング</a></li>
                    <li><a href="view_data.html" class="nav-view-data">データ表示</a></li>
                    <li><a href="../../rebirth_parent/index.html">← Project Hub</a></li>
                </ul>
            </nav>
        </div>
    </header>"""
    content = header_pattern.sub(full_header, content)

    # Ensure Sidebar follows premium pattern
    if '<aside class="sidebar">' not in content and 'main-layout' in content:
        sidebar_code = """
        <!-- Sidebar (Right) -->
        <aside class="sidebar">

            <!-- Author Widget -->
            <div class="widget profile-widget">
                <div class="profile-img"></div>
                <h3 style="font-size:1.1rem; margin-bottom:0.5rem;">Neo Eng 55</h3>
                <p style="font-size:0.9rem; color:var(--text-light); line-height:1.6;">
                    字幕なしで映画を観るのが夢。<br>
                    現在の目標：TOEIC 700
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
                    <li><a href="category_reading.html" class="text-reading">リーディング (2)</a></li>
                    <li><a href="category_listening.html" class="text-listening">リスニング (2)</a></li>
                    <li><a href="category_writing.html" class="text-writing">ライティング (2)</a></li>
                    <li><a href="category_speaking.html" class="text-speaking">スピーキング (2)</a></li>
                </ul>
            </div>

        </aside>"""
        # Insert before closing div of main-layout
        content = re.sub(r'(</main>)', r'\1' + sidebar_code, content)

    # Add Footer if missing
    if 'child-footer' not in content:
        footer_code = """
    <footer class="child-footer">
        <div class="container">
            <p>&copy; 2025 English Gym | Re:Birth 55 Project</p>
        </div>
    </footer>
"""
        content = re.sub(r'(</body>)', footer_code + r'\1', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

directory = '/Users/jono/Desktop/rebirth_project/children/rebirth_child_english'
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        upgrade_file(os.path.join(directory, filename))
