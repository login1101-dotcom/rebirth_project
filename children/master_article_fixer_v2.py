
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def fix_links_globally_refined(site_dir):
    article_db = {} 
    html_files = [f for f in os.listdir(site_dir) if f.endswith(".html") and not f.startswith("post_")]
    
    file_counter = 1
    
    for fname in html_files:
        path = os.path.join(site_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cards = re.findall(r'<article class="article-card".*?</article>', content, re.DOTALL)
        for card in cards:
            t_m = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card, re.DOTALL)
            if not t_m: continue
            title = t_m.group(1).strip()
            
            c_m = re.search(r'class="cat text-([a-z0-9_-]+)".*?>\s*(.*?)\s*</a>', card, re.DOTALL)
            cat_slug = c_m.group(1).strip() if c_m else "others"
            cat_name = c_m.group(2).strip() if c_m else "Others"
            
            e_m = re.search(r'<p class="article-excerpt">\s*(.*?)\s*</p>', card, re.DOTALL)
            excerpt = e_m.group(1).strip() if e_m else ""
            
            d_m = re.search(r'<span class="date">\s*(.*?)\s*</span>', card)
            date = d_m.group(1).strip() if d_m else "2025.12.24"
            
            if title not in article_db:
                target_filename = f"post_{file_counter}.html"
                file_counter += 1
                article_db[title] = {
                    "filename": target_filename,
                    "slug": cat_slug,
                    "name": cat_name,
                    "excerpt": excerpt,
                    "date": date
                }

    template_path = os.path.join(site_dir, "article.html")
    if not os.path.exists(template_path):
        candidates = [f for f in os.listdir(site_dir) if f.startswith("article") and f.endswith(".html")]
        if candidates: template_path = os.path.join(site_dir, candidates[0])
        else: return

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    for title, data in article_db.items():
        fpath = os.path.join(site_dir, data["filename"])
        new_c = template_content
        
        # 1. Meta / SEO
        new_c = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', new_c)
        new_c = re.sub(r'<h1>\s*(.*?)\s*</h1>', f'<h1>{title}</h1>', new_c, flags=re.DOTALL)
        
        # 2. Header Colors
        new_c = re.sub(r'class="bg-styled bg-[a-z0-9_-]+"', f'class="bg-styled bg-{data["slug"]}"', new_c)
        
        # 3. Breadcrumbs / Article Meta
        # home > category > post
        new_c = re.sub(r'<a href="category_[^"]*">.*?</a>', f'<a href="category_{data["slug"]}.html">{data["name"]}</a>', new_c)
        
        # Find the meta line (Date • Category)
        # 2025.05.20 • Diet / Meal -> Correct it
        new_c = re.sub(r'(\d{4}\.\d{2}\.\d{2})\s*•\s*[^<]*', f'{data["date"]} • {data["name"]}', new_c)
        
        # Also handle the <span> case
        new_c = re.sub(r'class="cat text-[a-z0-9_-]+"(.*?>).*?</a>', 
                       f'class="cat text-{data["slug"]}"\\1{data["name"]}</a>', new_c)

        # 4. Tags cleanup
        # Look for <div class="article-tags">...</div>
        tag_pattern = r'<div class="article-tags">.*?</div>'
        new_tags = f'<div class="article-tags" style="margin-top:1rem;"><span style="background:#f1f5f9; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.8rem; margin-right:0.5rem;">#{data["name"]}</span></div>'
        new_c = re.sub(tag_pattern, new_tags, new_c, flags=re.DOTALL)

        # 5. Body Content Rewrite
        # We replace the content inside <div class="post-content">
        parts = re.split(r'(<div class="post-content">)', new_c)
        if len(parts) > 2:
            body_start = parts[1]
            rest = parts[2]
            
            # Find the closing tag for post-content
            # This is tricky because there might be nested divs. 
            # But usually it ends before <!-- Sidebar --> or <hr> or </main>
            
            # Simple approach: find first </div> that isn't matched? No.
            # Best way: we know the structure usually has </main> after post-content.
            sub_parts = re.split(r'(</main>)', rest)
            if len(sub_parts) > 1:
                # sub_parts[0] is the old body
                new_body = f"""
    <p style="font-weight:bold; margin-bottom:2rem;">{data["excerpt"]}</p>
    
    <p>51歳からの再挑戦、Re:Birth 55プロジェクトへようこそ。</p>
    <p>この記事では、<strong>「{data["name"]}」</strong>に関する最新の知見と、私自身の体験に基づいた実践的なステップを紹介します。</p>
    <p>加齢に伴う体の変化や環境の変化に戸惑うこともありますが、正しい知識と少しの工夫で、毎日はもっと楽しく、豊かになります。</p>

    <h2>1. 今回のポイント</h2>
    <p>{title}において最も重要なのは、「継続」と「分析」の両立です。ただ闇雲に取り組むのではなく、自分に合った最適な方法を見つけ出すプロセスそのものを楽しむことが、成功への近道です。</p>

    <div class="data-notice">
        <strong>💡 Check Point:</strong><br>
        このトピックに関する詳細な分析データは、ヘッダーの「View Data」から確認することができます。日々の変化を可視化することで、モチベーションの維持に役立ちます。
    </div>

    <h2>2. 次のアクション</h2>
    <p>まずは、明日からできる小さな一歩を決めることから始めましょう。大きな変革も、最初はほんの些細な習慣の積み重ねから始まります。</p>
    
    <p>詳しい実践レポートは順次更新予定です。一緒に健康で実りある50代を追求していきましょう！</p>
</div>
"""
                parts[2] = new_body + sub_parts[1] + "".join(sub_parts[2:])
                new_c = "".join(parts)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_c)

    # Update all links in all files
    all_files = [f for f in os.listdir(site_dir) if f.endswith(".html")]
    for fname in all_files:
        fpath = os.path.join(site_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        def href_replacer(match):
            card_html = match.group(0)
            t_match = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card_html, re.DOTALL)
            if t_match:
                title = t_match.group(1).strip()
                if title in article_db:
                    correct_href = article_db[title]["filename"]
                    return re.sub(r'href="[^"]*\.html"', f'href="{correct_href}"', card_html)
            return card_html

        new_content = re.sub(r'<article class="article-card".*?</article>', href_replacer, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
    
    print(f"  Thoroughly fixed {len(article_db)} articles in {os.path.basename(site_dir)}")

def main():
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            fix_links_globally_refined(site_path)

if __name__ == "__main__":
    main()
