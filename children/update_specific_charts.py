
import os
import re

# Logic Definitions base on User Request (Step 66)
site_configs = {
    'rebirth_child_health': {
        'phase_title': 'Current Body Stats',
        'progress_percent': '5',
        'milestones': ['Start', 'Standard BMI', 'Body Fat 15%', 'Ideal Body'],
        'chart1_title': 'Weight & Body Fat',
        'chart1_labels': "['Start', 'Now', 'Goal']", # Simplified time axis
        'chart1_datasets': """
            [{
                label: 'Weight (kg)',
                data: [75.0, 74.5, 65.0],
                borderColor: '#15803d',
                backgroundColor: 'rgba(21, 128, 61, 0.1)',
                yAxisID: 'y'
            }, {
                label: 'Body Fat (%)',
                data: [25.0, 24.5, 15.0],
                borderColor: '#86efac',
                backgroundColor: 'rgba(134, 239, 172, 0.1)',
                yAxisID: 'y1'
            }]
        """,
        'chart2_title': 'Lifiting Max (kg)',
        'chart2_labels': "['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']", 
        'chart2_datasets': """
             [{
                label: 'Bench Press',
                data: [40, 42.5, 45, 47.5, 50, 50],
                borderColor: '#ef4444',
                tension: 0.3
            }, {
                label: 'Squat',
                data: [60, 65, 70, 75, 80, 80],
                borderColor: '#3b82f6',
                tension: 0.3
            }, {
                label: 'Deadlift',
                data: [70, 75, 80, 90, 100, 100],
                borderColor: '#eab308',
                tension: 0.3
            }]
        """
    },
    'rebirth_child_novel': {
        'phase_title': 'Phase 1: 100本ノック (Quantity Phase)',
        'progress_percent': '1',
        'milestones': ['10 Works', '30 Works', '50 Works', '100 Works'],
        'chart1_title': 'Works Completed',
        'chart1_labels': "['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']",
        'chart1_datasets': """[{
            label: 'Total Works',
            data: [0, 1, 2, 3, 4, 5],
            borderColor: '#78350f',
            backgroundColor: 'rgba(120, 53, 15, 0.1)',
            fill: true
        }]""",
        'chart2_title': 'Award / Revenue',
        'chart2_labels': "['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']",
        'chart2_datasets': """[{
             label: 'Revenue (JPY)',
             data: [0, 0, 0, 0, 0, 0],
             borderColor: '#fbbf24',
             backgroundColor: 'rgba(251, 191, 36, 0.1)',
        }]"""
    },
    'rebirth_child_manga': {
        'phase_title': 'Phase 1: 100本ノック (Quantity Phase)',
        'progress_percent': '1',
        'milestones': ['10 Works', '30 Works', '50 Works', '100 Works'],
        'chart1_title': 'Works Completed',
        'chart1_labels': "['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']",
        'chart1_datasets': """[{
            label: 'Total Works',
            data: [0, 1, 2, 3, 4, 5],
            borderColor: '#000000',
            backgroundColor: 'rgba(0, 0, 0, 0.1)',
            fill: true
        }]""",
        'chart2_title': 'Award / Revenue',
        'chart2_labels': "['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']",
        'chart2_datasets': """[{
             label: 'Revenue (JPY)',
             data: [0, 0, 0, 0, 0, 0],
             borderColor: '#fbbf24',
             backgroundColor: 'rgba(251, 191, 36, 0.1)',
        }]"""
    },
    'rebirth_child_reading': {
        'phase_title': 'Progress: 10 Masterpieces',
        'progress_percent': '10',
        'milestones': ['Book 1', 'Book 3', 'Book 7', 'Book 10'],
        'chart1_title': 'Books Finished',
        'chart1_labels': "['Start', 'Now', 'Goal']",
        'chart1_datasets': """[{
            label: 'Books Count',
            data: [0, 1, 10],
            borderColor: '#4338ca',
            backgroundColor: 'rgba(67, 56, 202, 0.1)',
            fill: true,
            stepped: true
        }]""",
        'chart2_title': 'Current Book Progress (Page)',
        'chart2_labels': "['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']",
        'chart2_datasets': """[{
             label: 'Page Number',
             data: [0, 20, 45, 80, 100],
             borderColor: '#a5b4fc',
             fill: true
        }]"""
    },
    'rebirth_child_youtube': {
        'phase_title': 'Monetization Progress',
        'progress_percent': '0',
        'milestones': ['Setup', 'Monetization', 'Revenue', 'Living Income'],
        'chart1_title': 'Monetization Requirements',
        'chart1_labels': "['Start', 'Now', 'Goal']",
        'chart1_datasets': """
            [{
                label: 'Subscribers (Goal: 1000)',
                data: [0, 12, 1000],
                borderColor: '#ef4444',
                yAxisID: 'y'
            }, {
                label: 'Watch Hours (Goal: 4000)',
                data: [0, 5, 4000],
                borderColor: '#3b82f6',
                yAxisID: 'y1'
            }]
        """,
        'chart2_title': 'Revenue (JPY)',
        'chart2_labels': "['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']",
        'chart2_datasets': """[{
             label: 'Monthly Revenue',
             data: [0, 0, 0, 0, 0, 0],
             borderColor: '#fbbf24',
             backgroundColor: 'rgba(251, 191, 36, 0.2)',
             fill: true
        }]"""
    }
}

