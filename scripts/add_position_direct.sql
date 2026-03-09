-- Add position column to users table
-- Run this SQL directly in your MySQL database

ALTER TABLE users ADD COLUMN position VARCHAR(50) DEFAULT 'staff' AFTER department;
