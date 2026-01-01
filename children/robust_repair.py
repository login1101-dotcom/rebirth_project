
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def get_clean_cat_name(text):
    # Remove any emoji and HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove emojis (common ones)
    text = re.sub(r'[\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF]', '', text)
    return text.strip()

def fix_site_robustly(site_dir):
    site_name = os.path.basename(site_dir)
    print(f"Repairing {site_name}...")

    # 1. Clean up all previous mess
    for f in os.listdir(site_dir):
        if (f.startswith("post_") or f.startswith("article_")) and f.endswith(".html"):
            os.remove(os.path.join(site_dir, f))

    # 2. Extract Articles with MUCH better regex
    truth_path = os.path.join(site_dir, "index.html")
    if not os.path.exists(truth_path): return
    with open(truth_path, 'r', encoding='utf-8') as f:
        idx_html = f.read()

    cards = re.findall(r'<article class="article-card".*?</article>', idx_html, re.DOTALL)
    article_list = []
    seen_titles = set()

    for card in cards:
        title_m = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card, re.DOTALL)
        if not title_m: continue
        title = title_m.group(1).strip()
        if title in seen_titles: continue
        seen_titles.add(title)

        # Meta
        date_m = re.search(r'<span class="date">\s*(.*?)\s*</span>', card)
        # Use a non-greedy CAT match that stops at the first closing tag
        cat_m = re.search(r'class="cat text-([a-z0-9_-]+)"[^>]*>\s*(.*?)\s*</(?:span|a)>', card, re.DOTALL)
        excerpt_m = re.search(r'<p class="article-excerpt">\s*(.*?)\s*</p>', card, re.DOTALL)

        article_list.append({
            "title": title,
            "date": date_m.group(1).strip() if date_m else "2025.12.24",
            "cat_slug": cat_m.group(1).strip() if cat_m else "others",
            "cat_name": get_clean_cat_name(cat_m.group(2)) if cat_m else "その他",
            "excerpt": excerpt_m.group(1).strip() if excerpt_m else ""
        })

    # 3. Fix the Navigation in all files (including index.html)
    # We want: <li><a href="index.html">ホーム</a></li> followed by categories
    nav_match = re.search(r'<nav class="main-nav">\s*<ul>(.*?)</ul>\s*</nav>', idx_html, re.DOTALL)
    if nav_match:
        nav_ul_inner = nav_match.group(1)
        # Remove any existing "Home" or "ホーム" link to re-add it cleanly
        nav_ul_inner = re.sub(r'<li><a[^>]*href="index\.html"[^>]*>.*?</a></li>', '', nav_ul_inner)
        # Re-add it
        new_nav_inner = '<li><a href="index.html">ホーム</a></li>\n' + nav_ul_inner.strip()
        
        # Site specific adjustments (Novel Lab: 物語 -> 小説)
        if 'novel' in site_name:
            new_nav_inner = new_nav_inner.replace('物語', '小説')
    else:
        new_nav_inner = None

    # 4. Prepare Post Template
    template_path = os.path.join(site_dir, "article.html")
    if not os.path.exists(template_path): return
    with open(template_path, 'r', encoding='utf-8') as f:
        tpl_raw = f.read()

    # Define a PERFECTLY CLEAN single post structure
    post_tpl = """
            <article class="single-post">
                <header class="bg-styled bg-{cat_slug}">
                    <div class="breadcrumb" style="font-size:0.9rem; color:var(--text-light); margin-bottom:1rem;">
                        <a href="index.html">ホーム</a> &gt; <a href="category_{cat_slug}.html">{cat_name}</a>
                    </div>
                    <h1 style="color: var(--color-{cat_slug});">{title}</h1>
                    <div class="article-meta" style="font-size: 0.9rem; color: var(--text-light); margin-top: 0.5rem;">
                        <span class="date">{date}</span> • <span class="cat text-{cat_slug}">{cat_name}</span>
                    </div>
                </header>

                <div class="post-content" style="margin-top: 2rem;">
                    <p style="font-weight:700; font-size:1.2rem; margin-bottom:2rem; line-height:1.6; color: var(--text-main);">{excerpt}</p>
                    
                    <p>Re:Birth 55プロジェクトへようこそ。51歳からの「第2の人生」をより豊かにするために、日々の記録をありのままに綴っています。</p>
                    <p>今回のテーマは <strong>「{cat_name}」</strong> です。実際に取り組んでみて分かったこと、つまずいたこと、そして次に役立つヒントを整理しました。</p>

                    <h2 style="border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; margin-top: 2.5rem;">1. 今回の気づき</h2>
                    <p>「{title}」において最も重要だと感じたのは、数値化すること、そしてそれを楽しむことです。ただ練習するだけでなく、変化を可視化することでモチベーションが驚くほど維持しやすくなりました。</p>
                    
                    <div class="data-notice" style="background: #f8fafc; border-left: 4px solid var(--color-{cat_slug}); padding: 1.5rem; border-radius: 4px; margin: 2rem 0;">
                        <strong>💡 活動ログの確認:</strong><br>
                        詳しい分析データや推移グラフは、上部メニューの「データ表示」からリアルタイムで確認いただけます。
                    </div>

                    <h2 style="border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; margin-top: 2.5rem;">2. 次へのステップ</h2>
                    <p>一歩ずつ、しかし着実に。完璧を目指すのではなく、昨日より少しだけ前進していることを喜びながら、今後もこの活動を続けていきたいと思います。</p>
                    <p>皆さんの挑戦のヒントになれば幸いです。共に素晴らしい50代を追求していきましょう！</p>
                </div>
            </article>
    """

    # 5. Process all HTML files
    all_html_files = [f for f in os.listdir(site_dir) if f.endswith(".html")]
    for fname in all_html_files:
        fpath = os.path.join(site_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()

        # Update Nav in ALL files
        if new_nav_inner:
            html = re.sub(r'<nav class="main-nav">\s*<ul>.*?</ul>\s*</nav>', 
                          f'<nav class="main-nav"><ul>{new_nav_inner}</ul></nav>', 
                          html, flags=re.DOTALL)

        # Handle Active Class in Nav
        # First remove all active
        html = re.sub(r'class="([^"]*)\s+active\s*([^"]*)"', r'class="\1\2"', html)
        html = re.sub(r'class="active"', '', html)
        # Add to current
        html = re.sub(r'href="' + re.escape(fname) + r'"', f'class="active" href="{fname}"', html)
        # Handle some cases where class was already there
        html = html.replace('class=""', '').replace('class="active" class="', 'class="active ')

        # If it's the article template or any existing post, we REGENERATE it
        # Actually we only generate post_N.html
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)

    # 6. Generate the post_N.html files
    for i, art in enumerate(article_list, 1):
        filename = f"post_{i}.html"
        art["id"] = filename
        
        # Build page using article.html as container
        # Find where to inject
        main_m = re.search(r'(<main[^>]*>).*?(</main>)', tpl_raw, re.DOTALL)
        if not main_m: continue
        
        injected_main = main_m.group(1) + "\n" + post_tpl.format(**art) + "\n" + main_m.group(2)
        post_html = tpl_raw.replace(main_m.group(0), injected_main)
        
        # Final cleanup for the post (Update Title tag, etc.)
        post_html = re.sub(r'<title>.*?</title>', f'<title>{art["title"]} | {site_name}</title>', post_html)
        # Re-apply nav sync to this new file
        if new_nav_inner:
            post_html = re.sub(r'<nav class="main-nav">\s*<ul>.*?</ul>\s*</nav>', 
                              f'<nav class="main-nav"><ul>{new_nav_inner}</ul></nav>', 
                              post_html, flags=re.DOTALL)
        # Set active class for the post? Usually none are active since it's a subpage
        # but we can set the category as active if we want.
        cat_file = f"category_{art['cat_slug']}.html"
        post_html = re.sub(r'href="' + re.escape(cat_file) + r'"', f'class="active" href="{cat_file}"', post_html)

        with open(os.path.join(site_dir, filename), 'w', encoding='utf-8') as f:
            f.write(post_html)

    # 7. Final Link Update: Ensure every card in every file points to post_N.html
    # We do this again for EVERY file to be 100% sure
    for fname in os.listdir(site_dir):
        if not fname.endswith(".html"): continue
        fpath = os.path.join(site_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        for art in article_list:
            def link_replace(match):
                card = match.group(0)
                if art["title"] in card:
                    # Update the wrap link
                    card = re.sub(r'href="(?!category_|index\.html|view_data\.html|../../)[^"]+\.html"', f'href="{art["id"]}"', card)
                return card
            html = re.sub(r'<article class="article-card".*?</article>', link_replace, html, flags=re.DOTALL)
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)

if __name__ == "__main__":
    for item in sorted(os.listdir(base_dir)):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            fix_site_robustly(site_path)
