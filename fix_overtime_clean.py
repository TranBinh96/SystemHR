#!/usr/bin/env python3
"""
Script to fix overtime.html by removing duplicate JavaScript code
"""

def fix_overtime_html():
    with open('templates/overtime.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the first </script> tag position
    first_script_end = content.find('</script>')
    
    if first_script_end == -1:
        print("No </script> tag found!")
        return
    
    # Find the second </script> tag (if exists)
    second_script_end = content.find('</script>', first_script_end + 9)
    
    if second_script_end == -1:
        print("Only one </script> tag found, file might be OK")
        return
    
    # Keep everything up to and including the second </script>
    # Then add </body></html>
    fixed_content = content[:second_script_end + 9] + '\n</body>\n</html>\n'
    
    # Write back
    with open('templates/overtime.html', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Fixed overtime.html successfully!")
    print(f"Original length: {len(content)} chars")
    print(f"Fixed length: {len(fixed_content)} chars")

if __name__ == '__main__':
    fix_overtime_html()
