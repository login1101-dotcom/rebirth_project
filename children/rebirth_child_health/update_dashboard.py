import os
import re
from datetime import datetime

def get_status_report():
    dir_path = '/Users/jono/Desktop/rebirth_project/children/rebirth_child_health'
    today = datetime(2025, 12, 25) 
    
    categories = {
        '食事': 'diet',
        '筋トレ': 'muscle',
        '睡眠': 'sleep'
    }
    
    latest_dates = {cat: None for cat in categories}

    for filename in os.listdir(dir_path):
        if filename.endswith('.html') and filename.startswith('post_'):
            with open(os.path.join(dir_path, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                
                date_match = re.search(r'class="date">(\d{4}\.\d{2}\.\d{2})</span>', content)
                if date_match:
                    date_str = date_match.group(1).replace('.', '-')
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    
                    for cat_kana, cat_key in categories.items():
                        if f'text-{cat_key}' in content:
                            if latest_dates[cat_kana] is None or date_obj > latest_dates[cat_kana]:
                                latest_dates[cat_kana] = date_obj

    def calc_status(cat_name):
        d = latest_dates[cat_name]
        if not d: return 'x'
        diff = (today - d).days
        if diff <= 1: return '◎'
        if diff <= 3: return '◯'
        if diff <= 7: return '△'
        return 'x'

    status_map = {cat: calc_status(cat) for cat in categories}
    return status_map

def update_index():
    index_path = '/Users/jono/Desktop/rebirth_project/children/rebirth_child_health/index.html'
    status_map = get_status_report()
    
    # Emoji conversion map
    emoji_map = {
        '◎': '😆',
        '◯': '😊',
        '△': '😐',
        'x': '😫'
    }
    
    def get_stat_content(label, value, subtext=None, is_status=False):
        if is_status:
            emoji = emoji_map.get(value, '❓')
            val_content = f'<span class="status-badge status-{value}">{emoji}</span>'
        else:
            val_content = value
            
        delta_content = f'<div class="stat-delta">{subtext}</div>' if subtext else '<div class="stat-delta" style="visibility:hidden; height:1rem;">placeholder</div>'
        
        return f"""
                        <div class="stat-label">{label}</div>
                        <div class="stat-value">{val_content}</div>
                        {delta_content}"""

    new_dashboard_html = f"""            <section class="dashboard-card-pro">
                <div class="stats-grid-group">
                    <!-- Row 1: Group Headers -->
                    <div class="stat-header-cell" style="grid-column: span 2;">現在</div>
                    <div class="stat-header-cell">昨日</div>
                    <div class="stat-header-cell" style="grid-column: span 3;">継続率</div>

                    <!-- Row 2: Items -->
                    <div class="stat-item-premium">{get_stat_content('体重', '72.4<small>kg</small>', subtext='↓0.5kg')}</div>
                    <div class="stat-item-premium">{get_stat_content('体脂肪', '23.5<small>%</small>', subtext='↓0.2%')}</div>
                    <div class="stat-item-premium">{get_stat_content('歩数', '8,402<small>歩</small>', subtext='↑1,200歩')}</div>
                    <div class="stat-item-premium">{get_stat_content('食事', status_map['食事'], is_status=True)}</div>
                    <div class="stat-item-premium">{get_stat_content('筋トレ', status_map['筋トレ'], is_status=True)}</div>
                    <div class="stat-item-premium">{get_stat_content('睡眠', status_map['睡眠'], is_status=True)}</div>
                </div>
                <div class="stats-action">
                    <a href="view_data.html" class="btn-data-pro">データ表示</a>
                </div>
            </section>"""

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    dashboard_pattern = re.compile(r'<!-- Dashboard Widget.*?<section.*?>.*?</section>', re.DOTALL)
    content = dashboard_pattern.sub(f'<!-- Dashboard Widget: Only on Home -->\n{new_dashboard_html}', content)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_index()
    print("Dashboard updated with facial emojis for status.")
