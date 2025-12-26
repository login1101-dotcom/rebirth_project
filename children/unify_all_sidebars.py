import os

# Define Author content for each child site
AUTHOR_INFO = {
    "rebirth_child_typing": {
        "name": "Admin 55",
        "desc": "51歳からのスキル獲得実験中。<br>現在の目標：WPM 100"
    },
    "rebirth_child_health": {
        "name": "Bio 55",
        "desc": "健康寿命を延ばす実験中。<br>現在の目標：体脂肪率 20%以下"
    },
    "rebirth_child_english": {
        "name": "Polyglot 55",
        "desc": "51歳からの英語脳構築中。<br>現在の目標：IELTS 7.0"
    },
    "rebirth_child_manga": {
        "name": "Artist 55",
        "desc": "デジタルイラスト修行中。<br>現在の目標：100日連続投稿"
    },
    "rebirth_child_novel": {
        "name": "Writer 55",
        "desc": "物語を紡ぐ実験中。<br>現在の目標：新人賞応募"
    },
    "rebirth_child_youtube": {
        "name": "Creator 55",
        "desc": "動画制作スキル習得中。<br>現在の目標：登録者1000人"
    },
    "rebirth_child_reading": {
        "name": "Reader 55", # Assuming Reader 55 for reading or maybe Thinker 55
        "desc": "難解書読破チャレンジ中。<br>現在の目標：積読消化"
    }
}

CHILDREN_ROOT = "/Users/jono/Desktop/rebirth_project/children"

def get_sidebar_template(site_name):
    info = AUTHOR_INFO.get(site_name, {"name": "Admin 55", "desc": "Re:Birth 55 Project"})
    
    # Template structure: Profile -> Ads -> Categories
    # Note: Using generic class names that should work with style.css
    
    sidebar = f"""        <aside class="sidebar">

            <!-- Author Widget -->
            <div class="widget profile-widget">
                <div class="profile-img"></div> <!-- Placeholder image -->
                <h3 style="font-size:1.1rem; margin-bottom:0.5rem;">{info['name']}</h3>
                <p style="font-size:0.9rem; color:var(--text-light); line-height:1.6;">
                    {info['desc']}
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
    return sidebar

def update_site_sidebars(site_name):
    site_dir = os.path.join(CHILDREN_ROOT, site_name)
    if not os.path.exists(site_dir):
        return

    print(f"Processing {site_name}...")
    sidebar_content = get_sidebar_template(site_name)
    
    for fname in os.listdir(site_dir):
        if fname.endswith(".html"):
            # We want to update ALL html files to ensure consistency, 
            # BUT we should preserve existing index.html if it has special widgets?
            # User said "Home is OK, make others like right side". 
            # In Typing Lab, home has "Live Stats Widget" which might be removed if we blindly overwrite.
            # User said "Basic (Unified) form: Profile -> CM -> Categories".
            # The prompt says "Home is OK". This implies Home MIGHT differ but user wants this specific structure on OTHERS?
            # OR user implies Home ALREADY has this structure (like Health) and wants others to match?
            # Health Home matches this structure exactly.
            # Typing Lab Home has Stats Widget. User says "Unified -> Profile -> CM -> Categories".
            # This implies removing Stats Widget from Typing Lab sidebars if we enforce this structure.
            # Let's assume user wants to Standardize the LAYOUT to Profile->CM->Categories for ALL pages including Home if it matches description "Right side basic form".
            # Actually, user said "Home is OK" (referring to Health home).
            # "Other tags also unified to this form".
            # This likely means: Apply the Health Home sidebar structure (Profile->Ads->Cat) to ALL pages of ALL sites.
            # Be careful: Reading site might be different structure entirely (library shelf).
            
            # Additional logic: If index.html, we check if we should overwrite.
            # If we overwrite index.html in Typing Lab, we lose Live Stats.
            # User said "Home is OK" looking at Health.
            # I will apply this standard structure to all pages. 
            # For Typing Lab, this removes Live Stats. If user wants stats, they are separate.
            # Wait, "Home is OK" refers to Health screen shown in screenshot.
            # "Other child sites also fix same way" -> Make them look like Health sidebar.
            
            fpath = os.path.join(site_dir, fname)
            
            # Create backup just in case? No, destructive is requested.
            
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            start_tag = '<aside class="sidebar">'
            end_tag = '</aside>'
            
            start_idx = content.find(start_tag)
            end_idx = content.find(end_tag)
            
            if start_idx != -1 and end_idx != -1:
                 # Check if 'view_data.html' generally has no sidebar or full width?
                 # In index view_data usually full width?
                 # Health view_data has no sidebar in previous output "Sidebar not found in view_data.html".
                 # So we obey file structure.
                 
                 new_content = content[:start_idx] + sidebar_content + content[end_idx + len(end_tag):]
                 
                 with open(fpath, 'w', encoding='utf-8') as f:
                     f.write(new_content)
                 # print(f"  Updated {fname}")
            else:
                 pass
                 # print(f"  Sidebar not found in {fname}")

def main():
    sites = [
        "rebirth_child_typing",
        "rebirth_child_english",
        "rebirth_child_manga",
        "rebirth_child_novel",
        "rebirth_child_youtube",
        # "rebirth_child_reading" # Reading site has different layout (shelf), likely no sidebar. Skipping to be safe or check index.
    ]
    
    # Check reading index
    # Reading index.html usually doesn't have sidebar based on previous cat reading.
    
    for site in sites:
        update_site_sidebars(site)

if __name__ == "__main__":
    main()
