-- =====================================================
-- SERVICE USER CLEANUP SCRIPT
-- =====================================================
-- This script removes all objects created by create.service.user.sql
-- =====================================================
-- WARNING: This will permanently delete the service user, role, warehouse,
-- database, and schema. Ensure you have backups if needed!
-- =====================================================

-- =====================================================
-- 1. Revoke Role from User (as SECURITYADMIN)
-- =====================================================

USE ROLE SECURITYADMIN;

-- Revoke the role from the service user
REVOKE ROLE ETL_SERVICE_ROLE FROM USER ETL_SERVICE_USER;

-- =====================================================
-- 2. Drop Service User (as USERADMIN)
-- =====================================================

USE ROLE USERADMIN;

-- Drop the service user
DROP USER IF EXISTS ETL_SERVICE_USER;

-- =====================================================
-- 3. Revoke All Grants from Role (as SECURITYADMIN)
-- =====================================================

USE ROLE SECURITYADMIN;

-- Revoke warehouse privileges
REVOKE USAGE ON WAREHOUSE ETL_WH FROM ROLE ETL_SERVICE_ROLE;
REVOKE OPERATE ON WAREHOUSE ETL_WH FROM ROLE ETL_SERVICE_ROLE;

-- Revoke database and schema privileges
REVOKE USAGE ON DATABASE ETL_DB FROM ROLE ETL_SERVICE_ROLE;
REVOKE USAGE ON SCHEMA ETL_DB.ETL_SCHEMA FROM ROLE ETL_SERVICE_ROLE;
REVOKE CREATE TABLE ON SCHEMA ETL_DB.ETL_SCHEMA FROM ROLE ETL_SERVICE_ROLE;
REVOKE CREATE VIEW ON SCHEMA ETL_DB.ETL_SCHEMA FROM ROLE ETL_SERVICE_ROLE;
REVOKE CREATE STAGE ON SCHEMA ETL_DB.ETL_SCHEMA FROM ROLE ETL_SERVICE_ROLE;
REVOKE CREATE FILE FORMAT ON SCHEMA ETL_DB.ETL_SCHEMA FROM ROLE ETL_SERVICE_ROLE;
REVOKE CREATE PIPE ON SCHEMA ETL_DB.ETL_SCHEMA FROM ROLE ETL_SERVICE_ROLE;

-- Revoke table privileges
REVOKE SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA ETL_DB.ETL_SCHEMA FROM ROLE ETL_SERVICE_ROLE;
REVOKE SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON FUTURE TABLES IN SCHEMA ETL_DB.ETL_SCHEMA FROM ROLE ETL_SERVICE_ROLE;

-- =====================================================
-- 4. Drop Role (as SECURITYADMIN)
-- =====================================================

DROP ROLE IF EXISTS ETL_SERVICE_ROLE;

-- =====================================================
-- 5. Drop Database Objects (as SYSADMIN)
-- =====================================================

USE ROLE SYSADMIN;

-- Drop schema (CASCADE removes all contained objects)
DROP SCHEMA IF EXISTS ETL_DB.ETL_SCHEMA CASCADE;

-- Drop database (CASCADE removes all schemas and objects)
DROP DATABASE IF EXISTS ETL_DB CASCADE;

-- =====================================================
-- 6. Drop Warehouse (as SYSADMIN)
-- =====================================================

DROP WAREHOUSE IF EXISTS ETL_WH;

-- =====================================================
-- 7. Verify Cleanup
-- =====================================================

-- Verify user is removed (as ACCOUNTADMIN to see all users)
USE ROLE ACCOUNTADMIN;
SHOW USERS LIKE 'ETL_SERVICE_USER';  -- Should return no results

-- Verify role is removed
SHOW ROLES LIKE 'ETL_SERVICE_ROLE';  -- Should return no results

-- Verify database objects are removed
USE ROLE SYSADMIN;
SHOW DATABASES LIKE 'ETL_DB';        -- Should return no results
SHOW WAREHOUSES LIKE 'ETL_WH';       -- Should return no results

-- Display cleanup status
SELECT 'Service user cleanup complete!' AS status,
       'All ETL service account objects have been removed' AS message;

-- =====================================================
-- Cleanup Complete
-- =====================================================

/*
OBJECTS REMOVED:
- User: ETL_SERVICE_USER (service account)
- Role: ETL_SERVICE_ROLE
- Warehouse: ETL_WH
- Database: ETL_DB
- Schema: ETL_DB.ETL_SCHEMA
- All grants to: ETL_SERVICE_ROLE

RETENTION PERIOD:
- Dropped objects are retained for DATA_RETENTION_TIME_IN_DAYS
- They can be restored using UNDROP commands during retention period
- After retention expires, objects are permanently purged

TO RESTORE (within retention period):
  USE ROLE ACCOUNTADMIN;
  UNDROP USER ETL_SERVICE_USER;
  UNDROP ROLE ETL_SERVICE_ROLE;
  UNDROP DATABASE ETL_DB;
  UNDROP WAREHOUSE ETL_WH;
*/

