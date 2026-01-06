import os
import re

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

deleted = []
kept = []

for root, dirs, files in os.walk(CHILDREN_DIR):
    for f in files:
        if f.startswith("post_") and f.endswith(".html"):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', content)
            if date_match:
                date_str = date_match.group(1)
                # Parse date
                year, month, day = map(int, date_str.split('.'))
                
                # RE:BIRTH REAL LOGS start from Dec 2025
                is_real = False
                if year > 2025:
                    is_real = True
                elif year == 2025 and month == 12:
                    is_real = True
                
                if not is_real:
                    print(f"Deleting FAKE (Date {date_str}): {path}")
                    os.remove(path)
                    deleted.append(path)
                else:
                    print(f"Keeping REAL (Date {date_str}): {path}")
                    kept.append(path)
            else:
                # No date found - probably fake template
                print(f"Deleting FAKE (No Date): {path}")
                os.remove(path)
                deleted.append(path)

print(f"Summary: Deleted {len(deleted)}, Kept {len(kept)}")
