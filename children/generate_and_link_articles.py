
import os
import re
from bs4 import BeautifulSoup

base_dir = "/Users/jono/Desktop/rebirth_project/children"

# Mapping of generic 'article.html' to specific content for each site
# We will parse index.html to find article cards.
# For each card, we will generate a unique filename based on its title or category.
# Then we create that file from the 'article.html' template of that site.
# Finally we update the link in index.html (and category pages ideally, but starting with index).

def sanitize_filename(text):
    # Create valid filename from title or unique identifier
    return re.sub(r'[^a-zA-Z0-9]', '_', text).lower()[:20]

def fix_site_links(current_dir):
    index_path = os.path.join(current_dir, "index.html")
    article_template_path = os.path.join(current_dir, "article.html")
    
    if not os.path.exists(index_path) or not os.path.exists(article_template_path):
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Read template content
    with open(article_template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Find all article cards
    cards = soup.find_all('article', class_='article-card')
    
    replacements = [] # To store (old_link, new_link, new_file_info)

    print(f"Processing {os.path.basename(current_dir)}...")

    for i, card in enumerate(cards):
        # Extract info
        title_tag = card.find(class_='article-title')
        if not title_tag: continue
        title = title_tag.get_text(strip=True)
        
        excerpt_tag = card.find(class_='article-excerpt')
        excerpt = excerpt_tag.get_text(strip=True) if excerpt_tag else ""
        
        meta_tag = card.find(class_='article-meta')
        date = meta_tag.find(class_='date').get_text(strip=True) if meta_tag and meta_tag.find(class_='date') else "2025.01.01"
        
        cat_link = meta_tag.find('a', class_='cat') if meta_tag else None
        cat_name = cat_link.get_text(strip=True) if cat_link else "General"
        cat_class = " ".join(cat_link.get('class')) if cat_link else ""
        
        # Extract specific category slug for bg color from class (e.g., text-short -> bg-short)
        # Assuming class contains text-something
        bg_class_name = "bg-primary" # default
        if 'text-' in cat_class:
            for c in cat_class.split():
                if c.startswith('text-'):
                    bg_class_name = c.replace('text-', 'bg-')
                    break
        
        # Determine new filename
        # If it's the first card, maybe keep article.html? 
        # But user wants specific links. Let's make unique files for ALL, or keep one.
        # Strategy: If the link is currently generic 'article.html', meaningful-name it.
        
        link_tag = card.find('a')
        current_href = link_tag.get('href')
        
        # Generate new filename based on index or title unique hash
        # We start from article_1.html, article_2.html etc for simplicity and reliability
        # Or better: article_works.html etc if we can detect category.
        
        # Let's use simple numbering or keyword extraction to avoid collision
        new_filename = f"article_{i+1}.html"
        
        # However, if one of them corresponds to the CURRENT article.html content, we might want to keep it or copy it.
        # Since we don't know which one matches the current article.html text, we will overwrite ALL with new generated pages based on the card info.
        # This ensures the "Click -> See Title matches" behavior is consistent.
        # BUT this implies losing specific hardcoded content in article.html if we overwrite it with template data.
        # The user said "Properly make the page". 
        # The current article.html usually has GOOD content for ONE card.
        # We should check if the title matches.
        
        # Checking existing article.html title
        template_soup = BeautifulSoup(template_content, 'html.parser')
        template_h1 = template_soup.find('h1')
        existing_title = template_h1.get_text(strip=True) if template_h1 else ""
        
        is_existing_article = (title in existing_title or existing_title in title)
        
        if is_existing_article:
            new_filename = "article.html" # Keep existing
            # No generation needed, just ensure link is correct
        else:
            # Create new file
            new_file_path = os.path.join(current_dir, new_filename)
            
            # Modify content
            new_soup = BeautifulSoup(template_content, 'html.parser')
            
            # Update Title
            h1 = new_soup.find('h1')
            if h1: h1.string = title
            
            # Update Document Title
            if new_soup.title:
                site_name = new_soup.title.string.split('|')[-1].strip() if '|' in new_soup.title.string else "Re:Birth"
                new_soup.title.string = f"{title} | {site_name}"
            
            # Update Meta Date/Cat
            header = new_soup.find('main').find('header')
            if header:
                # Update Header BG class
                # Remove existing bg-styled and bg-* classes
                # header['class'] = ['bg-styled', bg_class_name] # This might wipe other classes
                # Better: clean existing bg classes
                existing_classes = header.get('class', [])
                clean_classes = [c for c in existing_classes if not c.startswith('bg-')]
                clean_classes.append('bg-styled')
                clean_classes.append(bg_class_name)
                header['class'] = clean_classes

                # Update Meta
                meta_div = header.find(class_='article-meta')
                if meta_div:
                    # preserve structure if possible
                    # <span class="date">...</span> • <span class="cat">...</span> or similar
                     meta_div.string = "" # clear
                     date_span = new_soup.new_tag("span", attrs={"class": "date"})
                     date_span.string = date
                     meta_div.append(date_span)
                     meta_div.append(" • ")
                     cat_span = new_soup.new_tag("span", attrs={"class": "cat", "style": f"color: var(--color-{bg_class_name.replace('bg-','')}); font-weight:bold;"})
                     cat_span.string = cat_name
                     meta_div.append(cat_span)

            # Update Body Content
            post_content = new_soup.find(class_='post-content')
            if post_content:
                post_content.clear()
                # Add excerpt as lead
                p_lead = new_soup.new_tag("p", attrs={"style": "font-weight:bold; margin-bottom:2rem;"})
                p_lead.string = excerpt
                post_content.append(p_lead)
                
                # Add dummy headers and text
                h2_1 = new_soup.new_tag("h2")
                h2_1.string = "1. 詳細な分析"
                post_content.append(h2_1)
                p_1 = new_soup.new_tag("p")
                p_1.string = "ここに詳細な記事本文が入ります。現在の表示はプレースホルダーですが、カードのタイトル「" + title + "」に基づいた内容が展開されます。"
                post_content.append(p_1)
                
                heading_2 = new_soup.new_tag("h2")
                heading_2.string = "2. まとめ"
                post_content.append(heading_2)
                p_2 = new_soup.new_tag("p")
                p_2.string = "この記事のまとめです。継続的な取り組みが結果を生みます。"
                post_content.append(p_2)

            # Save File
            with open(new_file_path, 'w', encoding='utf-8') as f_out:
                f_out.write(str(new_soup))
        
        replacements.append((current_href, new_filename))

    # Update index.html links
    # We must be careful not to replace generic strings globally without context, 
    # but since we are iterating cards, we should theoretically find the specific <a> tag and update it.
    # However, standard string replacement on the file is safer for preservation than soup.prettify() which might mangle formatting.
    
    # Actually, let's use the soup we already parsed to update the hrefs, then save index.html?
    # No, soup often messes up indentation.
    # We will use regex or careful string replacement if possible, OR just update the 'cards' object and define how many cards we had.
    
    # Re-reading index.html text to modify
    with open(index_path, 'r', encoding='utf-8') as f:
        file_text = f.read()

    # This is tricky because multiple cards might have href="article.html"
    # We need to replace them one by one in order.
    
    # We can split the content by 'article-card', then reconstruct.
    # Or simplified: First match of article-card link gets replacement[0], second gets replacement[1]...
    
    parts = re.split(r'(<article class="article-card".*?</article>)', file_text, flags=re.DOTALL)
    card_idx = 0
    new_file_text = ""
    
    for part in parts:
        if '<article class="article-card"' in part:
            if card_idx < len(replacements):
                original_href, new_href = replacements[card_idx]
                # Regex replace only the href inside THIS specific part
                # href="article.html" -> href="new_href"
                # Be careful if href is single quotes or formatted differently
                part = re.sub(r'href="[^"]*article\.html"', f'href="{new_href}"', part, count=1)
                card_idx += 1
        new_file_text += part
        
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_file_text)

    # Need to also update Category pages (category_*.html)
    # This is harder because we don't know which card is in which category file from here.
    # But we can try to apply the same logic: scan all category files, if we find a card with Title X, link it to the file we created for Title X.
    
    # Build a title -> filename map
    title_to_file = {}
    for i, card in enumerate(cards):
        title = card.find(class_='article-title').get_text(strip=True)
        # Re-derive filename logic to match
        # (We relied on index.html order: article_1.html, article_2.html...)
        # This is brittle if category pages have different order.
        # But we determined filenames: article_1, article_2...
        # Let's map Title -> article_{i+1}.html
        
        # Check existing logic
        template_soup = BeautifulSoup(template_content, 'html.parser')
        template_h1 = template_soup.find('h1')
        existing_title = template_h1.get_text(strip=True) if template_h1 else ""
        is_existing = (title in existing_title or existing_title in title)
        
        fname = "article.html" if is_existing else f"article_{i+1}.html"
        title_to_file[title] = fname

    # Update other HTML files in directory
    for fname in os.listdir(current_dir):
        if fname.startswith("category_") and fname.endswith(".html"):
            cat_path = os.path.join(current_dir, fname)
            with open(cat_path, 'r', encoding='utf-8') as f:
                c_content = f.read()
            
            # For each title in our map, see if it exists in this file and replace the link
            # This is safer.
            for title_key, target_file in title_to_file.items():
                # Look for a card containing this title
                # We need to target the href BEFORE or AROUND the title.
                # Regex: <a href="(old)" ...> ...Title... </a>
                # Because the card wraps the link usually.
                
                # Construct regex that matches the article card containing the title
                # <a href="article.html"> ... <h3 class="article-title">Exact Title</h3>
                
                # Escape title for regex
                escaped_title = re.escape(title_key)
                
                # Regex to find the href associated with this title
                # The href usually comes before the title in the DOM structure: <a href="..."> ... <h3>Title</h3> ... </a>
                # Note: 'article.html' is hardcoded target to replace
                
                pattern = re.compile(r'(href=")(article\.html)("[^>]*>.*?<h3 class="article-title">\s*' + escaped_title + r'\s*</h3>)', re.DOTALL)
                
                if pattern.search(c_content):
                    c_content = pattern.sub(r'\1' + target_file + r'\3', c_content)
            
            with open(cat_path, 'w', encoding='utf-8') as f:
                f.write(c_content)

def main():
    if not os.path.exists(base_dir):
        return
    for item in os.listdir(base_dir):
        full_path = os.path.join(base_dir, item)
        if os.path.isdir(full_path):
            fix_site_links(full_path)

if __name__ == "__main__":
    main()
