
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def update_dashboard_button(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to find the dashboard card section and update the button inside it.
    # However, a simpler regex might work if btn-primary is mainly used there.
    # Let's target the specific line pattern often seen: <a href="..." class="btn-primary">...</a>
    # We will replace ANY usage of btn-primary with the correct link and text IF it looks like a dashboard button 
    # (i.e., inside a div, possibly with href="#" or existing link).
    
    # Pattern: <a href="[^"]*" class="btn-primary">.*?</a>
    # We want to replace it with: <a href="view_data.html" class="btn-primary">View Data</a>
    
    pattern = re.compile(r'<a href="[^"]*" class="btn-primary">.*?</a>')
    
    # We should only replace this if we are relatively sure it's the dashboard button.
    # Given the templates, this class is unique to that button in index.html (Read More links use text styles).
    
    new_btn = '<a href="view_data.html" class="btn-primary">View Data</a>'
    
    # Check if we need to update
    matches = pattern.findall(content)
    updated = False
    
    if matches:
        for match in matches:
            if match != new_btn:
                print(f"Updating in {os.path.basename(os.path.dirname(filepath))}: {match} -> {new_btn}")
                content = content.replace(match, new_btn)
                updated = True
    
    if updated:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print(f"No changes needed for {os.path.basename(os.path.dirname(filepath))}")

def main():
    for item in os.listdir(base_dir):
        dirpath = os.path.join(base_dir, item)
        if os.path.isdir(dirpath):
            index_path = os.path.join(dirpath, "index.html")
            if os.path.exists(index_path):
                update_dashboard_button(index_path)

if __name__ == "__main__":
    main()
