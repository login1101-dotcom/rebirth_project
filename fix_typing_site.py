import os
import re

def fix_typing_site():
    dir_path = '/Users/jono/Desktop/rebirth_project/children/rebirth_child_typing'
    files = [f for f in os.listdir(dir_path) if f.endswith('.html')]
    
    cat_map = {
        'daily': '練習',
        'analysis': '分析',
        'tools': '使用サイト・ツール'
    }

    for filename in files:
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        is_index = filename == 'index.html'
        is_category = filename.startswith('category_')
        is_post = filename.startswith('post_')
        
        updated = False

        # 1. Clean up multi-active nav in header (Typing site specific bug)
        # Find the nav block
        nav_match = re.search(r'<nav class="main-nav">.*?</nav>', content, re.DOTALL)
        if nav_match:
            nav_html = nav_match.group(0)
            # Remove all 'active' classes first
            clean_nav = re.sub(r'\s*active', '', nav_html)
            
            # Set correct active class
            if is_index:
                clean_nav = clean_nav.replace('href="index.html" class=" "', 'href="index.html" class="active"')
            elif is_category or is_post:
                for key in cat_map:
                    if f'_{key}' in filename or f'bg-{key}' in content or f'text-{key}' in content:
                        clean_nav = clean_nav.replace(f'nav-{key}', f'nav-{key} active')
                        break
            
            if clean_nav != nav_html:
                content = content.replace(nav_html, clean_nav)
                updated = True

        # 2. Add Breadcrumb to articles and category pages if missing
        if not is_index and 'class="breadcrumb"' not in content:
            # Detect category
            found_key = None
            found_label = None
            for key, label in cat_map.items():
                if f'_{key}' in filename or f'bg-{key}' in content or f'text-{key}' in content:
                    found_key = key
                    found_label = label
                    break
            
            if found_key:
                breadcrumb_html = f"""            <div class="breadcrumb" style="font-size:0.9rem; color:var(--text-light); margin-bottom:1.5rem;">
                <a href="index.html">ホーム</a> &gt; <a class="active" href="category_{found_key}.html">{found_label}</a>
            </div>\n"""
                
                # Insert point: before article-list in category pages, or inside article header in posts
                if is_category:
                    content = re.sub(r'(<div class="article-list")', breadcrumb_html + r'\1', content)
                elif is_post:
                    content = re.sub(r'(<article class="single-post">\s*<header[^>]*>)', r'\1\n' + breadcrumb_html, content)
                
                updated = True

        # 3. Add Author Description more fully in sidebar
        if '51歳からのスキル獲得実験中。' in content and '現在の目標：WPM 100' not in content:
            content = content.replace('51歳からのスキル獲得実験中。', '51歳からのスキル獲得実験中。<br>現在の目標：WPM 100')
            updated = True

        if updated:
            print(f"Fixed {filename}")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

fix_typing_site()
