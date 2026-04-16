-- Add confirmation fields to meal_registrations table
-- Run this SQL script to update the database schema

-- Add is_confirmed column (default FALSE)
ALTER TABLE meal_registrations 
ADD COLUMN is_confirmed BOOLEAN DEFAULT FALSE;

-- Add confirmed_at column (nullable datetime)
ALTER TABLE meal_registrations 
ADD COLUMN confirmed_at DATETIME;

-- Add confirmed_by column (foreign key to users table)
ALTER TABLE meal_registrations 
ADD COLUMN confirmed_by INTEGER;

-- Add foreign key constraint for confirmed_by
ALTER TABLE meal_registrations 
ADD CONSTRAINT fk_meal_registrations_confirmed_by 
FOREIGN KEY (confirmed_by) REFERENCES users(id);

-- Create index for faster queries on is_confirmed
CREATE INDEX idx_meal_registrations_is_confirmed 
ON meal_registrations(is_confirmed);

-- Create index for faster queries on confirmed_at
CREATE INDEX idx_meal_registrations_confirmed_at 
ON meal_registrations(confirmed_at);

-- Verify the changes
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'meal_registrations'
ORDER BY ORDINAL_POSITION;
