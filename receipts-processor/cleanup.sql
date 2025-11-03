-- ============================================================================
-- Receipts Processing - Cleanup Script
-- ============================================================================
-- This script removes all database objects created for the receipts processing
-- project, including tables, views, streams, stages, schemas, databases, and warehouses.
-- ============================================================================
-- WARNING: This script will permanently delete data and objects!
-- ============================================================================

-- ============================================================================
-- 1. Drop Notebooks (as SYSADMIN)
-- ============================================================================

USE ROLE SYSADMIN;
USE DATABASE RECEIPTS_PROCESSING_DB;
USE SCHEMA PUBLIC;

-- Drop notebooks
DROP NOTEBOOK IF EXISTS receipts_extractor;
DROP NOTEBOOK IF EXISTS receipts_extractor_ai_extract;

-- ============================================================================
-- 2. Drop Views (as SYSADMIN)
-- ============================================================================

USE SCHEMA RAW;

-- Drop analytics views
DROP VIEW IF EXISTS receipt_analytics_vw;
DROP VIEW IF EXISTS receipt_analytics_ai_extract_vw;

-- ============================================================================
-- 3. Drop Tables (as SYSADMIN)
-- ============================================================================

-- Drop extracted receipt data tables
DROP TABLE IF EXISTS RECEIPTS_PROCESSING_DB.RAW.extracted_receipt_data;
DROP TABLE IF EXISTS RECEIPTS_PROCESSING_DB.RAW.extracted_receipt_data_via_ai_extract;

-- Drop parsed receipts table
DROP TABLE IF EXISTS RECEIPTS_PROCESSING_DB.RAW.parsed_receipts;

-- ============================================================================
-- 4. Drop Task (as SYSADMIN)
-- ============================================================================

