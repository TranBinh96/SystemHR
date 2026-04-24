#!/usr/bin/env python3
"""
Script kiểm tra timezone fix đã hoàn thành
"""

import re
import os

def check_timezone_fixes():
    """Kiểm tra xem timezone fixes đã hoàn thành chưa"""
    
    file_path = 'app.py'
    
    if not os.path.exists(file_path):
        print(f"❌ File không tồn tại: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 KIỂM TRA TIMEZONE FIXES")
    print("=" * 50)
    
    # Kiểm tra import
    if 'from utils.timezone_utils import' in content:
        print("✅ Import timezone utils: OK")
    else:
        print("❌ Import timezone utils: MISSING")
    
    # Kiểm tra các patterns cũ
    issues = []
    
    # 1. datetime.now().date()
    pattern1 = r'datetime\.now\(\)\.date\(\)'
    matches1 = re.findall(pattern1, content)
    if matches1:
        issues.append(f"datetime.now().date() còn {len(matches1)} chỗ")
    else:
        print("✅ datetime.now().date(): Đã sửa hết")
    
    # 2. datetime.now() (không có .date())
    pattern2 = r'datetime\.now\(\)(?!\.date\(\))'
    matches2 = re.findall(pattern2, content)
    if matches2:
        issues.append(f"datetime.now() còn {len(matches2)} chỗ")
    else:
        print("✅ datetime.now(): Đã sửa hết")
    
    # 3. date.today()
    pattern3 = r'date\.today\(\)'
    matches3 = re.findall(pattern3, content)
    if matches3:
        issues.append(f"date.today() còn {len(matches3)} chỗ")
    else:
        print("✅ date.today(): Đã sửa hết")
    
    # 4. Kiểm tra scheduler
    if 'timezone=\'Asia/Ho_Chi_Minh\'' in content:
        print("✅ Scheduler timezone: Asia/Ho_Chi_Minh")
    elif 'timezone=\'UTC\'' in content:
        print("⚠️  Scheduler timezone: UTC (cần đổi thành Asia/Ho_Chi_Minh)")
    else:
        print("❌ Scheduler timezone: Không tìm thấy")
    
    # Tổng kết
    print("\n" + "=" * 50)
    if issues:
        print("❌ CÒN VẤN ĐỀ:")
        for issue in issues:
            print(f"   • {issue}")
        return False
    else:
        print("✅ TẤT CẢ TIMEZONE FIXES ĐÃ HOÀN THÀNH!")
        return True

def check_config():
    """Kiểm tra config timezone"""
    print("\n🔧 KIỂM TRA CONFIG")
    print("=" * 30)
    
    # Kiểm tra .env
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
        
        if 'TIMEZONE=Asia/Ho_Chi_Minh' in env_content:
            print("✅ .env TIMEZONE: Asia/Ho_Chi_Minh")
        else:
            print("❌ .env TIMEZONE: Chưa set hoặc sai")
    else:
        print("⚠️  .env: File không tồn tại")
    
    # Kiểm tra config.py
    if os.path.exists('config.py'):
        with open('config.py', 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        if 'Asia/Ho_Chi_Minh' in config_content:
            print("✅ config.py TIMEZONE: Asia/Ho_Chi_Minh")
        else:
            print("❌ config.py TIMEZONE: Chưa set hoặc sai")
    else:
        print("❌ config.py: File không tồn tại")

def test_timezone_utils():
    """Test timezone utilities"""
    print("\n🧪 TEST TIMEZONE UTILS")
    print("=" * 30)
    
    try:
        from utils.timezone_utils import now, today, utcnow
        
        vn_time = now()
        vn_date = today()
        utc_time = utcnow()
        
        print(f"✅ VN time: {vn_time}")
        print(f"✅ VN date: {vn_date}")
        print(f"✅ UTC time: {utc_time}")
        
        # Kiểm tra timezone
        if '+07:00' in str(vn_time) or vn_time.tzinfo is not None:
            print("✅ VN time có timezone info")
        else:
            print("❌ VN time thiếu timezone info")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi test timezone utils: {e}")
        return False

def main():
    """Main function"""
    print("🚂 KIỂM TRA TIMEZONE FIX CHO RAILWAY")
    print("=" * 60)
    
    # Kiểm tra code fixes
    code_ok = check_timezone_fixes()
    
    # Kiểm tra config
    check_config()
    
    # Test timezone utils
    utils_ok = test_timezone_utils()
    
    print("\n" + "=" * 60)
    if code_ok and utils_ok:
        print("🎉 HOÀN THÀNH! SẴN SÀNG DEPLOY LÊN RAILWAY")
        print("\n📋 NEXT STEPS:")
        print("1. Thêm Environment Variables trong Railway Dashboard:")
        print("   TIMEZONE=Asia/Ho_Chi_Minh")
        print("   TZ=Asia/Ho_Chi_Minh")
        print("2. Commit và push code:")
        print("   git add .")
        print("   git commit -m 'Complete timezone fix for Railway'")
        print("   git push origin main")
        print("3. Railway sẽ tự động redeploy")
        print("4. Kiểm tra logs: railway logs")
    else:
        print("❌ VẪN CÒN VẤN ĐỀ CẦN SỬA")

if __name__ == "__main__":
    main()