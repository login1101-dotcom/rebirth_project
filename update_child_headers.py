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

# Regex to match the small tag containing "by Re:Birth 55"
# Allowing for flexible attributes and whitespace
pattern = re.compile(r'<small\s+[^>]*>by Re:Birth 55</small>', re.IGNORECASE)

for dirname, goal_text in directories.items():
    dir_path = os.path.join(base_path, dirname)
    if not os.path.exists(dir_path):
        print(f"Directory not found: {dir_path}")
        continue

    print(f"Processing directory: {dirname} -> {goal_text}")

    for filename in os.listdir(dir_path):
        if filename.endswith('.html'):
            file_path = os.path.join(dir_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replacement span
            # Using inline style to match the requested look (gray, smallish but readable)
            # The previous small tag had 0.8rem. 
            # I'll use similar style but maybe slightly adjusted as per user request "ichibun irete"
            replacement = f'<span style="font-size: 0.8rem; color: #64748b; margin-left: 10px; font-weight: normal;">{goal_text}</span>'
            
            new_content = pattern.sub(replacement, content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  Updated: {filename}")
            else:
                print(f"  No match found in: {filename}")
