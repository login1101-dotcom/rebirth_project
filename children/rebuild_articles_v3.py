
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def clean_and_rebuild_articles(site_dir):
    site_name = os.path.basename(site_dir)
    print(f"Checking {site_name}...")

    # 1. Start Fresh: delete all existing generated post pages
    for f in os.listdir(site_dir):
        if (f.startswith("post_") or f.startswith("article_")) and f.endswith(".html"):
            os.remove(os.path.join(site_dir, f))

    # 2. Extract unique articles from the source of truth (index.html)
    article_list = []
    seen_titles = set()

    truth_path = os.path.join(site_dir, "index.html")
    if not os.path.exists(truth_path): return

    with open(truth_path, 'r', encoding='utf-8') as f:
        idx_html = f.read()

    cards = re.findall(r'<article class="article-card".*?</article>', idx_html, re.DOTALL)
    for card in cards:
        title_m = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card, re.DOTALL)
        if not title_m: continue
        title = title_m.group(1).strip()
        if title in seen_titles: continue
        seen_titles.add(title)

        date_m = re.search(r'<span class="date">\s*(.*?)\s*</span>', card)
        cat_m = re.search(r'class="cat text-([a-z0-9_-]+)".*?>\s*(.*?)\s*</a>', card, re.DOTALL)
        excerpt_m = re.search(r'<p class="article-excerpt">\s*(.*?)\s*</p>', card, re.DOTALL)

        article_list.append({
            "title": title,
            "date": date_m.group(1).strip() if date_m else "2025.12.24",
            "cat_slug": cat_m.group(1).strip() if cat_m else "others",
            "cat_name": cat_m.group(2).strip() if cat_m else "その他",
            "excerpt": excerpt_m.group(1).strip() if excerpt_m else ""
        })

    # 3. Handle Category Pages too (they might have unique articles not on home)
    for fname in os.listdir(site_dir):
        if fname.startswith("category_") and fname.endswith(".html"):
            with open(os.path.join(site_dir, fname), 'r', encoding='utf-8') as f:
                cat_html = f.read()
            cards = re.findall(r'<article class="article-card".*?</article>', cat_html, re.DOTALL)
            for card in cards:
                title_m = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card, re.DOTALL)
                if not title_m: continue
                title = title_m.group(1).strip()
                if title in seen_titles: continue
                seen_titles.add(title)
                
                date_m = re.search(r'<span class="date">\s*(.*?)\s*</span>', card)
                cat_m = re.search(r'class="cat text-([a-z0-9_-]+)".*?>\s*(.*?)\s*</a>', card, re.DOTALL)
                excerpt_m = re.search(r'<p class="article-excerpt">\s*(.*?)\s*</p>', card, re.DOTALL)
                
                article_list.append({
                    "title": title,
                    "date": date_m.group(1).strip() if date_m else "2025.12.24",
                    "cat_slug": cat_m.group(1).strip() if cat_m else "others",
                    "cat_name": cat_m.group(2).strip() if cat_m else "その他",
                    "excerpt": excerpt_m.group(1).strip() if excerpt_m else ""
                })

    # 4. Template processing
    template_path = os.path.join(site_dir, "article.html")
    if not os.path.exists(template_path): return
    with open(template_path, 'r', encoding='utf-8') as f:
        tpl_raw = f.read()

    # Find the main area more flexibly
    main_m = re.search(r'(<main[^>]*>).*?(</main>)', tpl_raw, re.DOTALL)
    if not main_m: return
    main_open = main_m.group(1)
    main_close = main_m.group(2)

    # Simplified, Clean Structure for Single Post
    post_tpl = """
            <article class="single-post">
                <header class="bg-styled bg-{cat_slug}">
                    <div style="font-size:0.9rem; color:var(--text-light); margin-bottom:1rem;">
                        <a href="index.html">ホーム</a> &gt; <a href="category_{cat_slug}.html">{cat_name}</a>
                    </div>
                    <h1>{title}</h1>
                    <div class="article-meta">
                        <span class="date">{date}</span> • <span class="cat text-{cat_slug}">{cat_name}</span>
                    </div>
                </header>

                <div class="post-content">
                    <p style="font-weight:bold; font-size:1.2rem; margin-bottom:2rem; line-height:1.6; color: var(--text-main);">{excerpt}</p>
                    
                    <p>Re:Birth 55プロジェクトへようこそ。51歳からの「再定義」をテーマに、日々の試行錯誤を記録しています。</p>
                    <p>この記事では <strong>「{cat_name}」</strong> について、現在の進捗と得られた気づきをシェアします。同じ世代で新しいことに挑戦している方のヒントになれば幸いです。</p>

                    <h2>1. 実践の記録と気づき</h2>
                    <p>「{title}」の実践を通じて最も強く感じたのは、基礎の重要性です。派手なテクニックに走る前に、土台をしっかりと固めることが、最終的には最短ルートになるということを再確認しました。</p>
                    
                    <div class="data-notice">
                        <strong>💡 お知らせ:</strong><br>
                        この活動に関する生データや分析グラフは、上部メニューの「データ表示」からリアルタイムに確認いただけます。
                    </div>

                    <h2>2. 今後の展望</h2>
                    <p>今回の気づきを元に、来週からはさらに踏み込んだ検証を行う予定です。一歩一歩、焦らず、しかし着実に進んでいきたいと思います。</p>
                    <p>最後までお読みいただきありがとうございました。共に、輝かしい50代を築いていきましょう！</p>
                </div>
            </article>
    """

    # 5. Generate and Link
    for i, art in enumerate(article_list, 1):
        fname = f"post_{i}.html"
        art["id"] = fname
        
        content = main_open + "\n" + post_tpl.format(**art) + "\n" + main_close
        full_html = tpl_raw.replace(main_m.group(0), content)
        
        # Clean title tag
        full_html = re.sub(r'<title>.*?</title>', f'<title>{art["title"]} | {site_name}</title>', full_html)

        with open(os.path.join(site_dir, fname), 'w', encoding='utf-8') as f:
            f.write(full_html)

    # 6. Global Link Update
    for fname in os.listdir(site_dir):
        if not fname.endswith(".html"): continue
        fpath = os.path.join(site_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()

        for art in article_list:
            def replacer(m):
                card = m.group(0)
                if art["title"] in card:
                    # Replace the link to become post_N.html
                    # Target the first <a> wrap around the card
                    fixed = re.sub(r'href="(?!category_|index\.html|view_data\.html|../../)[^"]+\.html"', f'href="{art["id"]}"', card)
                    return fixed
                return card
            html = re.sub(r'<article class="article-card".*?</article>', replacer, html, flags=re.DOTALL)
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)

    print(f"  Successfully rebuilt {len(article_list)} articles for {site_name}")

def main():
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            clean_and_rebuild_articles(site_path)

if __name__ == "__main__":
    main()
