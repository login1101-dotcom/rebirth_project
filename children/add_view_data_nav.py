
import os
import re

# Configuration
base_dir = "/Users/jono/Desktop/rebirth_project/children"

# Define the View Data link HTML to insert
# We want to insert it before the Project Hub link
view_data_link = '<li><a href="view_data.html" class="nav-view-data">View Data</a></li>'

def update_nav(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if View Data link already exists to avoid duplicates
    if 'href="view_data.html"' in content:
        print(f"Skipping {filepath}: View Data link already exists.")
        return

    # Regex to find the <ul> inside <nav class="main-nav">
    # We look for the last <li> which is usually the Project Hub link, and insert before it
    # Or simply append to the list if we can find the closing </ul>
    
    # Strategy: Find "<li><a href=\"../../rebirth_parent/index.html\">" and insert before it
    # This assumes all child sites use the same relative path for the parent link
    
    target_str = '<li><a href="../../rebirth_parent/index.html">'
    
    if target_str in content:
        new_content = content.replace(target_str, f'{view_data_link}\n                    {target_str}')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
    else:
        print(f"Warning: Could not find Project Hub link in {filepath}")

def main():
    # Iterate over all directories in children
    for item in os.listdir(base_dir):
        dirpath = os.path.join(base_dir, item)
        if os.path.isdir(dirpath):
            print(f"Processing directory: {item}")
            for root, _, files in os.walk(dirpath):
                for file in files:
                    if file.endswith('.html'):
                        update_nav(os.path.join(root, file))

if __name__ == "__main__":
    main()
