import os
import re

# Directory
target_dir = 'rebirth_child_typing'
base_path = '/Users/jono/Desktop/rebirth_project/children'
dir_path = os.path.join(base_path, target_dir)

# Text to identify the span
target_text = 'アイデアを逃さない、ストレスフリーな指先へ。'

# New Style
# Larger size (0.8 -> 1.0rem or 1.1rem), Darker color (#64748b -> #334155), Bolder (normal -> 600)
new_style = 'font-size: 1.0rem; color: #334155; margin-left: 15px; font-weight: 600; letter-spacing: 0.05em;'

print(f"Updating style for: {target_text}")

# Regex to match the span containing the specific text
# capturing the style attribute content to replace it, or just replacing the whole tag opening
# <span style="...">TEXT</span>
span_pattern = re.compile(r'(<span\s+style=")([^"]+)("\s*>)(' + re.escape(target_text) + r')(</span>)', re.IGNORECASE)

if os.path.exists(dir_path):
    for filename in os.listdir(dir_path):
        if filename.endswith('.html'):
            file_path = os.path.join(dir_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replacement function
            def replace_style(m):
                # m.group(1): <span style="
                # m.group(2): existing style
                # m.group(3): ">
                # m.group(4): text
                # m.group(5): </span>
                return f'{m.group(1)}{new_style}{m.group(3)}{m.group(4)}{m.group(5)}'

            new_content = span_pattern.sub(replace_style, content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  Updated style in: {filename}")
            else:
                if target_text in content:
                     print(f"  Target found but regex didn't match (style might be different?): {filename}")
                else:
                     print(f"  Target text not found: {filename}")
