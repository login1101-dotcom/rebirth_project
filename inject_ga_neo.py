import os

# Google Analytics Tag for Typing Master Neo (ID: G-QCTM9NEWRK)
GA_TAG_NEO = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QCTM9NEWRK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-QCTM9NEWRK');
</script>
"""

# Target Directory: Typing Master Neo
target_dir = "/Users/jono/Desktop/rebirth_project/typingmaster_github_clone"

print("Starting Google Analytics tag injection for Typing Master Neo...")

if not os.path.exists(target_dir):
    print(f"Error: Directory not found at {target_dir}")
else:
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check for existing GA tags to avoid duplicates
                if "googletagmanager.com/gtag/js" in content:
                    if "G-QCTM9NEWRK" in content:
                        print(f"  Skipping {file} (already has current GA tag)")
                        continue
                    else:
                        print(f"  Warning: {file} has a different GA tag. Skipping to avoid conflict.")
                        continue

                # Injection
                if "<head>" in content:
                    new_content = content.replace("<head>", f"<head>\n{GA_TAG_NEO}")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"  Injected GA tag into {file}")
                else:
                    print(f"  Skipping {file} (no <head> tag found)")

print("Done.")
