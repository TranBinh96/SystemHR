#!/usr/bin/env python3
"""
Script cập nhật bảng users trên server chính
Thêm các cột còn thiếu một cách an toàn
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
import pymysql

def get_db_connection():
    """Kết nối đến database"""
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def column_exists(cursor, table_name, column_name):
    """Kiểm tra xem cột có tồn tại không"""
    cursor.execute(f"""
        SELECT COUNT(*) as count
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = '{Config.DB_NAME}'
        AND TABLE_NAME = '{table_name}'
        AND COLUMN_NAME = '{column_name}'
    """)
    result = cursor.fetchone()
    return result['count'] > 0

def index_exists(cursor, table_name, index_name):
    """Kiểm tra xem index có tồn tại không"""
    cursor.execute(f"""
        SELECT COUNT(*) as count
        FROM information_schema.STATISTICS
        WHERE TABLE_SCHEMA = '{Config.DB_NAME}'
        AND TABLE_NAME = '{table_name}'
        AND INDEX_NAME = '{index_name}'
    """)
    result = cursor.fetchone()
    return result['count'] > 0

def foreign_key_exists(cursor, table_name, constraint_name):
    """Kiểm tra xem foreign key có tồn tại không"""
    cursor.execute(f"""
        SELECT COUNT(*) as count
        FROM information_schema.TABLE_CONSTRAINTS
        WHERE TABLE_SCHEMA = '{Config.DB_NAME}'
        AND TABLE_NAME = '{table_name}'
        AND CONSTRAINT_NAME = '{constraint_name}'
        AND CONSTRAINT_TYPE = 'FOREIGN KEY'
    """)
    result = cursor.fetchone()
    return result['count'] > 0

def update_users_table():
    """Cập nhật bảng users"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("🔄 Bắt đầu cập nhật bảng users...")
        print()
        
        # Danh sách các cột cần thêm
        columns_to_add = [
            {
                'name': 'department_id',
                'definition': 'INT NULL',
                'description': 'ID phòng ban'
            },
            {
                'name': 'position_id',
                'definition': 'INT NULL',
                'description': 'ID chức vụ'
            },
            {
                'name': 'work_status',
                'definition': "VARCHAR(20) NULL DEFAULT 'working'",
                'description': 'Trạng thái làm việc'
            },
            {
                'name': 'avatar_url',
                'definition': 'VARCHAR(255) NULL',
                'description': 'URL ảnh đại diện'
            },
            {
                'name': 'role',
                'definition': "VARCHAR(20) NULL DEFAULT 'user'",
                'description': 'Vai trò (user/admin)'
            },
            {
                'name': 'is_active',
                'definition': 'TINYINT(1) NULL DEFAULT 1',
                'description': 'Tài khoản có hoạt động không'
            },
            {
                'name': 'can_approve',
                'definition': 'TINYINT(1) NULL DEFAULT 0',
                'description': 'Có quyền duyệt không'
            },
            {
                'name': 'can_register',
                'definition': 'TINYINT(1) NULL DEFAULT 1',
                'description': 'Có quyền đăng ký không'
            },
            {
                'name': 'created_at',
                'definition': 'DATETIME NULL DEFAULT CURRENT_TIMESTAMP',
                'description': 'Ngày tạo'
            },
            {
                'name': 'last_activity',
                'definition': 'DATETIME NULL',
                'description': 'Lần hoạt động cuối'
            }
        ]
        
        # Thêm các cột
        for col in columns_to_add:
            if not column_exists(cursor, 'users', col['name']):
                print(f"➕ Thêm cột '{col['name']}' ({col['description']})...")
                sql = f"ALTER TABLE users ADD COLUMN {col['name']} {col['definition']}"
                cursor.execute(sql)
                conn.commit()
                print(f"   ✅ Đã thêm cột '{col['name']}'")
            else:
                print(f"⏭️  Cột '{col['name']}' đã tồn tại, bỏ qua")
        
        print()
        
        # Thêm foreign keys
        print("🔗 Kiểm tra foreign keys...")
        
        if not foreign_key_exists(cursor, 'users', 'users_ibfk_1'):
            print("➕ Thêm foreign key users_ibfk_1 (department_id)...")
            try:
                cursor.execute("""
                    ALTER TABLE users 
                    ADD CONSTRAINT users_ibfk_1 
                    FOREIGN KEY (department_id) REFERENCES departments(id)
                """)
                conn.commit()
                print("   ✅ Đã thêm foreign key users_ibfk_1")
            except Exception as e:
                print(f"   ⚠️  Không thể thêm foreign key users_ibfk_1: {e}")
        else:
            print("⏭️  Foreign key users_ibfk_1 đã tồn tại")
        
        if not foreign_key_exists(cursor, 'users', 'users_ibfk_2'):
            print("➕ Thêm foreign key users_ibfk_2 (position_id)...")
            try:
                cursor.execute("""
                    ALTER TABLE users 
                    ADD CONSTRAINT users_ibfk_2 
                    FOREIGN KEY (position_id) REFERENCES positions(id)
                """)
                conn.commit()
                print("   ✅ Đã thêm foreign key users_ibfk_2")
            except Exception as e:
                print(f"   ⚠️  Không thể thêm foreign key users_ibfk_2: {e}")
        else:
            print("⏭️  Foreign key users_ibfk_2 đã tồn tại")
        
        print()
        
        # Thêm indexes
        print("📇 Kiểm tra indexes...")
        
        if not index_exists(cursor, 'users', 'department_id'):
            print("➕ Thêm index cho department_id...")
            cursor.execute("CREATE INDEX department_id ON users(department_id)")
            conn.commit()
            print("   ✅ Đã thêm index department_id")
        else:
            print("⏭️  Index department_id đã tồn tại")
        
        if not index_exists(cursor, 'users', 'position_id'):
            print("➕ Thêm index cho position_id...")
            cursor.execute("CREATE INDEX position_id ON users(position_id)")
            conn.commit()
            print("   ✅ Đã thêm index position_id")
        else:
            print("⏭️  Index position_id đã tồn tại")
        
        print()
        
        # Cập nhật giá trị mặc định cho các bản ghi hiện có
        print("🔄 Cập nhật giá trị mặc định cho các bản ghi hiện có...")
        
        updates = [
            ("UPDATE users SET is_active = 1 WHERE is_active IS NULL", "is_active"),
            ("UPDATE users SET can_register = 1 WHERE can_register IS NULL", "can_register"),
            ("UPDATE users SET can_approve = 0 WHERE can_approve IS NULL", "can_approve"),
            ("UPDATE users SET role = 'user' WHERE role IS NULL", "role"),
            ("UPDATE users SET work_status = 'working' WHERE work_status IS NULL", "work_status"),
            ("UPDATE users SET created_at = NOW() WHERE created_at IS NULL", "created_at")
        ]
        
        for sql, field in updates:
            cursor.execute(sql)
            affected = cursor.rowcount
            if affected > 0:
                print(f"   ✅ Cập nhật {affected} bản ghi cho trường '{field}'")
        
        conn.commit()
        
        print()
        print("=" * 60)
        print("✅ CẬP NHẬT BẢNG USERS THÀNH CÔNG!")
        print("=" * 60)
        print()
        
        # Hiển thị cấu trúc bảng
        print("📋 Cấu trúc bảng users sau khi cập nhật:")
        print()
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        
        print(f"{'Field':<20} {'Type':<20} {'Null':<6} {'Key':<6} {'Default':<15} {'Extra':<15}")
        print("-" * 90)
        for col in columns:
            print(f"{col['Field']:<20} {col['Type']:<20} {col['Null']:<6} {col['Key']:<6} {str(col['Default']):<15} {col['Extra']:<15}")
        
        print()
        
        # Đếm số lượng users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        count = cursor.fetchone()['count']
        print(f"📊 Tổng số users trong bảng: {count}")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print()
    print("=" * 60)
    print("SCRIPT CẬP NHẬT BẢNG USERS")
    print("=" * 60)
    print()
    
    try:
        update_users_table()
    except Exception as e:
        print(f"\n❌ Script thất bại: {e}")
        sys.exit(1)
