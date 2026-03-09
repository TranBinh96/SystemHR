with open('templates/overtime.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check lines around the script tag
for i in range(283, 293):
    if i < len(lines):
        line = lines[i]
        print(f"Line {i+1}: {repr(line)}")
