
import os

target_files = [
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_novel/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_health/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_english/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_youtube/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_manga/article.html",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_reading/article.html" # Added just in case it was missed
]

def reduce_banner_height(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "height:300px" in content:
        new_content = content.replace("height:300px", "height:180px")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {os.path.basename(os.path.dirname(filepath))}")
    else:
        print(f"No big banner found in: {os.path.basename(os.path.dirname(filepath))}")

for p in target_files:
    reduce_banner_height(p)
