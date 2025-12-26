import os
import re

TARGET_DIR = "/Users/jono/Desktop/rebirth_project/children/rebirth_child_typing"
FILES = [f for f in os.listdir(TARGET_DIR) if f.startswith("post_") and f.endswith(".html")]

FILES.sort(key=lambda x: int(re.search(r'post_(\d+)', x).group(1)))

print(f"Target files: {FILES}")

# 1. カテゴリマッピング
file_categories = {}
category_groups = {}

breadcrumb_regex = re.compile(r'<div class="breadcrumb"[^>]*>(.*?)</div>', re.DOTALL | re.IGNORECASE)
cat_link_regex = re.compile(r'category_([a-z]+)\.html')

for filename in FILES:
    filepath = os.path.join(TARGET_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    category = "uncategorized"
    
    # パンくずリスト部分を抽出
    match = breadcrumb_regex.search(content)
    if match:
        breadcrumb_content = match.group(1)
        
        # 特例判定: Typing Master Neo が含まれていたら独立カテゴリにする
        if "Typing Master Neo" in breadcrumb_content:
            category = "neo"
        else:
            # 通常判定: リンク先で判断
            cat_match = cat_link_regex.search(breadcrumb_content)
            if cat_match:
                category = cat_match.group(1)
    
    file_categories[filename] = category
    
    if category not in category_groups:
        category_groups[category] = []
    category_groups[category].append(filename)

print("Category Grouping Result (Refined):")
for cat, fs in category_groups.items():
    print(f"  {cat.upper()}: {fs}")


# 2. リンク生成
for i, filename in enumerate(FILES):
    filepath = os.path.join(TARGET_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    my_cat = file_categories[filename]
    my_group = category_groups.get(my_cat, [])
    
    try:
        idx = my_group.index(filename)
    except ValueError:
        idx = -1
    
    # 色決定
    nav_color = "var(--primary)"
    if my_cat == "analysis":
        nav_color = "var(--color-analysis)"
    elif my_cat == "daily":
        nav_color = "var(--color-daily)"
    elif my_cat == "tools":
        nav_color = "var(--color-tools)"
    elif my_cat == "neo":
        nav_color = "#10b981" # Neo Green (from header button)

    # --- Prev ---
    if idx > 0:
        prev_link = my_group[idx - 1]
        prev_html = f'<a href="{prev_link}" style="text-decoration: none; color: {nav_color};">&laquo; 前の記事</a>'
    else:
        prev_html = f'<span style="color: #ccc;">&laquo; 前の記事</span>'

    # --- Next ---
    if idx != -1 and idx < len(my_group) - 1:
        next_link = my_group[idx + 1]
        next_html = f'<a href="{next_link}" style="text-decoration: none; color: {nav_color};">次の記事 &raquo;</a>'
    else:
        next_html = f'<span style="color: #ccc;">次の記事 &raquo;</span>'


    # HTML Blocks
    nav_block = f'''
                    <div class="post-navigation" style="display: flex; justify-content: space-between; margin-bottom: 1rem; font-size: 0.9rem; font-weight: bold;">
                        {prev_html}
                        {next_html}
                    </div>'''
    
    nav_block_bottom = f'''
                    <div class="post-navigation" style="display: flex; justify-content: space-between; margin-top: 3rem; margin-bottom: 1rem; font-size: 0.9rem; font-weight: bold;">
                        {prev_html}
                        {next_html}
                    </div>'''

    # Clean up
    content = re.sub(r'<div class="post-navigation".*?</div>', '', content, flags=re.DOTALL)

    # Insert Top
    breadcrumb_pattern = r'(<div class="breadcrumb"[^>]*>.*?</div>)'
    if re.search(breadcrumb_pattern, content, re.DOTALL):
        content = re.sub(breadcrumb_pattern, r'\1' + nav_block, content, count=1, flags=re.DOTALL)
    
    # Insert Bottom
    bottom_pattern = r'(\s*</div>\s*</article>)'
    if re.search(bottom_pattern, content, re.DOTALL):
        content = re.sub(bottom_pattern, nav_block_bottom + r'\1', content, count=1, flags=re.DOTALL)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Updated {filename} -> Category: {my_cat}")
