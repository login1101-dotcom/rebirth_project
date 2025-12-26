import os
import re

CHILDREN_ROOT = "/Users/jono/Desktop/rebirth_project/children"

def update_category_pages(site_name):
    site_dir = os.path.join(CHILDREN_ROOT, site_name)
    if not os.path.exists(site_dir):
        return

    print(f"Checking {site_name}...")
    
    # Get all post files to build a database of articles
    posts = []
    for fname in os.listdir(site_dir):
        if fname.startswith("post_") and fname.endswith(".html"):
            with open(os.path.join(site_dir, fname), 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract basic info for list generation
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content)
            date_match = re.search(r'<span class="date">(.*?)</span>', content)
            cat_match = re.search(r'<span class="cat\s+([^"]+)">', content) # get classes
            cat_text_match = re.search(r'<span class="cat[^>]*>(.*?)</span>', content)
            
            # Extract excerpt (first p after h1 or in post-content?)
            # Usually we used item-excerpt in index.html, but in post file it is just <p> content.
            # Let's try to extract the first paragraph of post-content
            # <div class="post-content">\n<p...>(.*?)</p>
            excerpt_match = re.search(r'<div class="post-content">\s*<p[^>]*>(.*?)</p>', content, re.DOTALL)
            
            # Clean excerpt
            excerpt = "No description."
            if excerpt_match:
                excerpt = re.sub(r'<[^>]+>', '', excerpt_match.group(1)).strip()
                if len(excerpt) > 60: excerpt = excerpt[:60] + "..."
            
            title = title_match.group(1) if title_match else fname
            date = date_match.group(1) if date_match else "2025.01.01"
            cat_classes = cat_match.group(1) if cat_match else ""
            cat_name = cat_text_match.group(1) if cat_text_match else "Uncategorized"
            
            # Determine category link from class name if possible or heuristic
            # text-works -> category_works.html
            # text-tools -> category_tools.html
            # text-process -> category_process.html
            # text-short -> category_short.html
            # text-essay -> category_essay.html
            # text-diet -> category_diet.html
            # text-reading -> category_reading.html etc
            
            cat_slug = ""
            if "text-" in cat_classes:
                slug_part = cat_classes.split("text-")[-1].strip() # e.g. 'works'
                # handle special cases
                if slug_part == "other": slug_part = "others" # sometimes other vs others
                cat_slug = slug_part
            
            posts.append({
                "filename": fname,
                "title": title,
                "date": date,
                "cat_classes": cat_classes,
                "cat_name": cat_name,
                "excerpt": excerpt,
                "cat_slug": cat_slug
            })
            
    # Now verify/update category pages
    for fname in os.listdir(site_dir):
        if fname.startswith("category_") and fname.endswith(".html"):
            # Identify which category this page is for
            # e.g. category_works.html -> works
            page_slug = fname.replace("category_", "").replace(".html", "")
            
            # Find posts that belong to this slug
            relevant_posts = [p for p in posts if p['cat_slug'] == page_slug or (page_slug == "others" and p['cat_slug'] == "other")]
            
            # Sort valid posts by date desc or filename desc?
            relevant_posts.sort(key=lambda x: x['filename'], reverse=True) # Simple sort
            
            if not relevant_posts:
                continue
                
            print(f"  Updating {fname} with {len(relevant_posts)} posts.")
            
            # Construct HTML list
            html_list = ""
            for p in relevant_posts:
                # determine logo based on slug (simplified)
                logo = "📄"
                if "works" in p['cat_slug']: logo = "🎬"
                elif "tools" in p['cat_slug']: logo = "🛠️"
                elif "process" in p['cat_slug']: logo = "📹"
                elif "short" in p['cat_slug']: logo = "☂️" # or generic
                elif "essay" in p['cat_slug']: logo = "✒️"
                elif "diet" in p['cat_slug']: logo = "🍳"
                elif "muscle" in p['cat_slug']: logo = "💪"
                elif "sleep" in p['cat_slug']: logo = "💤"
                elif "reading" in p['cat_slug']: logo = "📚"
                elif "writing" in p['cat_slug']: logo = "✍️"
                elif "listening" in p['cat_slug']: logo = "🎧"
                elif "speaking" in p['cat_slug']: logo = "🗣️"
                elif "practice" in p['cat_slug']: logo = "🎯"
                
                html_list += f"""
                <article class="article-item">
                    <a href="{p['filename']}">
                        <div class="item-meta-group">
                            <span class="item-meta">{p['date']} • <span class="{p['cat_classes']}">{p['cat_name']}</span></span>
                            <div class="item-logo-row">
                                <span class="item-logo">{logo}</span>
                                <span class="item-click-hint {p['cat_classes']}">CLICK READ MORE →</span>
                            </div>
                        </div>
                        <div class="item-title-box">
                            <h3 class="article-title {p['cat_classes']}">{p['title']}</h3>
                            <p class="item-excerpt">{p['excerpt']}</p>
                        </div>
                    </a>
                </article>
"""
            
            # Inject into file
            with open(os.path.join(site_dir, fname), 'r', encoding='utf-8') as f:
                page_content = f.read()
            
            # Regex replace <div class="article-list">...</div>
            # Be careful to capture the closing div correctly.
            # Assuming standard indentation or just non-greedy until </div> check
            # Pattern: <div class="article-list"> ... </div>
            
            new_page_content = re.sub(
                r'(<div class="article-list">)(.*?)(</div>(\s*</main>))',
                f'\\1{html_list}</div>\\4',
                page_content,
                flags=re.DOTALL
            )
            
            # Reconstruct is slightly risky with regex on large blocks, let's use a simpler marker approach if possible?
            # Or just overwrite the block.
            # Safety check: if modification happened
            if new_page_content != page_content:
                with open(os.path.join(site_dir, fname), 'w', encoding='utf-8') as f:
                    f.write(new_page_content)
            else:
                # If regex didn't match (maybe structure diff), try finding explicit range
                pass

def main():
    sites = [
        "rebirth_child_youtube",
        "rebirth_child_novel",
        "rebirth_child_english",
        "rebirth_child_manga",
        "rebirth_child_typing"
    ]
    
    for site in sites:
        update_category_pages(site)

if __name__ == "__main__":
    main()
