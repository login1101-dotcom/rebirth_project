import os
import re

directories = {
    'rebirth_child_typing': 'ブラインドタッチを習得する',
    'rebirth_child_health': '見た目のいい健康な体を手にいれる',
    'rebirth_child_english': '使える英語を身につける',
    'rebirth_child_novel': '小説家やエッセイストになる',
    'rebirth_child_manga': '漫画家になる',
    'rebirth_child_youtube': '動画作家として生活できる収益を得る',
    'rebirth_child_reading': '難しい名著を理解する'
}

base_path = '/Users/jono/Desktop/rebirth_project/children'

for dirname, goal_text in directories.items():
    dir_path = os.path.join(base_path, dirname)
    if not os.path.exists(dir_path):
        continue

    print(f"Checking directory: {dirname} -> {goal_text}")

    # Regex to find the inserted span
    # We look for the span with the goal text, followed by possible whitespace and the SAME span again
    # We must match the attributes carefully or use a looser match
    
    # Exact span text we constructed:
    # <span style="font-size: 0.8rem; color: #64748b; margin-left: 10px; font-weight: normal;">{goal_text}</span>
    
    # We'll construct a regex that matches this string appearing twice consecutively
    # Escaping regex special chars in goal_text if any (none in this case, but good practice)
    
    span_str = f'<span style="font-size: 0.8rem; color: #64748b; margin-left: 10px; font-weight: normal;">{goal_text}</span>'
    
    # Simple string replacement for duplication
    # We look for "SPAN\s*SPAN"
    escaped_span = re.escape(span_str)
    dup_pattern = re.compile(f'({escaped_span})(\\s*)({escaped_span})', re.DOTALL)

    for filename in os.listdir(dir_path):
        if filename.endswith('.html'):
            file_path = os.path.join(dir_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use regex to find duplicates
            if dup_pattern.search(content):
                print(f"  Duplicate found in: {filename}. Fixing...")
                # Replace with single instance
                new_content = dup_pattern.sub(r'\1', content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            else:
               pass
               # print(f"  OK: {filename}")
