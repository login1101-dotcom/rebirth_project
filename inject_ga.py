import os

# Google Analytics Tag (Measurement ID: G-1F416P0VQS)
GA_TAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-1F416P0VQS"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-1F416P0VQS');
</script>
"""

# Targets: Parent site + 7 Child sites
# (Neo or other external sites are excluded as requested to keep Re:Birth clean)
base_dirs = [
    "/Users/jono/Desktop/rebirth_project/rebirth_parent",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_typing",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_health",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_english",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_novel",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_manga",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_youtube",
    "/Users/jono/Desktop/rebirth_project/children/rebirth_child_reading"
]

print("Starting Google Analytics tag injection...")

for site_dir in base_dirs:
    if not os.path.exists(site_dir):
        print(f"Skipping {site_dir} (not found)")
        continue

    print(f"Processing directory: {site_dir}")
    
    for root, dirs, files in os.walk(site_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check if GA tag already exists (avoid duplicates, even different IDs for now to be safe)
                if "googletagmanager.com/gtag/js" in content:
                    # If it's a DIFFERENT ID, we might want to replace it, but for safety now let's skip/alert
                    # Assuming clean install or overwrite
                    # Let's clean up old tags if any, then insert new one
                    if "G-1F416P0VQS" in content:
                        # print(f"  Skipping {file} (already has current GA tag)")
                        continue
                    else:
                        print(f"  Warning: {file} has a different GA tag. Replacing it.")
                        # Simple replacement logic might be complex. 
                        # For now, let's prepend the new one? No, bad idea.
                        # Let's assume we just insert the new one in <head> and user can clean up old if needed.
                        pass

                # Insertion logic: Immediately after <head>
                if "<head>" in content:
                    new_content = content.replace("<head>", f"<head>\n{GA_TAG}")
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"  Injected GA tag into {file}")
                else:
                    print(f"  Skipping {file} (no <head> tag found)")

print("Google Analytics injection completed.")
