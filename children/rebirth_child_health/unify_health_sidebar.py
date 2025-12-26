import os

# Define the standard sidebar content structure extracted from index.html (Profile -> Ads -> Categories)
# Note: Styles are preserved.
STANDARD_SIDEBAR = """        <aside class="sidebar">

            <!-- Author Widget -->
            <div class="widget profile-widget">
                <div class="profile-img"></div> <!-- Placeholder image -->
                <h3 style="font-size:1.1rem; margin-bottom:0.5rem;">Bio 55</h3>
                <p style="font-size:0.9rem; color:var(--text-light); line-height:1.6;">
                    健康寿命を延ばす実験中。<br>
                    現在の目標：体脂肪率 20%以下
                </p>
            </div>

            <!-- AdSense Widget (Top) -->
            <div class="widget">
                <h4 class="widget-label"
                    style="font-size:0.7rem; color:#999; margin-bottom:0.5rem; text-transform:uppercase;">Sponsored</h4>
                <div class="adsense-placeholder">
                    Ads Display
                </div>
            </div>

            <!-- Categories -->
            <div class="widget">
                <h3 class="widget-title">Categories</h3>
                <div id="category-list"></div>
            </div>

        </aside>"""

TARGET_DIR = "/Users/jono/Desktop/rebirth_project/children/rebirth_child_health"

def update_sidebar(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the sidebar block
    start_tag = '<aside class="sidebar">'
    end_tag = '</aside>'
    
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag)
    
    if start_idx != -1 and end_idx != -1:
        # Check if it's index.html, we don't need to update it since it is the source, 
        # but actually for consistency we can overwrite it (it should be same).
        # However, index.html sidebar is exactly what we put in STANDARD_SIDEBAR (minus whitespace variations)
        # To be safe, let's update everything EXCEPT index.html? 
        # User said "Home is OK", so we want others to match Home.
        # So we update others.
        if "index.html" in file_path:
            return # Skip index since it is the master
            
        new_content = content[:start_idx] + STANDARD_SIDEBAR + content[end_idx + len(end_tag):]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(file_path)}")
    else:
        print(f"Sidebar not found in {os.path.basename(file_path)}")

def main():
    if not os.path.exists(TARGET_DIR):
        print("Directory not found")
        return

    for fname in os.listdir(TARGET_DIR):
        if fname.endswith(".html"):
            update_sidebar(os.path.join(TARGET_DIR, fname))

if __name__ == "__main__":
    main()
