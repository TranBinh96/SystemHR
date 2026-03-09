#!/usr/bin/env python3
"""Analyze HTML structure to find misplaced divs"""

with open('templates/overtime.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find key markers
tab1_start = None
tab1_end = None
tab2_start = None
tab2_end = None
form_start = None
form_end = None

for i, line in enumerate(lines, 1):
    if 'id="content-register"' in line:
        tab1_start = i
        print(f"Line {i}: Tab 1 START - {line.strip()}")
    elif 'End Tab Content: Register' in line:
        # Find the closing div before this comment
        for j in range(i-1, max(0, i-5), -1):
            if '</div>' in lines[j-1]:
                tab1_end = j
                print(f"Line {j}: Tab 1 END - {lines[j-1].strip()}")
                break
    elif 'id="content-status"' in line:
        tab2_start = i
        print(f"Line {i}: Tab 2 START - {line.strip()}")
    elif 'End Tab Content: Status' in line:
        for j in range(i-1, max(0, i-5), -1):
            if '</div>' in lines[j-1]:
                tab2_end = j
                print(f"Line {j}: Tab 2 END - {lines[j-1].strip()}")
                break
    elif '<form' in line and 'overtime-form' in line:
        form_start = i
        print(f"Line {i}: FORM START - {line.strip()}")
    elif '</form>' in line and form_start and not form_end:
        form_end = i
        print(f"Line {i}: FORM END - {line.strip()}")

print("\n=== ANALYSIS ===")
print(f"Tab 1: Lines {tab1_start} to {tab1_end}")
print(f"Form: Lines {form_start} to {form_end}")
print(f"Tab 2: Lines {tab2_start} to {tab2_end}")

if form_end and tab1_end:
    if form_end > tab1_end:
        print(f"\n⚠️  ERROR: Form ends AFTER Tab 1 closes!")
        print(f"   Form end: {form_end}, Tab 1 end: {tab1_end}")
    else:
        print(f"\n✓ OK: Form is inside Tab 1")

# Check for content between tabs
if tab1_end and tab2_start:
    between_lines = tab2_start - tab1_end
    if between_lines > 5:
        print(f"\n⚠️  WARNING: {between_lines} lines between Tab 1 and Tab 2")
        print("Content between tabs:")
        for i in range(tab1_end, tab2_start):
            line = lines[i].strip()
            if line and not line.startswith('<!--'):
                print(f"  Line {i+1}: {line}")
