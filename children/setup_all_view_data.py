
import os
import re

# Logic Definitions for each site
site_configs = {
    'rebirth_child_english': {
        'phase_title': 'Phase 1: 基礎固め (Foundation)',
        'progress_percent': '10',
        'milestones': ['Start', 'TOEIC 600', 'TOEIC 800', 'Fluent'],
        'chart1_title': 'TOEIC Score',
        'chart1_label': 'Score',
        'chart1_data': '[400, 420, 450, 480, 500, 520]',
        'chart2_title': 'Words Learned',
        'chart2_label': 'Words',
        'chart2_data': '[100, 500, 1000, 1500, 2000, 2500]',
        'chart_color1': '#b91c1c', # Red
        'chart_color2': '#fca5a5'
    },
    'rebirth_child_health': {
        'phase_title': 'Phase 1: 習慣化 (Habit Formation)',
        'progress_percent': '5',
        'milestones': ['Start', '-5kg', '-10kg', 'Ideal Body'],
        'chart1_title': 'Body Weight (kg)',
        'chart1_label': 'Weight',
        'chart1_data': '[75, 74.5, 74, 73.8, 73.5, 73.2]',
        'chart2_title': 'Body Fat (%)',
        'chart2_label': 'Fat %',
        'chart2_data': '[25, 24.8, 24.5, 24.2, 24.0, 23.8]',
        'chart_color1': '#15803d', # Green
        'chart_color2': '#86efac'
    },
    'rebirth_child_novel': {
        'phase_title': 'Phase 1: 構想・執筆 (Conception)',
        'progress_percent': '1',
        'milestones': ['Idea', 'Plot', 'Draft', 'Finish'],
        'chart1_title': 'Total Characters Written',
        'chart1_label': 'Characters',
        'chart1_data': '[0, 2000, 5000, 10000, 15000, 20000]',
        'chart2_title': 'Writing Time (min)',
        'chart2_label': 'Minutes',
        'chart2_data': '[0, 30, 60, 90, 120, 150]',
        'chart_color1': '#78350f', # Brown
        'chart_color2': '#fdba74'
    },
    'rebirth_child_manga': {
        'phase_title': 'Phase 1: 基礎練習 (Basic Practice)',
        'progress_percent': '1',
        'milestones': ['Sketch', '4-Koma', 'Short', 'Series'],
        'chart1_title': 'Practice Hours',
        'chart1_label': 'Hours',
        'chart1_data': '[0, 2, 5, 8, 12, 15]',
        'chart2_title': 'Works Completed',
        'chart2_label': 'Count',
        'chart2_data': '[0, 1, 1, 2, 2, 3]',
        'chart_color1': '#000000', # Black
        'chart_color2': '#94a3b8'
    },
    'rebirth_child_reading': {
        'phase_title': 'Book 1: 読書中 (Reading)',
        'progress_percent': '2',
        'milestones': ['Book 1', 'Book 3', 'Book 5', 'Book 10'],
        'chart1_title': 'Pages Read',
        'chart1_label': 'Pages',
        'chart1_data': '[0, 50, 120, 200, 280, 350]',
        'chart2_title': 'Books Finished',
        'chart2_label': 'Books',
        'chart2_data': '[0, 0, 0, 1, 1, 1]',
        'chart_color1': '#4338ca', # Indigo
        'chart_color2': '#a5b4fc'
    },
    'rebirth_child_youtube': {
        'phase_title': 'Phase 1: 準備 (Setup)',
        'progress_percent': '0',
        'milestones': ['Setup', '10 Subs', '100 Subs', '1000 Subs'],
        'chart1_title': 'Subscribers',
        'chart1_label': 'Subs',
        'chart1_data': '[0, 0, 1, 2, 3, 5]',
        'chart2_title': 'Watch Time (Hours)',
        'chart2_label': 'Hours',
        'chart2_data': '[0, 0, 0.1, 0.5, 1.0, 2.5]',
        'chart_color1': '#ef4444', # Red
        'chart_color2': '#fca5a5'
    }
}

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def update_index_link(index_path):
    """Updates the View Data dashboard link to point to view_data.html"""
    if not os.path.exists(index_path):
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find <a href="#" class="btn-primary">View Data</a> inside dashboard section
    # Note: Previous tool might have already updated some
    # We look for href="#" specifically associated with View Data
    
    pattern = r'href="#"\s+class="btn-primary"\s*>\s*View Data'
    replacement = 'href="view_data.html" class="btn-primary">View Data'
    
    new_content, count = re.subn(pattern, replacement, content)
    
    if count > 0:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated index link for: {os.path.basename(os.path.dirname(index_path))}")
    else:
        print(f"Index link already correct or not found for: {os.path.basename(os.path.dirname(index_path))}")

def customize_view_data(view_data_path, config):
    """Replaces the content of view_data.html with site specific configs"""
    if not os.path.exists(view_data_path):
        return

    with open(view_data_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Phase Title
    # Pattern: Phase 1: 初級1（人差し指のみ）クリア済
    content = re.sub(r'Phase 1:.*?<\/span>', f'{config["phase_title"]}</span>', content)

    # 2. Update Percentage (Big Number)
    # Pattern: >25%</span>
    content = re.sub(r'>\d+%<\/span>', f'>{config["progress_percent"]}%</span>', content)

    # 3. Update Progress Bar Width
    # Pattern: width: 25%
    content = re.sub(r'width: \d+%; height: 100%', f'width: {config["progress_percent"]}%; height: 100%', content)

    # 4. Update Milestones text
    # Level 1, Level 2, Level 3, Master
    ms = config['milestones']
    content = content.replace('Level 1', ms[0])
    content = content.replace('Level 2', ms[1])
    content = content.replace('Level 3', ms[2])
    content = content.replace('Master', ms[3])

    # 5. Update Charts
    # Regex to replace Chart Data blocks
    
    # WPM Chart Title
    content = content.replace("'WPM Growth'", f"'{config['chart1_title']}'")
    content = content.replace("'WPM (Words Per Minute)'", f"'{config['chart1_label']}'")
    
    # WPM Data Array
    # data: [15, 18, 24, 28, 35, 42.5],
    content = re.sub(r'data: \[.*?\],', f'data: {config["chart1_data"]},', content, count=1)
    
    # Accuracy Chart Title
    content = content.replace("'Accuracy Rate'", f"'{config['chart2_title']}'")
    content = content.replace("'Accuracy (%)'", f"'{config['chart2_label']}'")
    
    # Accuracy Data Array (This is the second occurrence of data: [...])
    # However, re.sub finds from start. We need to be careful.
    # Approach: Split content by "Accuracy Data" comment?
    
    parts = content.split('// Accuracy Data')
    if len(parts) > 1:
        # Update the second part
        parts[1] = re.sub(r'data: \[.*?\],', f'data: {config["chart2_data"]},', parts[1], count=1)
        content = parts[0] + '// Accuracy Data' + parts[1]

    # Colors (Optional, simple replace for now)
    # Replace blue with config color 1
    content = content.replace('#3b82f6', config['chart_color1'])
    
    with open(view_data_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Customized view_data for: {os.path.basename(os.path.dirname(view_data_path))}")

def main():
    for dirname, config in site_configs.items():
        dirpath = os.path.join(base_dir, dirname)
        
        # 1. Update Index Button
        update_index_link(os.path.join(dirpath, "index.html"))
        
        # 2. Update View Data Content
        customize_view_data(os.path.join(dirpath, "view_data.html"), config)

if __name__ == "__main__":
    main()
