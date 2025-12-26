
import os
import re

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"

def sync_all_colors_robustly(style_path):
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extract all category colors from :root
    # Pattern: --color-([a-z0-9_-]+):\s*(#[a-fA-F0-9]+);
    colors = re.findall(r'--color-([a-z0-9_-]+):\s*(#[a-fA-F0-9]+);', content)
    
    if not colors:
        print(f"  No colors found in {style_path}")
        return

    # 2. Build the unified color block
    color_logic_block = "\n/* --- Dynamic Category Color Sync --- */\n"
    
    for slug, hex_val in colors:
        light_bg = hex_to_rgba(hex_val, 0.08)
        med_bg = hex_to_rgba(hex_val, 0.15)
        
        # Text and Nav
        color_logic_block += f".text-{slug}, .nav-{slug} {{ color: var(--color-{slug}) !important; }}\n"
        
        # Backgrounds (used for card thumbnails)
        # Note: we use !important to override any legacy hardcoded gradients
        color_logic_block += f".bg-{slug} {{\n    background: linear-gradient(135deg, {light_bg}, {med_bg}) !important;\n    color: var(--color-{slug}) !important;\n}}\n"
        
        # Single Post Header (Header is white, Title is colored)
        color_logic_block += f".single-post header.bg-{slug} h1 {{ color: var(--color-{slug}) !important; }}\n"
        # Breadcrumb border/accent
        color_logic_block += f".single-post header.bg-{slug} {{ border-top: 3px solid var(--color-{slug}) !important; }}\n"
    
    # 3. Clean up old category blocks to avoid conflicts
    # This is tricky, but we'll try to remove common patterns
    content = re.sub(r'/\* Category (Text|Background|Title|Nav).*?\*/.*?(?=\n\n|\*/)', '', content, flags=re.DOTALL)
    # Remove previous "Dynamic Category Color Sync" if exists
    content = re.sub(r'/\* --- Dynamic Category Color Sync --- \*/.*$', '', content, flags=re.DOTALL)
    
    # Add the new block at the end
    content = content.strip() + "\n" + color_logic_block

    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    for item in os.listdir(base_dir):
        site_path = os.path.join(base_dir, item)
        if os.path.isdir(site_path):
            style_p = os.path.join(site_path, "style.css")
            if os.path.exists(style_p):
                print(f"Syncing colors for {item}...")
                sync_all_colors_robustly(style_p)
location = "rebirth_project/children"
