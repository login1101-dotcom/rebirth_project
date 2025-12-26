
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

site_display_names = {
    "rebirth_child_english": "English Gym",
    "rebirth_child_health": "Body Logic",
    "rebirth_child_manga": "Manga Lab",
    "rebirth_child_novel": "Writer's Desk",
    "rebirth_child_reading": "Reading Log",
    "rebirth_child_typing": "Typing Lab",
    "rebirth_child_youtube": "YouTube Lab"
}

def final_deep_cleanup(site_dir):
    site_id = os.path.basename(site_dir)
    display_name = site_display_names.get(site_id, site_id)
    
    for root, dirs, files in os.walk(site_dir):
        for file in files:
            if not file.endswith(".html"): continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()

            # 1. Fix Title Tags: change "rebirth_child_english" to "English Gym"
            html = html.replace(f" | {site_id}", f" | {display_name}")

            # 2. Fix Duplicate Class Attributes
            def merge_classes(match):
                tag_content = match.group(1)
                # Find all class="..."
                classes = re.findall(r'class="([^"]*)"', tag_content)
                if len(classes) > 1:
                    new_classes = " ".join(classes).split()
                    # unique while preserving order
                    seen = set()
                    unique_classes = [x for x in new_classes if not (x in seen or seen.add(x))]
                    # Remove all class="..." from tag_content
                    tag_content = re.sub(r'\s*class="[^"]*"', '', tag_content)
                    return f'<{match.group(2)} class="{" ".join(unique_classes)}"{tag_content}'
                return match.group(0)

            # Match <tag class="..." class="..."> (simplified)
            html = re.sub(r'<([a-zA-Z0-9]+)(\s+[^>]*class="[^"]*"[^>]*)>', merge_classes, html)

            # 3. Ensure Japanese Category names in Meta/Tags
            # English Gym
            html = html.replace("🎧 Listening", "リスニング")
            html = html.replace("📖 Reading", "リーディング")
            html = html.replace("✍️ Writing", "ライティング")
            html = html.replace("🗣️ Speaking", "スピーキング")
            # Novel Lab
            html = html.replace(">Essay<", ">エッセイ<")
            html = html.replace(">Novel<", ">小説<")
            # Others
            html = html.replace("Diet / Meal", "食事")
            html = html.replace("Walking", "ウォーキング")

            # 4. Clean up nav whitespace
            html = html.replace('<nav class="main-nav"><ul>', '<nav class="main-nav">\n                <ul>\n                    ')
            html = html.replace('</ul></nav>', '\n                </ul>\n            </nav>')

            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)

if __name__ == "__main__":
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            final_deep_cleanup(site_path)
