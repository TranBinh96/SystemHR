-- ============================================================
-- Migration Script: Remove Position Tables and Columns
-- ============================================================
-- This script removes all position-related tables and columns
-- from the database.
--
-- IMPORTANT: Backup your database before running this script!
-- mysqldump -u ovnm -p db_hr > backup_before_remove_position.sql
--
-- To run this script:
-- mysql -u ovnm -p db_hr < scripts/remove_position_tables.sql
-- ============================================================

USE db_hr;

-- Show current database
SELECT DATABASE() AS 'Current Database';

-- ============================================================
-- STEP 1: Drop foreign key constraints
-- ============================================================
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

-- Drop position_id foreign key from users table
SELECT 'Dropping foreign key constraints...' AS 'Step 1';

-- Find and drop the foreign key constraint for position_id
SET @constraint_name = (
    SELECT CONSTRAINT_NAME 
    FROM information_schema.KEY_COLUMN_USAGE 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'users' 
    AND COLUMN_NAME = 'position_id' 
    AND REFERENCED_TABLE_NAME = 'positions'
    LIMIT 1
);

SET @sql = IF(@constraint_name IS NOT NULL, 
    CONCAT('ALTER TABLE users DROP FOREIGN KEY ', @constraint_name),
    'SELECT "No foreign key constraint found for users.position_id" AS Info'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ============================================================
-- STEP 2: Drop position_id column from users table
-- ============================================================
SELECT 'Dropping position_id column from users table...' AS 'Step 2';

ALTER TABLE users DROP COLUMN IF EXISTS position_id;

SELECT 'OK: Removed position_id from users table' AS 'Result';

-- ============================================================
-- STEP 3: Drop position column from overtime_requests table
-- ============================================================
SELECT 'Dropping position column from overtime_requests table...' AS 'Step 3';

ALTER TABLE overtime_requests DROP COLUMN IF EXISTS position;

SELECT 'OK: Removed position from overtime_requests table' AS 'Result';

-- ============================================================
-- STEP 4: Drop position column from leave_requests table
-- ============================================================
SELECT 'Dropping position column from leave_requests table...' AS 'Step 4';

ALTER TABLE leave_requests DROP COLUMN IF EXISTS position;

SELECT 'OK: Removed position from leave_requests table' AS 'Result';

-- ============================================================
-- STEP 5: Drop position column from exit_entry_requests table
-- ============================================================
SELECT 'Dropping position column from exit_entry_requests table...' AS 'Step 5';

ALTER TABLE exit_entry_requests DROP COLUMN IF EXISTS position;

SELECT 'OK: Removed position from exit_entry_requests table' AS 'Result';

-- ============================================================
-- STEP 6: Drop approval_hierarchy table
-- ============================================================
SELECT 'Dropping approval_hierarchy table...' AS 'Step 6';

DROP TABLE IF EXISTS approval_hierarchy;

SELECT 'OK: Dropped approval_hierarchy table' AS 'Result';

-- ============================================================
-- STEP 7: Drop positions table
-- ============================================================
SELECT 'Dropping positions table...' AS 'Step 7';

DROP TABLE IF EXISTS positions;

SELECT 'OK: Dropped positions table' AS 'Result';

-- ============================================================
-- STEP 8: Restore foreign key checks
-- ============================================================
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;

-- ============================================================
-- VERIFICATION: Check if tables and columns are removed
-- ============================================================
SELECT '========================================' AS '';
SELECT 'VERIFICATION RESULTS' AS '';
SELECT '========================================' AS '';

-- Check if positions table exists
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'OK: positions table removed'
        ELSE 'ERROR: positions table still exists'
    END AS 'Positions Table'
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'positions';

-- Check if approval_hierarchy table exists
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'OK: approval_hierarchy table removed'
        ELSE 'ERROR: approval_hierarchy table still exists'
    END AS 'Approval Hierarchy Table'
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'approval_hierarchy';

-- Check if position_id column exists in users
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'OK: position_id column removed from users'
        ELSE 'ERROR: position_id column still exists in users'
    END AS 'Users.position_id Column'
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'users' 
AND COLUMN_NAME = 'position_id';

-- Check if position column exists in overtime_requests
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'OK: position column removed from overtime_requests'
        ELSE 'ERROR: position column still exists in overtime_requests'
    END AS 'OvertimeRequests.position Column'
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'overtime_requests' 
AND COLUMN_NAME = 'position';

-- Check if position column exists in leave_requests
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'OK: position column removed from leave_requests'
        ELSE 'ERROR: position column still exists in leave_requests'
    END AS 'LeaveRequests.position Column'
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'leave_requests' 
AND COLUMN_NAME = 'position';

-- Check if position column exists in exit_entry_requests
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'OK: position column removed from exit_entry_requests'
        ELSE 'ERROR: position column still exists in exit_entry_requests'
    END AS 'ExitEntryRequests.position Column'
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'exit_entry_requests' 
AND COLUMN_NAME = 'position';

SELECT '========================================' AS '';
SELECT 'MIGRATION COMPLETED SUCCESSFULLY!' AS '';
SELECT '========================================' AS '';
SELECT 'All position-related tables and columns have been removed.' AS 'Status';
SELECT 'You can now restart your application.' AS 'Next Step';
