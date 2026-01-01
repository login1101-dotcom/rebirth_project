
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def clean_duplicate_attributes(html):
    # Merge multiple class attributes into one
    # Pattern: <a ... class="X" ... class="Y" ...>
    # We'll use a more complex regex or just simple replacement for common cases
    
    def merge_class(match):
        full_tag = match.group(0)
        classes = re.findall(r'class="([^"]*)"', full_tag)
        if len(classes) > 1:
            merged = " ".join(classes)
            # Remove all existing class="..."
            new_tag = re.sub(r'\s+class="[^"]*"', '', full_tag)
            # Insert merged class inside the tag (after <a or similar)
            new_tag = re.sub(r'^(<[a-zA-Z0-9]+)', r'\1 class="' + merged + '"', new_tag)
            return new_tag
        return full_tag

    # Target <a> tags specifically for now as they are the most likely to have duplicates from my scripts
    html = re.sub(r'<a\s+[^>]*>', merge_class, html)
    
    # Also clean up double spaces in class names
    html = re.sub(r'class="([^"]*)"', lambda m: 'class="' + " ".join(m.group(1).split()) + '"', html)
    
    return html

def final_cleanup():
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            for root, dirs, files in os.walk(site_path):
                for file in files:
                    if file.endswith(".html"):
                        fpath = os.path.join(root, file)
                        with open(fpath, 'r', encoding='utf-8') as f:
                            c = f.read()
                        new_c = clean_duplicate_attributes(c)
                        if new_c != c:
                            with open(fpath, 'w', encoding='utf-8') as f:
                                f.write(new_c)

if __name__ == "__main__":
    final_cleanup()
