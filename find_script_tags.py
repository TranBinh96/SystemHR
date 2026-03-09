with open('templates/overtime.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    if '<script' in line.lower() or '</script' in line.lower():
        print(f"Line {i}: {line.rstrip()}")
