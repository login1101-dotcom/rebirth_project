
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

# We need to make sure 'bg-xxx' classes in style.css actually provide a SOFT background color suitable for black text,
# OR we need to use a specific utility like 'bg-xxx-soft'.
# Upon checking previous style.css views, 'bg-daily' etc were typically gradients or solid colors for THUMBNAILS.
# e.g. .bg-daily { background: linear-gradient(...); color: var(--color-daily); }
# If this is applied to the Header, it might look okay IF the text color is handled.
# But user says "Why is it red?".

# Let's check style.css definitions and force them to be soft backgrounds if they aren't already,
# or ensure the Article Header uses the SOFT version.

# Many existing css files had:
# .bg-daily { background: linear-gradient(to right, #eff6ff, #dbeafe) !important; color: var(--color-daily); }
# This is a light blue gradient. If the text is var(--color-daily) (Blue), it should look like Blue Text on Light Blue BG.
# This matches the user's "good" example.

# However, if it looks wrong (e.g. Red background on Analysis), let's verify Typing Lab's Analysis color.
# Typing Lab Analysis: --color-analysis: #ef4444; (Red)
# .bg-analysis: background: linear-gradient(to right, #fef2f2, #fee2e2) !important; (Light Red)
# So it SHOULD be Light Red background with Red text.

# If the user sees "Red? Why red?", maybe they expected Blue or Grey because it's a Review?
# The card says "Analysis". Analysis COLOR is Red in Typing Lab.
# So "Why Red?" -> User probably thinks "Tools" or "Review" should be grey/blue, but it was tagged Analysis.
# Or maybe the generated HTML has the WRONG class.

# Let's start by fixing the generated HTML files to ensure they have the CORRECT class from the card.
# I will re-scan index.html to find the correct class for each title and force-update the article_x.html header class.

def fix_article_header_classes(current_dir):
    index_path = os.path.join(current_dir, "index.html")
    if not os.path.exists(index_path): return

    with open(index_path, 'r', encoding='utf-8') as f:
        idx_content = f.read()
    
    # 1. Map Title -> Category Class
    # We find cards, extract title and category class.
    # Regex for card block
    cards = re.findall(r'(<article class="article-card".*?</article>)', idx_content, re.DOTALL)
    
    title_to_class = {}
    
    for card in cards:
        # Extract title
        t_m = re.search(r'<h3 class="article-title">\s*(.*?)\s*</h3>', card, re.DOTALL)
        if t_m:
            title = t_m.group(1).strip()
            # Extract category class (text-xxx)
            # <a href="..." class="cat text-analysis">Analysis</a>
            c_m = re.search(r'class="cat (text-[a-z]+)"', card)
            if c_m:
                # We want the corresponding bg class. text-analysis -> bg-analysis
                text_class = c_m.group(1)
                bg_class = text_class.replace('text-', 'bg-')
                title_to_class[title] = bg_class
            else:
                # Try to guess? Or default
                pass

    # 2. Iterate all article_*.html files and update their header class matches the title
    for fname in os.listdir(current_dir):
        if fname.startswith("article") and fname.endswith(".html"):
            fpath = os.path.join(current_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the title in this file to look up correct class
            # Title is in <h1>...</h1> or <title>...
            t_match = re.search(r'<h1>\s*(.*?)\s*</h1>', content, re.DOTALL)
            if not t_match: continue
            
            this_title = t_match.group(1).strip()
            
            if this_title in title_to_class:
                correct_bg = title_to_class[this_title]
                
                # Update the header class
                # Look for <header class="bg-styled ..."> OR <header>
                # We want to force it to: <header class="bg-styled {correct_bg}">
                
                # Regex replace opening header tag
                # We look for <header ...> that is NOT the main site header.
                # The main site header usually has <div class="container header-inner"> inside.
                # The article header is usually inside <main ... single-post>
                
                # Safer: Replace <header class="bg-styled .*?">
                if 'class="bg-styled' in content:
                    content = re.sub(r'class="bg-styled [^"]*"', f'class="bg-styled {correct_bg}"', content)
                
                # If it doesn't have bg-styled yet (missed by previous scripts)
                elif '<header>' in content:
                    # We need to distinguish site header from article header.
                    # Article header follows <main class="content-area single-post">
                    # Let's replace only the first header AFTER <main...single-post>
                    
                    # Find split point
                    parts = re.split(r'(<main class="content-area single-post">)', content)
                    if len(parts) > 1:
                        # parts[0] is before main, parts[1] is the tag, parts[2] is body
                        # In parts[2], replace first <header>
                        parts[2] = parts[2].replace('<header>', f'<header class="bg-styled {correct_bg}">', 1)
                        content = "".join(parts)
                
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {fname} in {os.path.basename(current_dir)} to {correct_bg}")

def main():
    if not os.path.exists(base_dir): return
    for item in os.listdir(base_dir):
        full = os.path.join(base_dir, item)
        if os.path.isdir(full):
            fix_article_header_classes(full)

if __name__ == "__main__":
    main()