base_dir = "/Users/jono/Desktop/rebirth_project/children"

def apply_chart_config(view_data_path, config):
    if not os.path.exists(view_data_path):
        return

    with open(view_data_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update basic milestones & progress bar (Same as before)
    content = re.sub(r'Phase 1:.*?<\/span>', f'{config["phase_title"]}</span>', content)
    content = re.sub(r'>\d+%<\/span>', f'>{config["progress_percent"]}%</span>', content)
    content = re.sub(r'width: \d+%; height: 100%', f'width: {config["progress_percent"]}%; height: 100%', content)
    
    ms = config['milestones']
    # Removing original Milestones hardcoding for cleanliness if needed, but for now replace known placeholders
    # The previous script might have overwritten Level 1 etc with something else.
    # To be safe, we might want to rebuild the milestone HTML, but simple replace usually works if run once.
    # Note: If the file was already customized, 'Level 1' might be gone.
    # So this replace might fail if run multiple times. 
    # But since we are tweaking the logic, assuming we start from a somewhat known state or flexible regex.
    
    # 2. Update Charts logic
    # We will replace the entire <script> block containing chart logic to be safe.
    
    # Construct new script content
    new_script = f"""
        <script>
            // Data Configured via Python Script
            
            // Chart 1: {config['chart1_title']}
            const ctx1 = document.getElementById('wpmChart').getContext('2d');
            new Chart(ctx1, {{
                type: 'line',
                data: {{
                    labels: {config['chart1_labels']},
                    datasets: {config['chart1_datasets']}
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        title: {{ display: true, text: '{config['chart1_title']}' }}
                    }},
                    scales: {{
                        y: {{ beginAtZero: true, display: true, position: 'left' }},
                        // Add y1 for potential dual axis usage (Health, YouTube)
                        y1: {{ beginAtZero: true, display: false, position: 'right', grid: {{ drawOnChartArea: false }} }}
                    }}
                }}
            }});

            // Chart 2: {config['chart2_title']}
            const ctx2 = document.getElementById('accuracyChart').getContext('2d');
            new Chart(ctx2, {{
                type: 'line',
                data: {{
                    labels: {config['chart2_labels']},
                    datasets: {config['chart2_datasets']}
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        title: {{ display: true, text: '{config['chart2_title']}' }}
                    }},
                    scales: {{
                        y: {{ beginAtZero: true }}
                    }}
                }}
            }});
            
            // Activate Dual Axis if needed (Health, YouTube)
            // Validating logic: check if datasets have yAxisID
            if (JSON.stringify({config['chart1_datasets']}).includes('y1')) {{
                Chart.getChart("wpmChart").options.scales.y1.display = true;
                Chart.getChart("wpmChart").update();
            }}
        </script>
    """
    
    # Regex to find the script block
    # Matches <script>...new Chart...</script>
    # We need to be careful not to match the chart.js loader script
    
    script_pattern = re.compile(r'<script>\s*// Dummy Data.*?<\/script>', re.DOTALL)
    
    # If the previous script structure is different (because we ran setup_all_view_data.py), 
    # we need a more robust pattern. The previous script had comments like // WPM Data
    
    # Let's try to match from `const labels =` to the end of script
    script_pattern_v2 = re.compile(r'<script>\s*.*?new Chart.*?<\/script>', re.DOTALL)

    if script_pattern_v2.search(content):
        content = script_pattern_v2.sub(new_script, content)
    else:
        # If we can't find it, append it? No, that would break.
        print(f"Warning: Could not replace script in {view_data_path}")
        return

    with open(view_data_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated charts for: {os.path.basename(os.path.dirname(view_data_path))}")

def main():
    for dirname, config in site_configs.items():
        dirpath = os.path.join(base_dir, dirname)
        apply_chart_config(os.path.join(dirpath, "view_data.html"), config)

if __name__ == "__main__":
    main()
