
import os
import re

target_files = [
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_health/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_english/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_youtube/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_manga/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_reading/article.html"
]

def remove_hero_image_div(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the div with class "article-thumb" inside the header or just globally in the file (but restricted to single post context usually)
    # The div looks like: <div class="article-thumb ...> ... </div>
    # It might span multiple lines.
    
    # We look for <div class="article-thumb [^>]*>.*?</div>
    # Using dotall to match across lines.
    
    pattern = re.compile(r'<div class="article-thumb[^"]*"[^>]*>.*?</div>', re.DOTALL)
    
    if pattern.search(content):
        # Specific fix: In article.html, this is usually strictly for the hero image.
        # Be careful not to delete article-thumb in article-card if I were editing index.html, 
        # but here we target article.html which is the single post.
        
        # However, checking the file content provided previously, the class is indeed 'article-thumb bg-...'
        new_content = pattern.sub('', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed hero image from: {os.path.basename(os.path.dirname(filepath))}")
    else:
        print(f"No hero image div found in: {os.path.basename(os.path.dirname(filepath))}")

for p in target_files:
    remove_hero_image_div(p)
