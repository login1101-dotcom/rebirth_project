import os

ROOT_DIR = "/Users/jono/.gemini/antigravity/scratch/Rebirth_Main_Work"
CHILDREN_DIR = os.path.join(ROOT_DIR, "children")

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The broken pattern is a prematurely closed script tag followed by leaked JS code
    # <script> ... </script> display: true, ...
    # We want to remove the premature </script> tag if followed by known leaked code pattern
    # Actually, it looks like a mess. 
    # In the view_data.html of novel:
    # Line 226: </script> display: true,
    # Line 277: </script>
    
    # We need to remove the content from "display: true," down to "});" AND the first </script>
    # Basically the JS structure is broken.
    
    # The chart config seems to be:
    # options: { ... scales: { ... y1: { type: 'linear', display: true, position: 'right', min: 0, grid: { display: false }, ticks: { stepSize: 1, color: '#d97706' } } } } });
    
    # The file has:
    # 225:             }
    # 226:         </script> display: true,
    
    # It seems like I accidentally pasted some partial JS code OUTSIDE the script tag in a previous massive edit?
    # Or strict replacement failed.
    
    # Let's look at the structure.
    # We should just look for `</script> display: true,` and remove everything until the next `<script>` or just clean it up.
    
    if "display: true," in content and "</script> display: true," in content:
        # This specific breakage
        print(f"Fixing broken JS in {file_path}")
        
        # We need to reconstruct the Chart JS properly or just remove the leaked text.
        # The leaked text is orphan code.
        # It looks like the Chart definition in the script block ABOVE line 226 is actually CLOSED properly?
        # Let's check line 180: });
        # So the chart is closed.
        # The code starting from display: true... is effectively garbage that should be deleted.
        # And the extra function showCalendar definition (lines 237-276) duplicates or conflicts with the one inside the script?
        # No, line 222 showChart() is inside the first script block.
        # Line 182 showCalendar is also inside.
        
        # So lines 226-277 contain:
        # 1. Leaked garbage text (display: true...)
        # 2. A DUPLICATE definition of showCalendar?
        # Let's check.
        # Line 182: function showCalendar(monthName, monthIndex) { ... }
        # Line 237: function showCalendar(monthName, monthIndex) { ... }
        
        # Yes, it's a duplicate.
        # So we should delete everything from line 226 (inclusive) to 277 (inclusive).
        # EXCEPT we need to keep the closing </script> for the valid script block?
        # No, line 226 starts with </script>. So that closes the valid block.
        # So we should delete everything AFTER `</script>` on line 226 up to line 277 `</script>`?
        # Wait, if we delete line 277 `</script>`, we have unmatched tags if we are not careful.
        
        # Structure:
        # <script>
        # ... valid code ...
        # </script> (Line 226)
        # GAP: garbage code + duplicate code
        # </script> (Line 277)
        
        # So we just need to delete the GAP and the second </script>.
        
        # Identify the start of the garbage
        parts = content.split('</script> display: true,')
        if len(parts) > 1:
            valid_part = parts[0] + '</script>'
            remainder = parts[1]
            
            # Now find the end of the garbage
            # It ends with </script>
            
            remainder_parts = remainder.split('</script>')
            if len(remainder_parts) > 1:
                # The first part of remainder is the garbage to remove
                # The rest is valid HTML following it (sidebar etc)
                
                clean_content = valid_part + remainder_parts[1]
                # Wait, remainder_parts[1] starts after the SECOND </script>.
                # So we effectively removed the block.
                
                # However, confirm that `remainder` actually contains the duplicate code.
                # Yes, looking at the file view, it does.
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(clean_content)
                return True

    return False

for root, dirs, files in os.walk(CHILDREN_DIR):
    for f in files:
        if f == "view_data.html":
            process_file(os.path.join(root, f))
