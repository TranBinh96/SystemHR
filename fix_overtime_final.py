#!/usr/bin/env python3
"""Fix overtime.html by moving mobile cards code inside renderMyRequests function"""

with open('templates/overtime.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line "container.innerHTML = tableHTML;"
# and the line "// Build mobile cards"
container_line_idx = None
mobile_cards_start_idx = None
mobile_cards_end_idx = None

for i, line in enumerate(lines):
    if 'container.innerHTML = tableHTML;' in line:
        container_line_idx = i
    if '// Build mobile cards' in line:
        mobile_cards_start_idx = i
    if mobile_cards_start_idx and 'container.innerHTML = mobileHTML' in line:
        # Find the closing brace after this line
        for j in range(i, min(i+5, len(lines))):
            if lines[j].strip() == '}':
                mobile_cards_end_idx = j
                break

if container_line_idx and mobile_cards_start_idx and mobile_cards_end_idx:
    print(f"Found container.innerHTML at line {container_line_idx + 1}")
    print(f"Found mobile cards from line {mobile_cards_start_idx + 1} to {mobile_cards_end_idx + 1}")
    
    # Extract mobile cards code
    mobile_cards_code = lines[mobile_cards_start_idx:mobile_cards_end_idx+1]
    
    # Remove mobile cards from original position
    del lines[mobile_cards_start_idx:mobile_cards_end_idx+1]
    
    # Recalculate container_line_idx after deletion
    if mobile_cards_start_idx < container_line_idx:
        container_line_idx -= (mobile_cards_end_idx - mobile_cards_start_idx + 1)
    
    # Insert mobile cards before container.innerHTML line
    # Replace "container.innerHTML = tableHTML;" with mobile cards + new container.innerHTML
    indent = '            '
    new_lines = mobile_cards_code + [indent + "container.innerHTML = mobileHTML + '<div class=\"hidden lg:block\">' + tableHTML + '</div>';\n"]
    
    # Remove old container.innerHTML line
    lines[container_line_idx] = ''
    
    # Insert new code
    for idx, new_line in enumerate(new_lines):
        lines.insert(container_line_idx + idx, new_line)
    
    # Write back
    with open('templates/overtime.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("Fixed successfully!")
else:
    print("Could not find required lines")
    print(f"container_line_idx: {container_line_idx}")
    print(f"mobile_cards_start_idx: {mobile_cards_start_idx}")
    print(f"mobile_cards_end_idx: {mobile_cards_end_idx}")
