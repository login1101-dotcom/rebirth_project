import os

# 対象となる子サイトのディレクトリ名
child_sites = [
    "rebirth_child_typing",
    "rebirth_child_health",
    "rebirth_child_english",
    "rebirth_child_novel",
    "rebirth_child_manga",
    "rebirth_child_youtube",
    "rebirth_child_reading"
]

base_dir = "/Users/jono/Desktop/rebirth_project/children"
source_js_path = os.path.join(base_dir, "universal_counter.js")

# 1. read universal_counter.js
with open(source_js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# HTML挿入用スニペット
# フッターの著作権表示の後ろなどに追加する
# ターゲット: </footer> の直前、あるいは Copyrightのpタグの中
COUNTER_HTML_SNIPPET = '<span id="visit-counter" style="margin-left:10px; font-size:0.8rem; color:#888;">訪問数：--</span>'
SCRIPT_TAG = '<script src="counter.js"></script>'

for site in child_sites:
    site_dir = os.path.join(base_dir, site)
    if not os.path.exists(site_dir):
        print(f"Skipping {site} (not found)")
        continue
    
    print(f"Processing {site}...")

    # 2. copy counter.js to each site root
    dest_js_path = os.path.join(site_dir, "counter.js")
    with open(dest_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    
    # 3. Process all HTML files
    for root, dirs, files in os.walk(site_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 既にcounter.jsがあるかチェック
                if '<script src="counter.js"></script>' in content:
                    print(f"  Skipping {file} (already has counter script)")
                    continue
                
                # Modify HTML
                # Strategy:
                # 1. Insert SCRIPT_TAG before </body>
                # 2. Insert COUNTER_HTML_SNIPPET inside the copyright <p> tag if possible, or before </footer>
                
                new_content = content
                
                # 1. Add Script
                if "</body>" in new_content:
                    new_content = new_content.replace("</body>", f"{SCRIPT_TAG}\n</body>")
                
                # 2. Add Counter Span
                # Search for copyright paragraph pattern
                # Pattern: <p>&copy; ... </p> or <p class="copyright">... </p>
                # Simple approach: Find </footer> and prepend if not found in p
                
                inserted_span = False
                
                # Try to insert into the last paragraph of footer (copyright usually)
                if "</p>" in new_content:
                     # Find the last closing p tag before footer close if possible, but regex is risky.
                     # Let's simple-replace the closing p tag inside footer.
                     # But we don't know where footer is exactly with simple string replace.
                     
                     # Look for specific copyright patterns used in this project
                     # &copy; 2025 ... </p>
                     
                     # Split by lines to find the copyright line
                    lines = new_content.split('\n')
                    for i, line in enumerate(lines):
                        if "&copy;" in line and "</p>" in line:
                             if 'id="visit-counter"' not in line:
                                 # Replace default copyright closing
                                 lines[i] = line.replace("</p>", f" {COUNTER_HTML_SNIPPET}</p>")
                                 inserted_span = True
                                 break
                    new_content = "\n".join(lines)

                if not inserted_span:
                    # Fallback: Insert before </footer>
                    if "</footer>" in new_content:
                        new_content = new_content.replace("</footer>", f"<div style='text-align:center; margin-bottom:10px;'>{COUNTER_HTML_SNIPPET}</div>\n</footer>")
                
                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"  Updated {file}")
                else:
                    print(f"  No changes made to {file}")

print("All Done!")