-- Suspend task first (if it's running)
ALTER TASK IF EXISTS RECEIPTS_PROCESSING_DB.RAW.AUTO_PROCESS_NEW_RECEIPTS SUSPEND;

-- Drop the task
DROP TASK IF EXISTS RECEIPTS_PROCESSING_DB.RAW.AUTO_PROCESS_NEW_RECEIPTS;

-- ============================================================================
-- 5. Drop Stream (as SYSADMIN)
-- ============================================================================

DROP STREAM IF EXISTS RECEIPTS_PROCESSING_DB.RAW.RECEIPTS_STREAM;

-- ============================================================================
-- 6. Drop Stages (as SYSADMIN)
-- ============================================================================

-- Remove all files from stages first (optional - uncomment if needed)
-- REMOVE @RECEIPTS_PROCESSING_DB.RAW.RECEIPTS;
-- REMOVE @RECEIPTS_PROCESSING_DB.PUBLIC.NOTEBOOKS;

-- Drop the receipt files stage
DROP STAGE IF EXISTS RECEIPTS_PROCESSING_DB.RAW.RECEIPTS;

-- Drop the notebooks stage
DROP STAGE IF EXISTS RECEIPTS_PROCESSING_DB.PUBLIC.NOTEBOOKS;

-- ============================================================================
-- 7. Drop Schema (as SYSADMIN)
-- ============================================================================

DROP SCHEMA IF EXISTS RECEIPTS_PROCESSING_DB.RAW CASCADE;

-- ============================================================================
-- 8. Drop Database (as SYSADMIN)
-- ============================================================================

DROP DATABASE IF EXISTS RECEIPTS_PROCESSING_DB CASCADE;

-- ============================================================================
-- 9. Drop Warehouses (as SYSADMIN)
-- ============================================================================

DROP WAREHOUSE IF EXISTS RECEIPTS_PARSE_COMPLETE_WH;
DROP WAREHOUSE IF EXISTS RECEIPTS_AI_EXTRACT_WH;

-- ============================================================================
-- 10. Revoke Grants (as ACCOUNTADMIN) - Optional
-- ============================================================================

USE ROLE ACCOUNTADMIN;

-- Revoke grants from ETL_SERVICE_ROLE
REVOKE USAGE ON WAREHOUSE RECEIPTS_PARSE_COMPLETE_WH FROM ROLE ETL_SERVICE_ROLE;
REVOKE USAGE ON WAREHOUSE RECEIPTS_AI_EXTRACT_WH FROM ROLE ETL_SERVICE_ROLE;
REVOKE USAGE ON DATABASE RECEIPTS_PROCESSING_DB FROM ROLE ETL_SERVICE_ROLE;
REVOKE USAGE ON SCHEMA RECEIPTS_PROCESSING_DB.RAW FROM ROLE ETL_SERVICE_ROLE;
REVOKE CREATE TABLE ON SCHEMA RECEIPTS_PROCESSING_DB.RAW FROM ROLE ETL_SERVICE_ROLE;
REVOKE CREATE VIEW ON SCHEMA RECEIPTS_PROCESSING_DB.RAW FROM ROLE ETL_SERVICE_ROLE;
REVOKE CREATE STREAM ON SCHEMA RECEIPTS_PROCESSING_DB.RAW FROM ROLE ETL_SERVICE_ROLE;
REVOKE READ ON STAGE RECEIPTS_PROCESSING_DB.RAW.RECEIPTS FROM ROLE ETL_SERVICE_ROLE;
REVOKE WRITE ON STAGE RECEIPTS_PROCESSING_DB.RAW.RECEIPTS FROM ROLE ETL_SERVICE_ROLE;
REVOKE ALL PRIVILEGES ON STAGE RECEIPTS_PROCESSING_DB.RAW.RECEIPTS FROM ROLE ETL_SERVICE_ROLE;
REVOKE SELECT ON STREAM RECEIPTS_PROCESSING_DB.RAW.RECEIPTS_STREAM FROM ROLE ETL_SERVICE_ROLE;

-- ============================================================================
-- 9. Verify Cleanup
-- ============================================================================

USE ROLE SYSADMIN;

-- Verify all objects are removed
SHOW WAREHOUSES LIKE 'RECEIPTS_%';               -- Should return no results
SHOW DATABASES LIKE 'RECEIPTS_PROCESSING_DB';    -- Should return no results

-- Display cleanup status
SELECT 'Cleanup complete!' AS status,
       'All receipts processing objects have been removed' AS message;

-- ============================================================================
-- Cleanup Complete
-- ============================================================================

/*
OBJECTS REMOVED:
- Warehouses: 
  * RECEIPTS_PARSE_COMPLETE_WH (for AI_COMPLETE processing)
  * RECEIPTS_AI_EXTRACT_WH (for AI_EXTRACT processing)
- Database: RECEIPTS_PROCESSING_DB
- Schemas: RAW, PUBLIC
- Stages:
  * RECEIPTS_PROCESSING_DB.RAW.RECEIPTS (receipt PDF files)
  * RECEIPTS_PROCESSING_DB.PUBLIC.NOTEBOOKS (notebook files)
- Notebooks:
  * receipts_extractor (AI_COMPLETE approach)
  * receipts_extractor_ai_extract (AI_EXTRACT approach)
- Stream: RECEIPTS_PROCESSING_DB.RAW.RECEIPTS_STREAM
- Task: RECEIPTS_PROCESSING_DB.RAW.AUTO_PROCESS_NEW_RECEIPTS
- Tables:
  * parsed_receipts
  * extracted_receipt_data
  * extracted_receipt_data_via_ai_extract
- Views:
  * receipt_analytics_vw
  * receipt_analytics_ai_extract_vw
- Grants to: ETL_SERVICE_ROLE

NOTE: This script does NOT drop the ETL_SERVICE_ROLE itself.
If you want to remove the role, run:
  USE ROLE ACCOUNTADMIN;
  DROP ROLE IF EXISTS ETL_SERVICE_ROLE;
*/

