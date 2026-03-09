# Auto Database Setup Guide

## Tính Năng Tự Động Setup Database

Hệ thống có khả năng tự động:
1. ✅ Kiểm tra database có tồn tại không
2. ✅ Tạo database nếu chưa có
3. ✅ Tạo tất cả tables nếu chưa có
4. ✅ Tạo user mặc định (admin + sample user)

## Cách 1: Auto Setup Khi Chạy App (Khuyến Nghị)

App sẽ tự động kiểm tra và tạo database/tables khi khởi động:

```bash
python app.py
```

Nếu database hoặc tables chưa có, app sẽ tự động tạo!

## Cách 2: Chạy Script Setup Riêng

Nếu muốn setup trước khi chạy app:

```bash
python auto_setup_db.py
```

Script này sẽ:
- Kiểm tra database `db_hr` có tồn tại không
- Nếu không → Tạo database mới
- Tạo tất cả tables (users, overtime_requests, meal_registrations)
- Tạo 2 user mặc định nếu chưa có

## Cách 3: Setup Tự Động Hoàn Toàn

```bash
python setup.py
```

Script này sẽ:
1. Kiểm tra Python version
2. Cài đặt dependencies
3. Tạo .env file
4. Hỏi có muốn setup database không
5. Nếu có → Chạy auto_setup_db.py

## Yêu Cầu

### MySQL Server Phải:
- ✅ Đang chạy
- ✅ User có quyền CREATE DATABASE
- ✅ Thông tin kết nối đúng trong .env

### Quyền MySQL Cần Thiết:

```sql
-- User cần có các quyền sau:
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT 
ON *.* TO 'ovnm'@'%';

-- Hoặc cấp quyền cho database cụ thể:
GRANT ALL PRIVILEGES ON db_hr.* TO 'ovnm'@'%';
FLUSH PRIVILEGES;
```

## Cấu Hình Database

File `.env`:
```env
DB_HOST=10.216.28.11
DB_PORT=3306
DB_USER=ovnm
DB_PASSWORD=P@ssw0rd
DB_NAME=db_hr
```

## Kết Quả Sau Khi Setup

### Database Created:
```
db_hr (CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci)
```

### Tables Created:
1. **users** - Thông tin nhân viên
   - id, employee_id, name, email, password
   - department, role, is_active
   - created_at, last_activity

2. **overtime_requests** - Yêu cầu tăng ca
   - id, user_id, date, start_time, end_time
   - reason, status, approved_by, approved_at
   - created_at, updated_at

3. **meal_registrations** - Đăng ký suất ăn
   - id, user_id, date, meal_type
   - has_meal, notes
   - created_at, updated_at

### Default Users:
```
Admin:
  Employee ID: ADMIN
  Password: admin123
  Role: admin

Sample User:
  Employee ID: EMP001
  Password: password123
  Role: user
```

## Xử Lý Lỗi

### Lỗi: Access denied for user

**Nguyên nhân**: User MySQL không có quyền CREATE DATABASE

**Giải pháp**:
```sql
-- Login as root
mysql -u root -p

-- Grant privileges
GRANT ALL PRIVILEGES ON *.* TO 'ovnm'@'%';
FLUSH PRIVILEGES;
```

### Lỗi: Can't connect to MySQL server

**Nguyên nhân**: MySQL server không chạy hoặc thông tin kết nối sai

**Giải pháp**:
1. Kiểm tra MySQL đang chạy
2. Kiểm tra host, port, user, password trong .env
3. Test connection:
```bash
mysql -h 10.216.28.11 -P 3306 -u ovnm -p
```

### Lỗi: Database exists but tables not created

**Nguyên nhân**: Lỗi trong quá trình tạo tables

**Giải pháp**:
```bash
# Xóa database và tạo lại
mysql -h 10.216.28.11 -u ovnm -p
DROP DATABASE db_hr;
exit

# Chạy lại setup
python auto_setup_db.py
```

## Manual Setup (Nếu Auto Fail)

Nếu auto setup không hoạt động, chạy SQL thủ công:

```sql
-- 1. Create database
CREATE DATABASE db_hr CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db_hr;

-- 2. Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_activity DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. Create overtime_requests table
CREATE TABLE overtime_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    approved_by INT,
    approved_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- 4. Create meal_registrations table
CREATE TABLE meal_registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    meal_type VARCHAR(20),
    has_meal BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 5. Insert default users
INSERT INTO users (employee_id, name, email, password, department, role) VALUES
('ADMIN', 'Administrator', 'admin@okivietnam.com', 
 'scrypt:32768:8:1$...', 'IT', 'admin'),
('EMP001', 'Nguyen Van A', 'nguyenvana@okivietnam.com',
 'scrypt:32768:8:1$...', 'production', 'user');
```

## Kiểm Tra Setup Thành Công

```bash
# Check database exists
mysql -h 10.216.28.11 -u ovnm -p -e "SHOW DATABASES LIKE 'db_hr';"

# Check tables
mysql -h 10.216.28.11 -u ovnm -p db_hr -e "SHOW TABLES;"

# Check users
mysql -h 10.216.28.11 -u ovnm -p db_hr -e "SELECT employee_id, name, role FROM users;"
```

## Best Practices

1. **Backup trước khi setup**: 
   ```bash
   mysqldump -h 10.216.28.11 -u ovnm -p db_hr > backup.sql
   ```

2. **Test connection trước**:
   ```bash
   python -c "from auto_setup_db import create_database_if_not_exists; create_database_if_not_exists()"
   ```

3. **Chạy trong môi trường test trước**

4. **Đổi password mặc định sau khi setup**

## Tích Hợp CI/CD

Trong pipeline deployment:

```yaml
# .github/workflows/deploy.yml
- name: Setup Database
  run: |
    python auto_setup_db.py
  env:
    DB_HOST: ${{ secrets.DB_HOST }}
    DB_USER: ${{ secrets.DB_USER }}
    DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

---

**Version**: 2.0.0  
**Last Updated**: 2026-03-05
