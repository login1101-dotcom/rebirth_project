
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

# Translation Map for Nav Items
translations = {
    ">Home<": ">ホーム<",
    ">Reading<": ">リーディング<",
    ">Listening<": ">リスニング<",
    ">Writing<": ">ライティング<",
    ">Speaking<": ">スピーキング<",
    ">Vocabulary<": ">語彙<",
    ">Essay<": ">エッセイ<",
    ">Novel<": ">小説<",
    ">View Data<": ">データ表示<",
    ">Planning<": ">企画<",
    ">Shooting<": ">撮影<",
    ">Editing<": ">編集<",
    ">Practice<": ">練習<",
    ">Works<": ">作品<",
    ">Diet<": ">食事<",
    ">Muscle<": ">筋トレ<",
    ">Sleep<": ">睡眠<",
    ">Others<": ">その他<"
}

def translate_nav_items(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for eng, jap in translations.items():
        content = content.replace(eng, jap)
    
    # Also handle some variations like common breadcrumbs or meta spans
    content = content.replace(">Home</a>", ">ホーム</a>")
    content = content.replace("Home >", "ホーム >")
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            count = 0
            for root, dirs, files in os.walk(site_path):
                for file in files:
                    if file.endswith(".html"):
                        if translate_nav_items(os.path.join(root, file)):
                            count += 1
            print(f"Translated {count} files in {item}")

if __name__ == "__main__":
    main()
