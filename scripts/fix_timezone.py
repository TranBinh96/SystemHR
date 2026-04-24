#!/usr/bin/env python3
"""
Script để sửa tất cả các chỗ sử dụng datetime không có timezone
"""

import re
import os

def fix_timezone_in_file(file_path):
    """Sửa timezone trong một file"""
    
    if not os.path.exists(file_path):
        print(f"File không tồn tại: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Các pattern cần thay thế
    replacements = [
        # datetime.now().date() -> today()
        (r'datetime\.now\(\)\.date\(\)', 'today()'),
        
        # datetime.now() -> now() (chỉ khi không có .date())
        (r'(?<!\.date\(\)\s*)datetime\.now\(\)(?!\s*\.date)', 'now()'),
        
        # datetime.utcnow() -> utcnow()
        (r'datetime\.utcnow\(\)', 'utcnow()'),
        
        # date.today() -> today()
        (r'date\.today\(\)', 'today()'),
        
        # Thêm import nếu chưa có
        # Sẽ được xử lý riêng
    ]
    
    # Thực hiện thay thế
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Kiểm tra xem có thay đổi gì không
    if content != original_content:
        # Kiểm tra xem đã có import timezone utils chưa
        if 'from utils.timezone_utils import' not in content:
            # Tìm dòng import cuối cùng để thêm import
            import_lines = []
            other_lines = []
            in_imports = True
            
            for line in content.split('\n'):
                if in_imports and (line.startswith('from ') or line.startswith('import ') or line.strip() == ''):
                    import_lines.append(line)
                else:
                    if line.strip() and in_imports:
                        # Thêm import timezone utils trước dòng đầu tiên không phải import
                        import_lines.append('')
                        import_lines.append('# Import timezone utilities')
                        import_lines.append('from utils.timezone_utils import now, today, utcnow, format_local_datetime, format_local_date')
                        import_lines.append('')
                        in_imports = False
                    other_lines.append(line)
            
            content = '\n'.join(import_lines + other_lines)
        
        # Ghi lại file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Đã sửa timezone trong: {file_path}")
        return True
    else:
        print(f"ℹ️  Không có thay đổi trong: {file_path}")
        return False

def main():
    """Main function"""
    print("🔧 Bắt đầu sửa timezone trong các file...")
    
    # Danh sách file cần sửa
    files_to_fix = [
        'app.py',
        'models/__init__.py',
    ]
    
    total_fixed = 0
    
    for file_path in files_to_fix:
        if fix_timezone_in_file(file_path):
            total_fixed += 1
    
    print(f"\n✅ Hoàn thành! Đã sửa {total_fixed}/{len(files_to_fix)} file(s)")
    print("\n📋 Các bước tiếp theo:")
    print("1. Cài đặt pytz: pip install pytz")
    print("2. Restart ứng dụng")
    print("3. Kiểm tra timezone hoạt động đúng")

if __name__ == "__main__":
    main()