#!/usr/bin/env python3
"""Find unmatched braces in overtime.html"""

with open('templates/overtime.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_script = False
brace_count = 0
line_num = 0

for i, line in enumerate(lines, 1):
    if '<script>' in line and 'src=' not in line:
        in_script = True
        print(f"Script starts at line {i}")
    
    if in_script:
        for char in line:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count < 0:
                    print(f"ERROR: Extra closing brace at line {i}")
                    print(f"Line content: {line.strip()}")
                    print(f"Brace count: {brace_count}")
    
    if '</script>' in line:
        in_script = False
        print(f"Script ends at line {i}, final brace count: {brace_count}")
