-- Add indexes to improve query performance

-- Users table indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_employee_id ON users(employee_id);
CREATE INDEX IF NOT EXISTS idx_users_department ON users(department);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- Meals table indexes
CREATE INDEX IF NOT EXISTS idx_meals_user_id ON meals(user_id);
CREATE INDEX IF NOT EXISTS idx_meals_date ON meals(date);
CREATE INDEX IF NOT EXISTS idx_meals_user_date ON meals(user_id, date);

-- Overtime table indexes
CREATE INDEX IF NOT EXISTS idx_overtime_user_id ON overtime(user_id);
CREATE INDEX IF NOT EXISTS idx_overtime_date ON overtime(date);
CREATE INDEX IF NOT EXISTS idx_overtime_user_date ON overtime(user_id, date);

-- Positions table indexes
CREATE INDEX IF NOT EXISTS idx_positions_code ON positions(code);
CREATE INDEX IF NOT EXISTS idx_positions_name ON positions(name);

-- Show all indexes
SHOW INDEX FROM users;
SHOW INDEX FROM meals;
SHOW INDEX FROM overtime;
SHOW INDEX FROM positions;
