
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def fix_links_globally(site_dir):
    # 1. Collect all unique articles (by title) and their info
    # We scan all .html files in the site to find everything that looks like an article-card
    article_db = {} # title -> { slug, category_name, excerpt, href, original_file_found_in }

    # Find all HTML files
    html_files = [f for f in os.listdir(site_dir) if f.endswith(".html")]
    
    # We'll use a sequential numbering for new files
    file_counter = 1
    
    # Existing article files to avoid overwriting or reusing incorrectly
    # We use 'article.html' as the primary template.
    
    # First pass: find all unique titles and assign them a permanent unique filename
    for fname in html_files:
        path = os.path.join(site_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex to find cards
        cards = re.findall(r'<article class="article-card".*?</article>', content, re.DOTALL)
        for card in cards:
            t_m = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card, re.DOTALL)
            if not t_m: continue
            title = t_m.group(1).strip()
            
            # Category info
            c_m = re.search(r'class="cat text-([a-z0-9_-]+)".*?>\s*(.*?)\s*</a>', card, re.DOTALL)
            cat_slug = c_m.group(1).strip() if c_m else "others"
            cat_name = c_m.group(2).strip() if c_m else "Others"
            
            # Excerpt
            e_m = re.search(r'<p class="article-excerpt">\s*(.*?)\s*</p>', card, re.DOTALL)
            excerpt = e_m.group(1).strip() if e_m else ""
            
            if title not in article_db:
                # Assign a unique filename
                # If it's the very first article we ever saw and it matched the original article.html content? 
                # No, better just assign sequential like article_1.html, article_2.html etc.
                # or use a slugified title.
                
                # Let's keep one as 'article.html' (usually the first one in index.html)
                clean_title = re.sub(r'[^a-zA-Z0-9]', '_', title)[:20]
                target_filename = f"post_{file_counter}.html"
                file_counter += 1
                
                # Special: try to keep original names if they were already unique? No, cleaner to redo.
                
                article_db[title] = {
                    "filename": target_filename,
                    "slug": cat_slug,
                    "name": cat_name,
                    "excerpt": excerpt
                }

    # 2. Generate the missing HTML files based on a template (article.html)
    template_path = os.path.join(site_dir, "article.html")
    if not os.path.exists(template_path):
        # Find any article_*.html to use as template if article.html is missing
        candidates = [f for f in html_files if f.startswith("article")]
        if candidates: template_path = os.path.join(site_dir, candidates[0])
        else: return # can't fix without template

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    for title, data in article_db.items():
        fpath = os.path.join(site_dir, data["filename"])
        
        # Build the new content
        new_c = template_content
        
        # Update title tag and h1
        new_c = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', new_c)
        new_c = re.sub(r'<h1>\s*(.*?)\s*</h1>', f'<h1>{title}</h1>', new_c, flags=re.DOTALL)
        
        # Update Header Background class and Category text
        new_c = re.sub(r'class="bg-styled bg-[a-z0-9_-]+"', f'class="bg-styled bg-{data["slug"]}"', new_c)
        new_c = re.sub(r'class="cat text-[a-z0-9_-]+"(.*?>).*?</a>', 
                       f'class="cat text-{data["slug"]}"\\1{data["name"]}</a>', new_c)
        
        # Update excerpt/body placeholder
        # Most of our articles have a <p> lead or similar.
        # Let's put the excerpt as the first paragraph.
        parts = re.split(r'(<div class="post-content">)', new_c)
        if len(parts) > 2:
            # Inject excerpt as bold lead
            intro = f'\n<p style="font-weight:bold; margin-bottom:2rem;">{data["excerpt"]}</p>\n'
            # Remove anything that looked like the old intro (optional, but cleaner)
            parts[2] = intro + "<p>この記事は現在準備中です。50代の健康と挑戦のための具体的なノウハウを執筆しています。</p>" + re.sub(r'<p style="font-weight:bold;.*?/p>', '', parts[2], flags=re.DOTALL)
            new_c = "".join(parts)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_c)

    # 3. Last Step: Update ALL links in ALL files to point to correct unique filenames
    for fname in html_files:
        fpath = os.path.join(site_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # We need to find each card and swap its href
        def href_replacer(match):
            card_html = match.group(0)
            t_match = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card_html, re.DOTALL)
            if t_match:
                title = t_match.group(1).strip()
                if title in article_db:
                    correct_href = article_db[title]["filename"]
                    # Replace href="..."
                    return re.sub(r'href="[^"]*\.html"', f'href="{correct_href}"', card_html)
            return card_html

        new_content = re.sub(r'<article class="article-card".*?</article>', href_replacer, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
    
    print(f"  Fixed links for {len(article_db)} unique articles in {os.path.basename(site_dir)}")

def main():
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            fix_links_globally(site_path)

if __name__ == "__main__":
    main()
