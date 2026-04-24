#!/usr/bin/env python3
"""
Script để sửa timezone cho Railway deployment
"""

import re
import os

def fix_railway_timezone():
    """Sửa timezone trong app.py cho Railway"""
    
    file_path = 'app.py'
    
    if not os.path.exists(file_path):
        print(f"❌ File không tồn tại: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = []
    
    # 1. Thay thế datetime.now().date() -> today()
    pattern1 = r'datetime\.now\(\)\.date\(\)'
    if re.search(pattern1, content):
        content = re.sub(pattern1, 'today()', content)
        changes_made.append("datetime.now().date() → today()")
    
    # 2. Thay thế datetime.now() (không có .date()) -> now()
    # Tìm tất cả datetime.now() không có .date() sau
    pattern2 = r'datetime\.now\(\)(?!\.date\(\))'
    if re.search(pattern2, content):
        content = re.sub(pattern2, 'now()', content)
        changes_made.append("datetime.now() → now()")
    
    # 3. Thay thế date.today() -> today()
    pattern3 = r'date\.today\(\)'
    if re.search(pattern3, content):
        content = re.sub(pattern3, 'today()', content)
        changes_made.append("date.today() → today()")
    
    # 4. Sửa scheduler timezone cho Railway (UTC)
    pattern4 = r'trigger=CronTrigger\(hour=16, minute=0\)'
    replacement4 = 'trigger=CronTrigger(hour=9, minute=0, timezone="UTC")  # 9:00 UTC = 16:00 VN'
    if re.search(pattern4, content):
        content = re.sub(pattern4, replacement4, content)
        changes_made.append("Scheduler timezone → UTC (9:00 UTC = 16:00 VN)")
    
    # 5. Kiểm tra import đã có chưa
    if 'from utils.timezone_utils import' not in content:
        # Tìm vị trí thêm import
        import_pattern = r'(from apscheduler\.triggers\.cron import CronTrigger\n)'
        import_replacement = r'\1\n# Import timezone utilities for Railway\nfrom utils.timezone_utils import now, today, utcnow, format_local_datetime, format_local_date\n'
        
        if re.search(import_pattern, content):
            content = re.sub(import_pattern, import_replacement, content)
            changes_made.append("Added timezone utils import")
    
    # Ghi lại file nếu có thay đổi
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Đã sửa timezone cho Railway deployment!")
        print("📋 Các thay đổi:")
        for change in changes_made:
            print(f"   • {change}")
        
        return True
    else:
        print("ℹ️  Không có thay đổi nào cần thiết")
        return False

def create_railway_env_guide():
    """Tạo hướng dẫn setup Railway environment"""
    
    guide = """
🚂 RAILWAY ENVIRONMENT SETUP

1. Vào Railway Dashboard → Your Project
2. Click tab "Variables" 
3. Thêm các biến sau:

┌─────────────────────────────────────┐
│ Variable Name    │ Value            │
├─────────────────────────────────────┤
│ TIMEZONE         │ Asia/Ho_Chi_Minh │
│ TZ               │ Asia/Ho_Chi_Minh │
└─────────────────────────────────────┘

4. Click "Deploy" để áp dụng thay đổi

⚠️  LƯU Ý:
- Railway server luôn dùng UTC timezone
- Scheduler sẽ chạy lúc 9:00 UTC = 16:00 VN
- Database vẫn lưu UTC, chỉ convert khi hiển thị
"""
    
    print(guide)

def main():
    """Main function"""
    print("🚂 RAILWAY TIMEZONE FIX")
    print("=" * 50)
    
    # Sửa code
    if fix_railway_timezone():
        print("\n✅ Code đã được sửa!")
    
    # Hiển thị hướng dẫn Railway
    print("\n" + "=" * 50)
    create_railway_env_guide()
    
    print("\n📋 NEXT STEPS:")
    print("1. Setup Railway Environment Variables (xem hướng dẫn trên)")
    print("2. Commit và push code:")
    print("   git add .")
    print("   git commit -m 'Fix timezone for Railway'")
    print("   git push origin main")
    print("3. Railway sẽ tự động redeploy")
    print("4. Kiểm tra logs: railway logs")

if __name__ == "__main__":
    main()