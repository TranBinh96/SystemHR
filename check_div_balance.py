#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check if divs are balanced in overtime.html"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('templates/overtime.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Track div balance
div_stack = []
in_tab1 = False
in_tab2 = False
tab1_start = None
tab1_divs = 0

for i, line in enumerate(lines, 1):
    # Check for Tab 1 start
    if 'id="content-register"' in line:
        in_tab1 = True
        tab1_start = i
        tab1_divs = 0
        print(f"\n{'='*60}")
        print(f"Line {i}: TAB 1 STARTS")
        print(f"{'='*60}")
    
    # Check for Tab 2 start
    if 'id="content-status"' in line:
        in_tab2 = True
        print(f"\n{'='*60}")
        print(f"Line {i}: TAB 2 STARTS")
        print(f"{'='*60}")
        print(f"Tab 1 had {tab1_divs} divs (should be 0 if balanced)")
        if tab1_divs != 0:
            print(f"WARNING: Tab 1 divs not balanced! Missing {-tab1_divs} closing divs")
        in_tab1 = False
    
    # Count divs in Tab 1
    if in_tab1:
        if '<div' in line:
            tab1_divs += line.count('<div')
            # Show important divs
            if 'class=' in line or 'id=' in line:
                print(f"Line {i}: +DIV {line.strip()[:80]}")
        if '</div>' in line:
            tab1_divs -= line.count('</div>')
            print(f"Line {i}: -DIV (balance: {tab1_divs})")
            
            # Check if this closes Tab 1
            if i > tab1_start + 10:  # Not immediately after start
                next_line = lines[i] if i < len(lines) else ""
                if 'End Tab Content: Register' in next_line:
                    print(f"\n{'='*60}")
                    print(f"Line {i}: TAB 1 ENDS HERE")
                    print(f"Final balance: {tab1_divs} (should be 0)")
                    print(f"{'='*60}")
                    if tab1_divs != 0:
                        print(f"ERROR: Unbalanced divs in Tab 1!")
                    in_tab1 = False

print("\n\nSearching for content between Tab 1 and Tab 2...")
tab1_end_line = None
tab2_start_line = None

for i, line in enumerate(lines, 1):
    if 'End Tab Content: Register' in line:
        tab1_end_line = i
    if 'id="content-status"' in line:
        tab2_start_line = i
        break

if tab1_end_line and tab2_start_line:
    print(f"\nTab 1 ends at line {tab1_end_line}")
    print(f"Tab 2 starts at line {tab2_start_line}")
    print(f"\nContent between (lines {tab1_end_line+1} to {tab2_start_line-1}):")
    for i in range(tab1_end_line, tab2_start_line):
        line = lines[i].strip()
        if line and not line.startswith('<!--'):
            print(f"  Line {i+1}: {line}")
