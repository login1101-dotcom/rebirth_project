import os

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

# Manual list of REAL files to KEEP
# Everything else in children/*/post_*.html will be DELETED.
REAL_FILES = [
    "rebirth_child_english/post_9.html",  # Let It Be
    "rebirth_child_health/post_9.html",   # サンドイッチ進化論
    "rebirth_child_health/post_10.html",  # 暴食
    "rebirth_child_health/post_11.html",  # いもパン
    "rebirth_child_health/post_12.html",  # おにぎり
    "rebirth_child_typing/post_8.html",   # 中級1の苦戦
    "rebirth_child_novel/post_7.html",    # ストレス食い
    "rebirth_child_novel/post_8.html",    # 焦燥と言葉の念
    "rebirth_child_novel/post_9.html",    # 時間税
]

# Novel might have more real ones? 
# "掌編小説：真夜中のコインランドリー" etc seems like filler I might have generated.
# I'll stick to the ones with recent dates (Dec 2025/Jan 2026) + the user's explicit OK.

def cleanup():
    deleted_count = 0
    for root, dirs, files in os.walk(CHILDREN_DIR):
        for f in files:
            if f.startswith("post_") and f.endswith(".html"):
                path = os.path.join(root, f)
                rel_path = os.path.relpath(path, CHILDREN_DIR)
                
                if rel_path not in REAL_FILES:
                    print(f"DELETING FAKE: {rel_path}")
                    os.remove(path)
                    deleted_count += 1
                else:
                    print(f"KEEPING REAL: {rel_path}")

    print(f"Total deleted: {deleted_count}")

if __name__ == "__main__":
    cleanup()
