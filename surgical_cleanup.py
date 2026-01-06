import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

# Titles that are DEFINITELY fakes I generated
FAKE_TITLE_PATTERNS = [
    "Reading Data Log: Toki Soba",
    "My First English Essay: Why I Code",
    "CNN 10を毎日聴き続けて",
    "初心者におすすめの洋書",
    "3行日記から始める英語アウトプット",
    "英語でTo-Doリストを書くと実行力が上がる件",
    "多読を開始して1ヶ月",
    "ポッドキャスト学習法",
    "40代から始めるサプリメント",
    "コンビニで買える「神」高タンパクおやつ",
    "自宅で始める自重トレーニング",
    "ダンベル1つで体は変わる",
    "7時間寝ても疲れが取れない",
    "枕難民に終止符を",
    "51歳からの夜間練習ルーティン",
    "HHKBのキートップ交換",
    "指の動きの効率化",
    "【計画】Typing Master Road Map 2026",
    "Re:Birth 55プロジェクトへようこそ",
    "Vlog #01：初めてのソロキャンプ",
    "Vlog：雨の日の珈琲焙煎",
    "DaVinci Resolve無料版でここまでできる",
    "iPhone撮影でも音は重要",
    "台本なしトークは事故の元",
    "照明ひとつで肌年齢が変わる",
    "連載：第1話",
    "自作PCの魅力"
]

def is_fake(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Check title
    title_match = re.search(r'<h1>(.*?)</h1>', content)
    if title_match:
        t = title_match.group(1)
        if any(p in t for p in FAKE_TITLE_PATTERNS):
            return True
            
    # 2. Check for signature template phrases
    if "Re:Birth 55プロジェクトへようこそ" in content:
        return True
    if "今回のテーマは" in content and "実際に取り組んでみて分かったこと" in content:
        return True
    if "明日からできること" in content and "一歩ずつ、しかし着実に" in content:
        return True
    
    # "Let It Be" is specifically REAL
    if "Let It Be 聴解チャレンジ" in content:
        return False
        
    # Health articles about Bouryoku/Imo Pan are REAL
    if any(p in content for p in ["暴食", "いもパン", "おにぎり", "逆流性食道炎"]):
        return False
        
    # Typing struggle with "B" is REAL
    if "中級1の苦戦" in content:
        return False

    return False

print("Surgical cleanup starting...")

deleted = 0
kept = []

for root, dirs, files in os.walk(CHILDREN_DIR):
    for f in files:
        if f.startswith("post_") and f.endswith(".html"):
            path = os.path.join(root, f)
            if is_fake(path):
                print(f"DELETING FAKE: {path}")
                os.remove(path)
                deleted += 1
            else:
                print(f"KEEPING REAL: {path}")
                kept.append(path)

print(f"\nDELETED: {deleted}")
print(f"KEPT: {len(kept)}")
for k in kept:
    print(f"  - {k}")
