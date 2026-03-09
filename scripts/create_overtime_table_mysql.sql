-- Bảng lưu yêu cầu tăng ca (MySQL version)
CREATE TABLE IF NOT EXISTS overtime_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    employee_id VARCHAR(50) NOT NULL,
    employee_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    position VARCHAR(50),
    
    -- Thông tin tăng ca
    overtime_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    total_hours DECIMAL(4,2) NOT NULL,
    reason TEXT NOT NULL,
    
    -- Trạng thái phê duyệt (chỉ cần trưởng phòng duyệt)
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, approved, rejected
    
    -- Phê duyệt bởi trưởng phòng
    manager_id INT NULL,
    manager_approved_at TIMESTAMP NULL,
    manager_comment TEXT NULL,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE SET NULL,
    
    CONSTRAINT check_time_order CHECK (end_time > start_time),
    CONSTRAINT check_total_hours CHECK (total_hours > 0 AND total_hours <= 24),
    
    INDEX idx_overtime_user_id (user_id),
    INDEX idx_overtime_date (overtime_date),
    INDEX idx_overtime_status (status),
    INDEX idx_overtime_department (department),
    INDEX idx_overtime_manager_id (manager_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bảng lưu thông tin trưởng phòng của mỗi phòng ban
CREATE TABLE IF NOT EXISTS department_managers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department VARCHAR(100) NOT NULL UNIQUE,
    manager_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_dept_manager_department (department)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
