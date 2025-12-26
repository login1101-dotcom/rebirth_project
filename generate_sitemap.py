import os

# Configuration
BASE_URL = "https://rebirth-project.pages.dev"
PROJECT_ROOT = "/Users/jono/Desktop/rebirth_project"
SITEMAP_FILE = os.path.join(PROJECT_ROOT, "rebirth_parent", "sitemap.xml")

sitemap_template_start = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

sitemap_template_end = """</urlset>"""

url_entry_template = """  <url>
    <loc>{url}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>
"""

# Priorities
PRIORITY_HOME = "1.0"
PRIORITY_CHILD_HOME = "0.9"
PRIORITY_ARTICLE = "0.8"
PRIORITY_CATEGORY = "0.7"

pages = []

def get_lastmod(filepath):
    # For now, just use a static date or today's date for simplicity, 
    # or get actual file modification time. Let's use file mod time.
    from datetime import datetime
    try:
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    except:
        return "2025-12-27"

def process_directory(directory, base_path_segment, is_parent=False):
    if not os.path.exists(directory):
        return

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                # Exclude specific files if needed (e.g., templates, partials)
                if file.startswith("temp_") or "backup" in file or "test" in file:
                    continue

                full_path = os.path.join(root, file)
                
                # Determine relative path for URL
                rel_path = os.path.relpath(full_path, PROJECT_ROOT)
                
                # Construct URL.
                # Project structure: 
                # Parent: rebirth_parent/index.html -> ROOT/index.html
                # Children: children/rebirth_child_xxx/index.html -> ROOT/children/rebirth_child_xxx/index.html
                
                # However, Cloudflare Pages usually maps the root of the repo to the site root.
                # Assuming the repo root is 'rebirth_project', and 'rebirth_parent' contents are at root?
                # WAIT. The deployment structure is crucial here.
                # If the user deploys the 'rebirth_project' folder, then:
                #   rebirth_project/rebirth_parent/index.html -> site.com/rebirth_parent/index.html ??
                #   No, usually users deploy 'rebirth_parent' as root? 
                # Let's check previous conversations or file structure logic.
                
                # Re-reading: "The user has 1 active workspaces... /Users/jono/Desktop/rebirth_project"
                # And earlier scripts copied children TO rebirth_parent? No, wait.
                # Let's assume the standard deployment:
                # The 'rebirth_parent' folder likely acts as the main site root, but 'children' are siblings.
                # This suggests the deployment might be confusing if not careful.
                # BUT, existing links are like <a href="../children/rebirth_child_typing/index.html">
                # This implies 'rebirth_parent' is a folder, 'children' is a sibling folder.
                # So the SITE ROOT on Cloudflare is likely the 'rebirth_project' directory itself.
                # So URL for rebirth_parent/index.html is BASE_URL + /rebirth_parent/index.html
                
                # Let's standardise URLs based on file path relative to PROJECT_ROOT.
                
                url_path = rel_path.replace(os.sep, "/")
                if url_path.startswith("./"):
                    url_path = url_path[2:]
                
                final_url = f"{BASE_URL}/{url_path}"
                
                # Determine priority
                priority = PRIORITY_ARTICLE
                if file == "index.html":
                    if is_parent and "rebirth_parent" in root:
                        priority = PRIORITY_HOME
                    elif "rebirth_child_" in root:
                        priority = PRIORITY_CHILD_HOME
                elif "category" in file:
                    priority = PRIORITY_CATEGORY
                
                lastmod = get_lastmod(full_path)
                
                pages.append({
                    "url": final_url,
                    "lastmod": lastmod,
                    "priority": priority
                })

# Process Parent
process_directory(os.path.join(PROJECT_ROOT, "rebirth_parent"), "rebirth_parent", is_parent=True)

# Process Children
children_dir = os.path.join(PROJECT_ROOT, "children")
if os.path.exists(children_dir):
    # Only process known child directories to avoid junk
    known_children = [
        "rebirth_child_typing", "rebirth_child_health", "rebirth_child_english",
        "rebirth_child_novel", "rebirth_child_manga", "rebirth_child_youtube",
        "rebirth_child_reading"
    ]
    for child in known_children:
        process_directory(os.path.join(children_dir, child), f"children/{child}")

# Generate XML
xml_content = sitemap_template_start
for page in pages:
    xml_content += url_entry_template.format(
        url=page["url"],
        lastmod=page["lastmod"],
        priority=page["priority"]
    )
xml_content += sitemap_template_end

# Write to rebirth_parent (assuming this is where the main index is, or maybe root?)
# Actually, sitemap usually goes to the ROOT of the domain.
# If deployment root is 'rebirth_project', it should go there.
# But let's put it in 'rebirth_project' root AND 'rebirth_parent' to be safe?
# Let's put it in PROJECT_ROOT.
target_file = os.path.join(PROJECT_ROOT, "sitemap.xml")

with open(target_file, "w", encoding="utf-8") as f:
    f.write(xml_content)

print(f"Sitemap generated at {target_file} with {len(pages)} URLs.")
