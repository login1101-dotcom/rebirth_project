
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def robust_html_cleanup(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Merge duplicate class attributes: class="a" class="b" -> class="a b"
    def merge_class_attributes(match):
        full_tag_start = match.group(0) # e.g., <a class="nav-reading" class="active" href="...">
        tag_name = match.group(1)
        
        # Extract all class content
        class_contents = re.findall(r'class="([^"]*)"', full_tag_start)
        if len(class_contents) <= 1:
            return full_tag_start
        
        # Merge classes
        merged_classes = " ".join(class_contents).split()
        unique_classes = []
        seen = set()
        for c in merged_classes:
            if c not in seen:
                unique_classes.append(c)
                seen.add(c)
        
        # Remove all class attributes from the string
        cleaned_tag = re.sub(r'\s*class="[^"]*"', '', full_tag_start)
        # Re-insert the merged one right after the tag name
        final_tag = cleaned_tag.replace(f'<{tag_name}', f'<{tag_name} class="{" ".join(unique_classes)}"')
        return final_tag

    # Match any opening tag that has at least one class attribute
    html = re.sub(r'<([a-z0-9]+)\s+[^>]*class="[^"]*"[^>]*>', merge_class_attributes, html, flags=re.IGNORECASE)

    # 2. Cleanup double spaces inside class names
    html = re.sub(r'class="([^"]*)"', lambda m: f'class="{ " ".join(m.group(1).split()) }"', html)

    # 3. Ensure Japanese translations for labels in all files
    translations = {
        ">Home<": ">ホーム<",
        ">Reading<": ">リーディング<",
        ">Listening<": ">リスニング<",
        ">Writing<": ">ライティング<",
        ">Speaking<": ">スピーキング<",
        ">Vocabulary<": ">語彙・フレーズ<",
        ">Daily Log<": ">練習記録<",
        ">Analysis<": ">分析<",
        ">Tools<": ">ツール<",
        ">Diet / Meal<": ">食事<",
        ">Muscle Training<": ">筋トレ<",
        ">Sleep / Relax<": ">睡眠<",
        ">Others<": ">その他<",
        ">Essay<": ">エッセイ<",
        ">Novel<": ">小説<",
        ">Practice<": ">練習記録<",
        ">Works<": ">制作物<"
    }
    for eng, jap in translations.items():
        html = html.replace(eng, jap)

    # 4. English site specific: fix the card thumb colors if they are sticking to old values
    # Actually my CSS sync should handle the colors, but I should ensure the classes are correct.
    # (The robust_repair.py already tried this, but let's double check common mistakes)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                robust_html_cleanup(os.path.join(root, file))
    print("Robust HTML cleanup completed.")
