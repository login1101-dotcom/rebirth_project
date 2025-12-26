
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def restore_card_colors_but_keep_post_header_white(style_path):
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Restore the backgrounds for the utility classes (used by cards)
    # We remove the 'background: transparent !important' that I added
    content = content.replace('background: transparent !important;', '')

    # Ensure the gradients are back and vibrant for the cards
    # (Re-applying the standard ones we had)
    replacements = {
        # Standard Blue
        '.bg-daily {': '.bg-daily {\n    background: linear-gradient(to right, #eff6ff, #dbeafe) !important;',
        '.bg-reading {': '.bg-reading {\n    background: linear-gradient(to right, #eff6ff, #dbeafe) !important;',
        '.bg-listening {': '.bg-listening {\n    background: linear-gradient(to right, #eff6ff, #dbeafe) !important;',
        # Standard Red
        '.bg-analysis {': '.bg-analysis {\n    background: linear-gradient(to right, #fef2f2, #fee2e2) !important;',
        '.bg-writing {': '.bg-writing {\n    background: linear-gradient(to right, #fef2f2, #fee2e2) !important;',
        '.bg-speaking {': '.bg-speaking {\n    background: linear-gradient(to right, #fef2f2, #fee2e2) !important;',
        # Standard Muscle Blue (if distinct)
        '.bg-muscle {': '.bg-muscle {\n    background: linear-gradient(to right, #eff6ff, #dbeafe) !important;',
        # Standard Sleep Purple
        '.bg-sleep {': '.bg-sleep {\n    background: linear-gradient(to right, #f3e8ff, #e9d5ff) !important;',
        # Standard Diet Orange
        '.bg-diet {': '.bg-diet {\n    background: linear-gradient(to right, #fff7ed, #ffedd5) !important;',
    }

    for key, val in replacements.items():
        if key in content and 'background:' not in content.split(key)[1].split('}')[0]:
            content = content.replace(key, val)

    # 2. IMPORTANT: Keep the SINGLE POST header white (the "same as right panel" request)
    # We must explicitly set background to card-bg for the article header 
    # so it overrides the .bg-xxx background
    if '.single-post header.bg-styled' in content:
        content = re.sub(
            r'\.single-post header\.bg-styled\s*{[^}]*}',
            '.single-post header.bg-styled {\n    padding: 1.5rem 2rem;\n    background: var(--bg-card) !important;\n    border: 1px solid var(--border);\n    border-radius: 12px;\n    margin-bottom: 2rem;\n    box-shadow: none;\n}',
            content
        )

    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    for item in os.listdir(base_dir):
        site_dir = os.path.join(base_dir, item)
        if not os.path.isdir(site_dir): continue
        
        style_p = os.path.join(site_dir, "style.css")
        if os.path.exists(style_p):
            restore_card_colors_but_keep_post_header_white(style_p)
            print(f"Restored card colors for {item}")

if __name__ == "__main__":
    main()
