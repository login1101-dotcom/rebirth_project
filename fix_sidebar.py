import os

DIR = "/Users/jono/Desktop/rebirth_project/children/rebirth_child_typing"
files = [f for f in os.listdir(DIR) if f.startswith("post_") and f.endswith(".html")]

print(f"Checking {len(files)} files for sidebar.js script tag...")

for f in files:
    path = os.path.join(DIR, f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # sidebar.jsが含まれているかチェック
    if '<script src="sidebar.js"></script>' not in content:
        # 含まれていない場合、</body>の直前に挿入
        if '</body>' in content:
            content = content.replace('</body>', '<script src="sidebar.js"></script>\n</body>')
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Recoved sidebar.js in: {f}")
        else:
            print(f"Skipped {f} (No </body> tag found)")
    else:
        print(f"OK: {f}")
