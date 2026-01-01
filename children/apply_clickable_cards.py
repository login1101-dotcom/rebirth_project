
import os
import re

# Base directory for children sites
base_dir = "/Users/jono/Desktop/rebirth_project/children"

# CSS snippet to inject for clickable cards
css_snippet = """
/* Extended Click Area for Article Cards */
.article-card {
    position: relative; /* establish positioning context */
}

/* Ensure the link covers the entire card */
.article-card a {
    display: flex;
    flex-direction: column;
    height: 100%;
    text-decoration: none;
    color: inherit;
    position: static;
}

.article-card a::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
}

/* Ensure inner links (if any, like categories) are still clickable above the card link */
.article-card .article-meta a {
    position: relative;
    z-index: 2;
}
"""

def update_style_css(dir_path):
    style_path = os.path.join(dir_path, "style.css")
    if not os.path.exists(style_path):
        print(f"Skipping (no style.css): {dir_path}")
        return

    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already applied to avoid duplication
    if ".article-card a::before" in content:
        print(f"Skipping (already updated): {os.path.basename(dir_path)}")
        return

    # Look for .article-card definition to insert `position: relative` if missing
    # or just append the whole block at the end, but we need to remove the duplicate .article-card definition if we are strict.
    # However, CSS is cascading, so appending at the end will override or extend.
    # To be cleaner, we can just append the snippet to the end of the file.
    
    # But wait, we need to make sure we don't break existing layouts.
    # The snippet assumes .article-card exists.
    
    new_content = content + "\n" + css_snippet
    
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated: {os.path.basename(dir_path)}")

def main():
    # List all directories in children folder
    for item in os.listdir(base_dir):
        dir_path = os.path.join(base_dir, item)
        if os.path.isdir(dir_path):
            # Apply to all child folders (typing, health, english, etc.)
            update_style_css(dir_path)

if __name__ == "__main__":
    main()
