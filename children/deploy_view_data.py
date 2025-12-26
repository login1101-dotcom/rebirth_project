
import os
import shutil

# Template file (Typing Lab's view_data.html)
source_file = "/Users/jono/Desktop/rebirth_project/children/rebirth_child_typing/view_data.html"

# List of target directories
target_dirs = [
    "rebirth_child_english",
    "rebirth_child_health",
    "rebirth_child_novel",
    "rebirth_child_manga",
    "rebirth_child_reading",
    "rebirth_child_youtube"
]

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def customize_content(content, site_name, site_icon, site_slogan):
    """Simple string replacement to customize the template for each site."""
    # Replace Site Title
    content = content.replace("Typing Lab", site_name)
    content = content.replace("keyboard", site_icon) # Icon usage varies, simplistic replace
    
    # Replace Icon in Title (SVG or direct char)
    # The source uses ⌨️ in title and SVG. 
    # Let's just do a generic replace of the visible text parts first.
    
    # Replace "アイデアを逃さない..." slogan
    # Note: Source has: <span ...>アイデアを逃さない、ストレスフリーな指先へ。</span>
    # We need to find this span and replace content.
    
    # For now, we will just copy the file. 
    # The user might want to customize the internal graphs later.
    # We should at least update the HEADER text to match the site.
    
    return content

def main():
    with open(source_file, 'r', encoding='utf-8') as f:
        template_content = f.read()

    for dir_name in target_dirs:
        target_path = os.path.join(base_dir, dir_name, "view_data.html")
        
        # We need to get the specific slogan/title for this site to customize the header
        # But for this step, let's just copy the file so the link works.
        # The user can then ask to customize each one.
        
        # Actually, let's try to grab the index.html of the target to find the correct header 
        # so it doesn't look completely wrong (like saying "Typing Lab" on "English Gym")
        
        index_path = os.path.join(base_dir, dir_name, "index.html")
        if os.path.exists(index_path):
             with open(index_path, 'r', encoding='utf-8') as index_f:
                index_content = index_f.read()
                
                # Extract Header content from index.html (between <header> and </header>)
                import re
                header_match = re.search(r'(<header>.*?</header>)', index_content, re.DOTALL)
                if header_match:
                    target_header = header_match.group(1)
                    
                    # Replace the header in the template with this site's header
                    # The template has its own header.
                    template_header_match = re.search(r'(<header>.*?</header>)', template_content, re.DOTALL)
                    if template_header_match:
                        new_content = template_content.replace(template_header_match.group(1), target_header)
                        
                        # Note: The copied header from index.html might NOT have the "View Data" link yet 
                        # if the index.html wasn't refreshed in memory or if we want the ACTIVE state.
                        # But we just ran add_view_data_nav.py, so index.html SHOULD have the link.
                        # However, we probably want to set the "View Data" link to 'active' class?
                        # For now, just having the correct header is good enough.
                        
                        with open(target_path, 'w', encoding='utf-8') as out_f:
                            out_f.write(new_content)
                        print(f"Created {target_path} with customized header.")
                        continue

        # Fallback if index extraction fails
        print(f"Copying to {target_path} (fallback)")
        shutil.copy(source_file, target_path)

if __name__ == "__main__":
    main()
