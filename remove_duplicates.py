#!/usr/bin/env python3
"""Remove duplicate functions from overtime.html"""

with open('templates/overtime.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all occurrences of "function formatDate" and "function cancelRequest"
formatDate_lines = []
cancelRequest_lines = []

for i, line in enumerate(lines):
    if 'function formatDate(dateStr)' in line:
        formatDate_lines.append(i)
    if 'function cancelRequest(id)' in line:
        cancelRequest_lines.append(i)

print(f"Found formatDate at lines: {[x+1 for x in formatDate_lines]}")
print(f"Found cancelRequest at lines: {[x+1 for x in cancelRequest_lines]}")

# If there are duplicates, keep only the first one and remove others
if len(formatDate_lines) > 1:
    # Remove second formatDate (from line to closing brace)
    start = formatDate_lines[1]
    # Find closing brace
    brace_count = 0
    found_opening = False
    end = start
    for i in range(start, len(lines)):
        for char in lines[i]:
            if char == '{':
                brace_count += 1
                found_opening = True
            elif char == '}':
                brace_count -= 1
                if found_opening and brace_count == 0:
                    end = i
                    break
        if found_opening and brace_count == 0:
            break
    
    print(f"Removing formatDate from line {start+1} to {end+1}")
    del lines[start:end+1]

# Reload to get new line numbers
if len(cancelRequest_lines) > 1:
    # Recalculate line numbers
    cancelRequest_lines = []
    for i, line in enumerate(lines):
        if 'function cancelRequest(id)' in line:
            cancelRequest_lines.append(i)
    
    if len(cancelRequest_lines) > 1:
        start = cancelRequest_lines[1]
        # Find closing brace
        brace_count = 0
        found_opening = False
        end = start
        for i in range(start, len(lines)):
            for char in lines[i]:
                if char == '{':
                    brace_count += 1
                    found_opening = True
                elif char == '}':
                    brace_count -= 1
                    if found_opening and brace_count == 0:
                        end = i
                        break
            if found_opening and brace_count == 0:
                break
        
        print(f"Removing cancelRequest from line {start+1} to {end+1}")
        del lines[start:end+1]

# Also remove duplicate "container.innerHTML" line
for i in range(len(lines)-1, -1, -1):
    if i > 0 and 'container.innerHTML = mobileHTML' in lines[i] and 'container.innerHTML = mobileHTML' in lines[i-1]:
        print(f"Removing duplicate container.innerHTML at line {i+1}")
        del lines[i]

# Write back
with open('templates/overtime.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Removed duplicates successfully!")
