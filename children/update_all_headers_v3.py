
import os
import re

# Configuration
base_dir = "/Users/jono/Desktop/rebirth_project/children"

# Target style
new_style = 'font-size: 1.0rem; color: #334155; margin-left: 15px; font-weight: 600; letter-spacing: 0.05em;'

# Map of directory names to new header text
site_texts = {
    'rebirth_child_english': '世界と繋がる新しい力',
    'rebirth_child_health': '自分を愛する最初の力',
    'rebirth_child_novel': '物語を心から世界へ',
    'rebirth_child_manga': '表現を広げる自由の翼',
    'rebirth_child_reading': '時空を超えて会いたい人たち',
    'rebirth_child_youtube': 'もっといい世界へ'
}

def update_file(filepath, new_text):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the site-brand link and its inner span that contains the slogan
    # It looks for the closing </a> of .site-brand and the span immediately preceding it
    # We want to replace the entire <span ...>...</span> block
    
    # Pattern explanation:
    # 1. match class="site-brand"> or similar opening
    # 2. consume until the last <span
    # 3. capture the span content until </span>
    # 4. followed by </a>
    
    # However, a simpler approach is to target the specific span if we are sure of the structure.
    # Structure: ...Site Name <span style="...">Old Text</span></a>
    
    pattern = re.compile(r'(<a[^>]*class="site-brand"[^>]*>.*?)(<span style="[^"]*">.*?</span>)(\s*</a>)', re.DOTALL)
    
    def replacement(match):
        prefix = match.group(1)
        suffix = match.group(3)
        # Construct the new span
        new_span = f'<span style="{new_style}">{new_text}</span>'
        return f'{prefix}{new_span}{suffix}'

    new_content, count = pattern.subn(replacement, content)
    
    if count > 0:
        print(f"Updated: {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        print(f"No match found in: {filepath}")

def main():
    for dirname, text in site_texts.items():
        dirpath = os.path.join(base_dir, dirname)
        if not os.path.exists(dirpath):
            print(f"Directory not found: {dirpath}")
            continue
            
        print(f"Processing {dirname} with text: {text}")
        
        for root, _, files in os.walk(dirpath):
            for file in files:
                if file.endswith('.html'):
                    filepath = os.path.join(root, file)
                    update_file(filepath, text)

if __name__ == "__main__":
    main()
