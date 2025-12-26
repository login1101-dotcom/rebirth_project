import os
import re

CHILDREN_DIR = "/Users/jono/Desktop/rebirth_project/children"

# Mapping logic based on link filename
def get_class_name(site_name, link):
    if "category_daily" in link: return "text-daily"
    if "category_analysis" in link: return "text-analysis"
    if "category_tools" in link: 
        if site_name == "rebirth_child_typing": return "text-tools"
        if site_name == "rebirth_child_youtube": return "text-tools"
        return "text-tools"
    
    # Health
    if "category_diet" in link: return "text-diet"
    if "category_muscle" in link: return "text-muscle"
    if "category_sleep" in link: return "text-sleep"
    
    # English
    if "category_writing" in link: return "text-writing"
    if "category_speaking" in link: return "text-speaking"
    if "category_listening" in link: return "text-listening"
    if "category_reading" in link: return "text-reading"
    if "category_vocabulary" in link: return "text-vocabulary"
    
    # Manga
    if "category_practice" in link: return "text-practice"
    if "category_works" in link: return "text-works"
    
    # Novel
    if "category_short" in link: return "text-short"
    if "category_essay" in link: return "text-essay"
    
    # YouTube
    if "category_process" in link: return "text-process"
    
    # Others
    if "category_others" in link:
        if site_name == "rebirth_child_novel":
            return "text-other"
        return "text-others"
        
    return ""

def process_site(site_name):
    js_path = os.path.join(CHILDREN_DIR, site_name, "sidebar.js")
    if not os.path.exists(js_path):
        return

    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple regex to replace className: "..." or className: ""
    # We iterate line by line to have context of 'link'
    
    new_lines = []
    lines = content.split('\n')
    
    for line in lines:
        if "className:" in line and "link:" in line:
            # Extract link
            link_match = re.search(r'link:\s*"([^"]+)"', line)
            if link_match:
                link = link_match.group(1)
                new_class = get_class_name(site_name, link)
                
                # Replace className value
                # Pattern: className: ".*?"
                line = re.sub(r'className:\s*"[^"]*"', f'className: "{new_class}"', line)
        
        new_lines.append(line)
    
    new_content = '\n'.join(new_lines)
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated sidebar.js for {site_name}")

def main():
    sites = [
        "rebirth_child_typing",
        "rebirth_child_health",
        "rebirth_child_english",
        "rebirth_child_manga",
        "rebirth_child_novel",
        "rebirth_child_youtube"
    ]
    
    for site in sites:
        process_site(site)

if __name__ == "__main__":
    main()
