
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def extract_title_and_excerpt(card_html):
    # Extract Title using regex: <h3 class="article-title">...</h3>
    t_match = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card_html, re.DOTALL)
    title = t_match.group(1) if t_match else "Untitled"
    
    # Extract Excerpt: <p class="article-excerpt">...</p>
    e_match = re.search(r'<p class="article-excerpt">\s*(.*?)\s*</p>', card_html, re.DOTALL)
    excerpt = e_match.group(1) if e_match else ""
    return title.strip(), excerpt.strip()

def get_base_article_title(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    m = re.search(r'<h1>\s*(.*?)\s*</h1>', c, re.DOTALL)
    return m.group(1).strip() if m else ""

def generate_articles_no_bs4(current_dir):
    index_path = os.path.join(current_dir, "index.html")
    article_template_path = os.path.join(current_dir, "article.html")
    
    if not os.path.exists(index_path) or not os.path.exists(article_template_path):
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        file_text = f.read()
        
    # Get existing template title to avoid overwriting the "real" article
    existing_title = get_base_article_title(article_template_path)
    
    # Find all cards
    # Pattern to capture the whole card content
    card_pattern = re.compile(r'(<article class="article-card".*?</article>)', re.DOTALL)
    cards = card_pattern.findall(file_text)
    
    replacements = [] # list of (title, new_filename)
    
    print(f"Processing {os.path.basename(current_dir)} with {len(cards)} cards...")

    for i, card_html in enumerate(cards):
        title, excerpt = extract_title_and_excerpt(card_html)
        
        # Determine filename
        # If title matches existing article.html title, keep it
        if title in existing_title or existing_title in title:
            new_filename = "article.html"
            print(f"  - Card '{title}' -> Kept as article.html")
        else:
            new_filename = f"article_{i+1}.html"
            print(f"  - Card '{title}' -> Created {new_filename}")
            
            # Create the file
            with open(article_template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. Replace Title in H1
            # <h1>...</h1>
            content = re.sub(r'<h1>\s*.*?\s*</h1>', f'<h1>{title}</h1>', content, flags=re.DOTALL)
            
            # 2. Replace Title tag
            content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content, flags=re.DOTALL)
            
            # 3. Replace Excerpt/Content
            # Find <div class="post-content"> ... </div>
            # We will replace the inner content of post-content
            # This is tricky with regex due to nested divs, but usually post-content structure is simple enough in our template
            # Let's try to match <div class="post-content"> until the closing </div> of that div.
            # Assuming post-content closes before </article>
            
            # Harder without parser. Let's just blindly replace the first <p> paragraph after div post-content?
            # Or just replace the whole body text we know exists.
            
            # Simplest correct way: Replace known string from template if we can identifying it.. 
            # but template content varies.
            
            # Let's just append the excerpt at the start of post-content
            content = content.replace('<div class="post-content">', 
                                      f'<div class="post-content"><p style="font-weight:bold; margin-bottom:2rem;">{excerpt}</p>')
            
            # 4. Colorize header based on card category?
            # Card has <a href="..." class="cat text-xxx">
            # We want to put bg-xxx on the new article header.
            # Find class in card
            cat_match = re.search(r'class="cat text-([a-z]+)"', card_html)
            if cat_match:
                cat_slug = cat_match.group(1)
                # Apply to header: class="bg-styled bg-xxx"
                # Find <header class="bg-styled ..."> or just <header ...>
                # Using our previous standardized output
                if 'class="bg-styled' in content:
                     # Replace existing bg class
                     content = re.sub(r'class="bg-styled bg-[a-z]+"', f'class="bg-styled bg-{cat_slug}"', content)
                else:
                    # Inject
                     content = content.replace('<header>', f'<header class="bg-styled bg-{cat_slug}">')

            with open(os.path.join(current_dir, new_filename), 'w', encoding='utf-8') as f_out:
                f_out.write(content)

        replacements.append((title, new_filename))

    # Now update links in Index and Category pages
    # We map Title -> Filename
    # We iterate all HTML files, find the card with that Title, and update its HREF
    
    # Files to update: index.html and category_*.html
    files_to_update = [f for f in os.listdir(current_dir) if f == 'index.html' or (f.startswith('category_') and f.endswith('.html'))]
    
    for fname in files_to_update:
        fpath = os.path.join(current_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            f_content = f.read()
            
        for title, new_file in replacements:
            if new_file == "article.html": continue # No change needed
            
            # Regex: Find <a href="article.html"> ... <h3...>Title</h3> ... </a>
            # We are modifying the HREF.
            # Pattern matches the Link tag opening, content until title, title, rest.
            
            # We assume structure: <a href="article.html"> ...Title... </a>
            # We escape the title.
            
            esc_title = re.escape(title)
            
            # Pattern: href="article.html" (followed eventually by title)
            # This is hard to do safely in one regex if determining WHICH href to change.
            # But the card structure is consistent.
            
            # Let's split by <article class="article-card"> to isolate context
            segments = re.split(r'(<article class="article-card".*?</article>)', f_content, flags=re.DOTALL)
            new_f_content = ""
            for seg in segments:
                if 'article-card' in seg and f"<h3 class=\"article-title\">{title}</h3>" in seg:
                     # This is the card for this title. Replace href="article.html"
                     # Only match article.html to avoid breaking other links
                     seg = seg.replace('href="article.html"', f'href="{new_file}"')
                     # Also handle href="article.html" inside article-meta if exists
                elif 'article-card' in seg and f"class=\"article-title\">{title}<" in seg: 
                     # Loose match for title spacing?
                     seg = seg.replace('href="article.html"', f'href="{new_file}"')
                
                new_f_content += seg
            f_content = new_f_content

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(f_content)

def main():
    if not os.path.exists(base_dir):
        return
    for item in os.listdir(base_dir):
        full_path = os.path.join(base_dir, item)
        if os.path.isdir(full_path):
            generate_articles_no_bs4(full_path)

if __name__ == "__main__":
    main()
