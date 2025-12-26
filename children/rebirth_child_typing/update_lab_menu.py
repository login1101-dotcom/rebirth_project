import os
import re

# Target Directory: Lab (rebirth_child_typing)
LAB_DIRECTORY = "/Users/jono/Desktop/rebirth_project/children/rebirth_child_typing"

# New Menu HTML snippet (simplified for replacement)
# We need to find the existing menu structure and replace items.
# Usually it looks like:
# <a href="...">ホーム</a>
# <a href="...">練習</a>
# ...

def update_lab_menu():
    count = 0
    # Files to update
    for filename in os.listdir(LAB_DIRECTORY):
        if not filename.endswith(".html"):
            continue
            
        filepath = os.path.join(LAB_DIRECTORY, filename)
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            continue
            
        original = content
        
        # 1. Remove "分析" link
        # Regex: <a href="[^"]*analysis[^"]*".*?</a>\s*
        content = re.sub(r'<a href="[^"]*analysis[^"]*"[^>]*>分析</a>\s*', '', content, flags=re.IGNORECASE)
        content = re.sub(r'<a href="[^"]*category_analysis[^"]*"[^>]*>分析</a>\s*', '', content, flags=re.IGNORECASE)

        # 2. Rename "使用サイト・ツール" to "Typing Master Neo"
        # Link remains category_tools.html
        content = content.replace("使用サイト・ツール", "Typing Master Neo")

        # 3. Rename "データ表示" to "NEO" button style and link to Neo
        # Old: <a href="view_data.html" ...>データ表示</a>
        # New: <a href="http://localhost:8000" target="_blank" class="nav-btn-neo">NEO</a>
        # We'll use a class/style to make it look like a button if possible, or just text for now.
        
        # Find the link for view_data.html
        if "view_data.html" in content:
            # We replace the whole tag
            # Simple string replace might fail if attributes vary
            # Regex replacement
            content = re.sub(
                r'<a href="[^"]*view_data\.html"[^>]*>データ表示</a>', 
                '<a href="http://localhost:8000" target="_blank" style="background:#00796b; color:white; padding:5px 10px; border-radius:4px; font-weight:bold;">NEO</a>', 
                content
            )

        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
            
    print(f"Updated menu in {count} files in Lab.")

if __name__ == "__main__":
    update_lab_menu()
