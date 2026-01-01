
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def soften_article_headers(style_path):
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Soften the header: lighter shadow, thinner border, better position
    # and we won't use 'currentColor' for border if possible, we will handle it below
    content = re.sub(
        r'\.single-post header\.bg-styled\s*{[^}]*}',
        '.single-post header.bg-styled {\n    padding: 1.2rem 1.8rem;\n    border-radius: 8px;\n    margin-bottom: 2rem;\n    box-shadow: 0 2px 8px rgba(0,0,0,0.03);\n    border-left: 4px solid var(--primary);\n}',
        content
    )

    # 2. Assign specific border colors for each category so they aren't 'blackish'
    # We look for the Category Background Utilities and add border-left-color there.
    
    # Blue
    content = content.replace('.bg-daily {', '.bg-daily {\n    border-left-color: var(--color-daily) !important;')
    # Red
    content = content.replace('.bg-analysis {', '.bg-analysis {\n    border-left-color: var(--color-analysis) !important;')
    # Tools/Others
    content = content.replace('.bg-tools {', '.bg-tools {\n    border-left-color: var(--color-tools) !important;')
    
    # Manga colors
    content = content.replace('.bg-practice {', '.bg-practice {\n    border-left-color: var(--color-practice) !important;')
    content = content.replace('.bg-works {', '.bg-works {\n    border-left-color: var(--color-works) !important;')
    
    # English Gym specialized
    content = content.replace('.bg-reading {', '.bg-reading {\n    border-left-color: var(--color-reading) !important;')
    content = content.replace('.bg-listening {', '.bg-listening {\n    border-left-color: var(--color-listening) !important;')
    content = content.replace('.bg-writing {', '.bg-writing {\n    border-left-color: var(--color-writing) !important;')
    content = content.replace('.bg-speaking {', '.bg-speaking {\n    border-left-color: var(--color-speaking) !important;')
    content = content.replace('.bg-vocabulary {', '.bg-vocabulary {\n    border-left-color: var(--color-vocabulary) !important;')

    # 3. Restore the lighter gradients (somewhere between 'too faint' and 'too dark')
    replacements = {
        '#dbeafe, #bfdbfe': '#eff6ff, #dbeafe', # Back to blue-ish
        '#fee2e2, #fecaca': '#fef2f2, #fee2e2', # Back to pink-ish
        '#e2e8f0, #cbd5e1': '#f8fafc, #e2e8f0', # Back to light slate
    }
    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    for item in os.listdir(base_dir):
        site_dir = os.path.join(base_dir, item)
        if not os.path.isdir(site_dir): continue
        
        style_p = os.path.join(site_dir, "style.css")
        if os.path.exists(style_p):
            soften_article_headers(style_p)
            print(f"Softened article headers in {item}")

if __name__ == "__main__":
    main()
