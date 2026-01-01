
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def add_view_data_link(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # If View Data is already there, skip
    if 'view_data.html' in content and 'nav-view-data' in content:
        return

    # Look for the last navigation item or the Project Hub link
    # Typical structure: <li><a href="../../rebirth_parent/index.html">← Project Hub</a></li>
    hub_link_pattern = r'<li><a href="\.\./\.\./rebirth_parent/index\.html">← Project Hub</a></li>'
    
    view_data_li = '<li><a href="view_data.html" class="nav-view-data">View Data</a></li>\n                    '
    
    if re.search(hub_link_pattern, content):
        new_content = re.sub(hub_link_pattern, view_data_li + r'\0', content)
        # Note: \0 or just repeat the pattern
        new_content = content.replace('<li><a href="../../rebirth_parent/index.html">← Project Hub</a></li>', 
                                     f'<li><a href="view_data.html" class="nav-view-data">View Data</a></li>\n                    <li><a href="../../rebirth_parent/index.html">← Project Hub</a></li>')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Added View Data to {os.path.basename(file_path)}")

def process_site(site_dir):
    for root, dirs, files in os.walk(site_dir):
        for file in files:
            if file.endswith(".html"):
                add_view_data_link(os.path.join(root, file))

def main():
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            print(f"Processing {item}...")
            process_site(site_path)

if __name__ == "__main__":
    main()
