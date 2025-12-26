import os
import re

directories = {
    'rebirth_child_typing': 'ブラインドタッチを習得する',
    'rebirth_child_health': '見た目のいい健康な体を手にいれる',
    'rebirth_child_english': '使える英語を身につける',
    'rebirth_child_novel': '小説家やエッセイストになる',
    'rebirth_child_manga': '漫画家になる',
    'rebirth_child_youtube': '動画作家として生活できる収益を得る',
    'rebirth_child_reading': '難しい名著を理解する'
}

base_path = '/Users/jono/Desktop/rebirth_project/children'

# Regex for site-brand link content
# Matches <a href="index.html" class="site-brand">(CONTENT)</a>
brand_pattern = re.compile(r'(<a\s+href="index\.html"\s+class="site-brand"[^>]*>)(.*?)(</a>)', re.DOTALL | re.IGNORECASE)

# Regex to find existing small tag with "by Re:Birth 55"
small_tag_pattern = re.compile(r'<small\s+[^>]*>\s*by Re:Birth 55\s*</small>', re.IGNORECASE)

for dirname, goal_text in directories.items():
    dir_path = os.path.join(base_path, dirname)
    if not os.path.exists(dir_path):
        continue

    print(f"Processing directory: {dirname} -> {goal_text}")

    for filename in os.listdir(dir_path):
        if filename.endswith('.html'):
            file_path = os.path.join(dir_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            def replace_brand(match):
                start_tag = match.group(1)
                inner_content = match.group(2)
                end_tag = match.group(3)
                
                # New span to insert
                new_span = f'<span style="font-size: 0.8rem; color: #64748b; margin-left: 10px; font-weight: normal;">{goal_text}</span>'
                
                # Check if small tag exists
                if small_tag_pattern.search(inner_content):
                    # Replace small tag with new span
                    new_inner_content = small_tag_pattern.sub(new_span, inner_content)
                else:
                    # Append new span
                    # Assuming inner_content ends with text or span
                    new_inner_content = inner_content + new_span
                    
                return f"{start_tag}{new_inner_content}{end_tag}"

            new_content = brand_pattern.sub(replace_brand, content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  Updated: {filename}")
            else:
                # If no update, maybe brand pattern didn't match?
                # Check if it's already updated (contains goal_text)
                if goal_text in content:
                    print(f"  Already updated/skipped: {filename}")
                else:
                    print(f"  Brand pattern not found: {filename}")
