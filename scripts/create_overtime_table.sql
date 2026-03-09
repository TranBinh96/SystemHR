-- Bảng lưu yêu cầu tăng ca
CREATE TABLE IF NOT EXISTS overtime_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
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
    manager_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    manager_approved_at TIMESTAMP,
    manager_comment TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT check_time_order CHECK (end_time > start_time),
    CONSTRAINT check_total_hours CHECK (total_hours > 0 AND total_hours <= 24)
);

-- Index để tăng tốc truy vấn
CREATE INDEX IF NOT EXISTS idx_overtime_user_id ON overtime_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_overtime_date ON overtime_requests(overtime_date);
CREATE INDEX IF NOT EXISTS idx_overtime_status ON overtime_requests(status);
CREATE INDEX IF NOT EXISTS idx_overtime_department ON overtime_requests(department);
CREATE INDEX IF NOT EXISTS idx_overtime_manager_id ON overtime_requests(manager_id);

-- Bảng lưu thông tin trưởng phòng của mỗi phòng ban
CREATE TABLE IF NOT EXISTS department_managers (
    id SERIAL PRIMARY KEY,
    department VARCHAR(100) NOT NULL UNIQUE,
    manager_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX IF NOT EXISTS idx_dept_manager_department ON department_managers(department);

-- Thêm dữ liệu mẫu cho department_managers (cần cập nhật manager_id thực tế)
-- INSERT INTO department_managers (department, manager_id) VALUES
-- ('Production', 1),  -- Thay 1 bằng user_id của trưởng phòng Production
-- ('HR', 2),
-- ('IT', 3),
-- ('Quality', 4),
-- ('Finance', 5),
-- ('Sales', 6),
-- ('Marketing', 7);

-- Trigger để tự động cập nhật updated_at
CREATE OR REPLACE FUNCTION update_overtime_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_overtime_updated_at
    BEFORE UPDATE ON overtime_requests
    FOR EACH ROW
    EXECUTE FUNCTION update_overtime_updated_at();

CREATE TRIGGER trigger_update_dept_manager_updated_at
    BEFORE UPDATE ON department_managers
    FOR EACH ROW
    EXECUTE FUNCTION update_overtime_updated_at();
