
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def remove_hero_image_all(dir_path):
    article_path = os.path.join(dir_path, "article.html")
    if not os.path.exists(article_path):
        return

    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find <div class="article-thumb ..."> ... </div>
    # We want to remove this block.
    pattern = re.compile(r'<div class="article-thumb[^"]*"[^>]*>.*?</div>', re.DOTALL)
    
    if pattern.search(content):
        # Substitute with empty string
        new_content = pattern.sub('', content)
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed hero image from: {os.path.basename(dir_path)}")
    else:
        # Check if it was already removed or didn't exist
        print(f"No hero image found in: {os.path.basename(dir_path)} (Clean)")

def main():
    if not os.path.exists(base_dir):
        print("Base directory not found.")
        return

    for item in os.listdir(base_dir):
        full_path = os.path.join(base_dir, item)
        if os.path.isdir(full_path):
            remove_hero_image_all(full_path)

if __name__ == "__main__":
    main()
