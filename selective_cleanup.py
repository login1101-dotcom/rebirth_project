import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

# These are the titles I know are placeholders from my previous template generations
FAKE_TITLES = [
    "枕難民に終止符を",
    "7時間寝ても疲れが取れない",
    "ダンベル1つで体は変わる",
    "自宅で始める自重トレーニング",
    "コンビニで買える「神」高タンパクおやつ",
    "40代から始めるサプリメント",
    "初心者におすすめの洋書",
    "3行日記から始める英語アウトプット",
    "英語でTo-Doリストを書くと実行力が上がる件",
    "多読を開始して1ヶ月",
    "ポッドキャスト学習法",
    "SNSで海外の趣味垢と繋がるための略語",
    "Re:Birth 55プロジェクトへようこそ",
    "今回のプロジェクトを立ち上げた理由",
    "1日10分のブラインドタッチ",
    "ホームポジションの壁を越える",
    "メカニカルキーボードの魅力",
    "My First English Essay: Why I Code",
    "CNN 10を毎日聴き続けて",
    "自己紹介：なぜ51歳でエンジニアを目指すのか",
    "プログラミング学習のロードマップ"
]

def is_definitely_fake(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'<h1>(.*?)</h1>', content)
    if title_match:
        t = title_match.group(1)
        if any(fake in t for fake in FAKE_TITLES):
            return True
            
    # Also check for very generic content patterns
    if "Re:Birth 55プロジェクトへようこそ" in content and "51歳から" in content and "日々の記録をありのままに" in content:
        # If the title is also generic, it's fake
        if title_match:
             t = title_match.group(1)
             if "記録" not in t and "2026" not in t:
                 return True
                 
    return False

print("Selectively cleaning fake articles...")

deleted = []
for root, dirs, files in os.walk(CHILDREN_DIR):
    for f in files:
        if f.startswith("post_") and f.endswith(".html"):
            path = os.path.join(root, f)
            if is_definitely_fake(path):
                print(f"Deleting verified fake: {path}")
                os.remove(path)
                deleted.append(path)

print(f"Deleted {len(deleted)} verified fake articles.")
