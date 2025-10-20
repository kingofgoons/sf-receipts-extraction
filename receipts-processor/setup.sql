-- ============================================================================
-- Receipts Processing - Database Setup
-- ============================================================================
-- This script sets up the database, schema, and stage for receipt processing
-- and grants necessary permissions to the ETL_SERVICE_ROLE
-- ============================================================================

USE ROLE ACCOUNTADMIN;

-- ============================================================================
-- 1. Create Database and Schema
-- ============================================================================

-- Create the main database for receipt processing
CREATE DATABASE IF NOT EXISTS RECEIPTS_PROCESSING_DB
  COMMENT = 'Database for processing ad-campaign receipts';

-- Use the database
USE DATABASE RECEIPTS_PROCESSING_DB;

-- Create the RAW schema for landing receipt files
CREATE SCHEMA IF NOT EXISTS RAW
  COMMENT = 'Raw schema for receipt file landing zone';

-- Use the schema
USE SCHEMA RAW;

-- ============================================================================
-- 2. Create Stage for Receipt Files
-- ============================================================================

-- Create internal stage for receipt PDFs
CREATE STAGE IF NOT EXISTS RECEIPTS
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'Stage for storing receipt PDF files with directory table enabled';

-- Refresh the stage metadata to initialize the directory table
ALTER STAGE RECEIPTS REFRESH;

-- ============================================================================
-- 3. Grant Permissions to ETL_SERVICE_ROLE
-- ============================================================================

-- Grant database usage
GRANT USAGE ON DATABASE RECEIPTS_PROCESSING_DB TO ROLE ETL_SERVICE_ROLE;

-- Grant schema usage and create permissions
GRANT USAGE ON SCHEMA RECEIPTS_PROCESSING_DB.RAW TO ROLE ETL_SERVICE_ROLE;
GRANT CREATE TABLE ON SCHEMA RECEIPTS_PROCESSING_DB.RAW TO ROLE ETL_SERVICE_ROLE;
GRANT CREATE VIEW ON SCHEMA RECEIPTS_PROCESSING_DB.RAW TO ROLE ETL_SERVICE_ROLE;
GRANT CREATE STREAM ON SCHEMA RECEIPTS_PROCESSING_DB.RAW TO ROLE ETL_SERVICE_ROLE;

-- Grant stage permissions (READ and WRITE for file operations)
GRANT READ ON STAGE RECEIPTS_PROCESSING_DB.RAW.RECEIPTS TO ROLE ETL_SERVICE_ROLE;
GRANT WRITE ON STAGE RECEIPTS_PROCESSING_DB.RAW.RECEIPTS TO ROLE ETL_SERVICE_ROLE;

-- Grant all privileges on the stage for full control
GRANT ALL PRIVILEGES ON STAGE RECEIPTS_PROCESSING_DB.RAW.RECEIPTS TO ROLE ETL_SERVICE_ROLE;

-- ============================================================================
-- 4. Verify Setup
-- ============================================================================

-- Show created objects
SHOW DATABASES LIKE 'RECEIPTS_PROCESSING_DB';
SHOW SCHEMAS IN DATABASE RECEIPTS_PROCESSING_DB;
SHOW STAGES IN SCHEMA RECEIPTS_PROCESSING_DB.RAW;

-- Show grants for ETL_SERVICE_ROLE
SHOW GRANTS TO ROLE ETL_SERVICE_ROLE;

-- ============================================================================
-- 5. Optional: Create Stream on Stage for Automated Processing
-- ============================================================================

-- Create a stream to track new files added to the stage
CREATE STREAM IF NOT EXISTS RECEIPTS_STREAM 
  ON STAGE RECEIPTS_PROCESSING_DB.RAW.RECEIPTS
  COMMENT = 'Stream to track new receipt files uploaded to the stage';

-- Grant permissions on the stream
GRANT SELECT ON STREAM RECEIPTS_PROCESSING_DB.RAW.RECEIPTS_STREAM TO ROLE ETL_SERVICE_ROLE;

-- ============================================================================
-- Setup Complete
-- ============================================================================

-- Display summary
SELECT 'Setup complete!' AS status,
       'RECEIPTS_PROCESSING_DB' AS database_name,
       'RAW' AS schema_name,
       'RECEIPTS' AS stage_name,
       'RECEIPTS_STREAM' AS stream_name,
       'ETL_SERVICE_ROLE' AS role_with_access;

-- ============================================================================
-- Usage Examples
-- ============================================================================

/*
-- To upload files to the stage (from SnowSQL or Python):
PUT file:///path/to/receipt.pdf @RECEIPTS_PROCESSING_DB.RAW.RECEIPTS;

-- To list files in the stage:
LIST @RECEIPTS_PROCESSING_DB.RAW.RECEIPTS;

-- To query the directory table:
SELECT * FROM DIRECTORY(@RECEIPTS_PROCESSING_DB.RAW.RECEIPTS);

-- To check for new files in the stream:
SELECT * FROM RECEIPTS_PROCESSING_DB.RAW.RECEIPTS_STREAM;

-- To remove a file from the stage:
REMOVE @RECEIPTS_PROCESSING_DB.RAW.RECEIPTS/receipt_filename.pdf;
*/

