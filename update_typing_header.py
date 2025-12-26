import os
import re

# Goal text to update
target_dir = 'rebirth_child_typing'
new_text = 'アイデアを逃さない、ストレスフリーな指先へ。'
old_text = 'ブラインドタッチを習得する'

base_path = '/Users/jono/Desktop/rebirth_project/children'
dir_path = os.path.join(base_path, target_dir)

print(f"Updating {target_dir} -> {new_text}")

# Regex to match the span we inserted previously
# <span ...>OLD_TEXT</span>
# We need to be flexible with the span attributes as they are specific
span_pattern = re.compile(r'(<span[^>]*>)(' + re.escape(old_text) + r')(</span>)', re.IGNORECASE)

if os.path.exists(dir_path):
    for filename in os.listdir(dir_path):
        if filename.endswith('.html'):
            file_path = os.path.join(dir_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace old text with new text within the span
            # We use a function to keep the surrounding tags
            new_content = span_pattern.sub(lambda m: f"{m.group(1)}{new_text}{m.group(3)}", content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  Updated: {filename}")
            else:
                if new_text in content:
                     print(f"  Already updated: {filename}")
                elif old_text not in content:
                     print(f"  Old text not found: {filename}")

# Also update the Parent Index button separately if needed?
# The user asked to change the text based on the "one sentence explanation". 
# Usually, this applies to the header slogan I just added. 
# The button on the parent page is "Acrivement List" (Noshitogeru koto list).
# "Mastering touch typing" (Blind touch wo shotoku suru) is the GOAL. 
# "Idea wo nogasanai..." is the WHY/VISION.
# The user's previous prompt was "Header ni ichibun irete" (Put a sentence in the header).
# So I will ONLY update the Child Site Header for now.
# If the user wants to change the parent button, they will ask or I can ask. 
# BUT, looking at the previous context: "stress naku..." -> "input stress de idea wo..." 
# This sounds like a refinement of the "Goal/Vision".
# I'll stick to updating the child site headers as explicitly implied by the context of "header refinement".
