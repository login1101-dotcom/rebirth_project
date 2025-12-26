
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def clean_and_rebuild_articles(site_dir):
    site_name = os.path.basename(site_dir)
    # 1. First, delete all existing post_*.html files to start fresh
    for f in os.listdir(site_dir):
        if f.startswith("post_") and f.endswith(".html"):
            os.remove(os.path.join(site_dir, f))

    # 2. Extract unique articles from all "main" pages (index and category pages)
    article_list = [] # List of dicts {title, excerpt, date, cat_slug, cat_name}
    seen_titles = set()

    for fname in os.listdir(site_dir):
        # We only scan "source" pages, not the generated ones (which we just deleted)
        if not fname.endswith(".html") or fname.startswith("post_") or fname.startswith("article_"): continue
        if fname == "article.html": continue # This is our template

        path = os.path.join(site_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Regex to find cards
        cards = re.findall(r'<article class="article-card".*?</article>', html, re.DOTALL)
        for card in cards:
            title_m = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card, re.DOTALL)
            if not title_m: continue
            title = title_m.group(1).strip()
            if title in seen_titles: continue
            seen_titles.add(title)

            # Meta data
            date_m = re.search(r'<span class="date">\s*(.*?)\s*</span>', card)
            cat_m = re.search(r'class="cat text-([a-z0-9_-]+)".*?>\s*(.*?)\s*</a>', card, re.DOTALL)
            excerpt_m = re.search(r'<p class="article-excerpt">\s*(.*?)\s*</p>', card, re.DOTALL)

            article_list.append({
                "title": title,
                "date": date_m.group(1) if date_m else "2025.12.24",
                "cat_slug": cat_m.group(1) if cat_m else "others",
                "cat_name": cat_m.group(2) if cat_m else "その他",
                "excerpt": excerpt_m.group(1).strip() if excerpt_m else ""
            })

    # 3. Create a clean template from the site's article.html (if it exists)
    template_path = os.path.join(site_dir, "article.html")
    if not os.path.exists(template_path): return
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_raw = f.read()

    # Clean the template: remove hardcoded post content but keep the structure
    # We look for <main class="content-area single-post"> ... </main>
    main_match = re.search(r'(<main class="content-area single-post">).*?(</main>)', template_raw, re.DOTALL)
    if not main_match: return
    
    header_html = """
            <header class="bg-styled bg-{cat_slug}">
                <div style="font-size:0.9rem; color:var(--text-light); margin-bottom:1rem;">
                    <a href="index.html">ホーム</a> &gt; <a href="category_{cat_slug}.html">{cat_name}</a>
                </div>
                <h1>{title}</h1>
                <div class="article-meta">
                    <span class="date">{date}</span> • <span class="cat text-{cat_slug}">{cat_name}</span>
                </div>
            </header>
    """
    
    content_html = """
            <div class="post-content">
                <p style="font-weight:bold; font-size:1.2rem; margin-bottom:2rem; line-height:1.6;">{excerpt}</p>
                <p>51歳からの再挑戦、Re:Birth 55プロジェクトへようこそ。</p>
                <p>この記事では、<strong>「{cat_name}」</strong>に関する最新の知見と、私自身の体験に基づいた実践的なステップを紹介します。加齢に負けず、日々進化し続けるための具体的なヒントをまとめています。</p>
                
                <h2>1. この記事の要点</h2>
                <p>「{title}」において最も重要なのは、小さな変化を楽しみ、それをデータとして記録することです。自分を客観的に見ることで、驚くほどスムーズにスキルアップが進みます。</p>
                
                <div class="data-notice">
                    <strong>💡 Check Point:</strong><br>
                    このトピックに関する詳細な分析や数値データは、上部メニューの「データ表示」から確認できます。日々の積み重ねがグラフとして可視化されており、モチベーション維持に最適です。
                </div>

                <h2>2. 今日から始めるアクション</h2>
                <p>大きな目標も、最初は数分間のトレーニングから。この記事を読み終えたら、まずは簡単な振り返りから始めてみてください。</p>
                <p>共に、実りある50代を追求していきましょう！</p>
            </div>
    """

    # 4. Generate the post files
    for i, art in enumerate(article_list, 1):
        filename = f"post_{i}.html"
        art["id"] = filename
        
        # Replace main section
        new_main = main_match.group(1) + \
                   header_html.format(**art) + \
                   content_html.format(**art) + \
                   main_match.group(2)
        
        # Full HTML
        full_html = template_raw.replace(main_match.group(0), new_main)
        
        # Update title tag
        full_html = re.sub(r'<title>.*?</title>', f'<title>{art["title"]} | {site_name}</title>', full_html)

        with open(os.path.join(site_dir, filename), 'w', encoding='utf-8') as f:
            f.write(full_html)

    # 5. Link all pages back to these new files
    for fname in os.listdir(site_dir):
        if not fname.endswith(".html"): continue
        fpath = os.path.join(site_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace links for each art
        for art in article_list:
            # We look for a card with THIS title
            # and swap its href to post_N.html
            def repl(m):
                card = m.group(0)
                if art["title"] in card:
                    # Swap ALL .html links inside this card to the correct post_N.html
                    # except the category ones which contain 'category_'
                    # and the index one
                    fixed = re.sub(r'href="(?!category_|index\.html|view_data\.html|../../)[^"]+\.html"', f'href="{art["id"]}"', card)
                    return fixed
                return card

            content = re.sub(r'<article class="article-card".*?</article>', repl, content, flags=re.DOTALL)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"  Rebuilt {len(article_list)} clean articles for {site_name}")

def main():
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            clean_and_rebuild_articles(site_path)

if __name__ == "__main__":
    main()
