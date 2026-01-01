
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def clean_article_headers(style_path):
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the styled header to be EXACTLY like the sidebar widgets
    # White background, 1px border, no shadow, no thick left border.
    content = re.sub(
        r'\.single-post header\.bg-styled\s*{[^}]*}',
        '.single-post header.bg-styled {\n    padding: 1.5rem 2rem;\n    background: var(--bg-card);\n    border: 1px solid var(--border);\n    border-radius: 12px;\n    margin-bottom: 2rem;\n    box-shadow: none;\n}',
        content
    )

    # 2. Update category utilities to color the TEXT of the title when in a styled header
    # We want .bg-daily inside .single-post header to color its own h1
    
    # First, let's remove the background-color overrides we added earlier to bg-xxx
    content = re.sub(r'border-left-color:.*?!important;', '', content)
    
    # Add a rule to color the H1 based on the header's category class
    color_rules = """
/* Category-specific Title Colors (Instead of backgrounds) */
.single-post header.bg-daily h1 { color: var(--color-daily); }
.single-post header.bg-analysis h1 { color: var(--color-analysis); }
.single-post header.bg-tools h1 { color: var(--color-tools); }

.single-post header.bg-reading h1 { color: var(--color-reading); }
.single-post header.bg-listening h1 { color: var(--color-listening); }
.single-post header.bg-writing h1 { color: var(--color-writing); }
.single-post header.bg-speaking h1 { color: var(--color-speaking); }
.single-post header.bg-vocabulary h1 { color: var(--color-vocabulary); }

.single-post header.bg-practice h1 { color: var(--color-practice); }
.single-post header.bg-works h1 { color: var(--color-works); }

.single-post header.bg-diet h1 { color: var(--color-diet); }
.single-post header.bg-muscle h1 { color: var(--color-muscle); }
.single-post header.bg-sleep h1 { color: var(--color-sleep); }
"""
    # Remove old custom color rules if any
    content = re.sub(r'/\* Category-specific Title Colors.*$', '', content, flags=re.DOTALL)
    content += "\n" + color_rules

    # 3. Clean up the base categories to NOT have strong backgrounds
    # We'll make them very faint or transparent for the header
    content = content.replace('background: linear-gradient(to right, #eff6ff, #dbeafe) !important;', 'background: transparent !important;')
    content = content.replace('background: linear-gradient(to right, #fef2f2, #fee2e2) !important;', 'background: transparent !important;')
    content = content.replace('background: linear-gradient(to right, #f8fafc, #e2e8f0) !important;', 'background: transparent !important;')

    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    for item in os.listdir(base_dir):
        site_dir = os.path.join(base_dir, item)
        if not os.path.isdir(site_dir): continue
        
        style_p = os.path.join(site_dir, "style.css")
        if os.path.exists(style_p):
            clean_article_headers(style_p)
            print(f"Cleaned article headers in {item}")

if __name__ == "__main__":
    main()
