-- ============================================================================
-- Receipts Processing - Database Setup
-- ============================================================================
-- This script sets up the database, schema, and stage for receipt processing
-- and grants necessary permissions to the ETL_SERVICE_ROLE
-- ============================================================================
-- Best Practice: Use SYSADMIN for object creation, ACCOUNTADMIN only for grants
-- ============================================================================

-- ============================================================================
-- 1. Create Warehouse for Receipt Processing (as SYSADMIN)
-- ============================================================================

USE ROLE SYSADMIN;

-- Create dedicated warehouse for receipt parsing and AI completion
CREATE WAREHOUSE IF NOT EXISTS RECEIPTS_PARSE_COMPLETE_WH
  WITH 
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Warehouse for receipts-extractor notebook AI parsing and completion';

-- ============================================================================
-- 2. Create Database and Schema (as SYSADMIN)
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
-- 3. Create Stage for Receipt Files
-- ============================================================================

-- Create internal stage for receipt PDFs
CREATE STAGE IF NOT EXISTS RECEIPTS
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'Stage for storing receipt PDF files with directory table enabled';

-- Refresh the stage metadata to initialize the directory table
ALTER STAGE RECEIPTS REFRESH;

-- ============================================================================
-- 4. Grant Permissions to ETL_SERVICE_ROLE (as ACCOUNTADMIN)
-- ============================================================================

USE ROLE ACCOUNTADMIN;

-- Grant warehouse usage for receipt processing
GRANT USAGE ON WAREHOUSE RECEIPTS_PARSE_COMPLETE_WH TO ROLE ETL_SERVICE_ROLE;

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
-- 5. Optional: Create Stream on Stage for Automated Processing (as SYSADMIN)
-- ============================================================================

USE ROLE SYSADMIN;
USE DATABASE RECEIPTS_PROCESSING_DB;
USE SCHEMA RAW;

-- Create a stream to track new files added to the stage
CREATE STREAM IF NOT EXISTS RECEIPTS_STREAM 
  ON STAGE RECEIPTS_PROCESSING_DB.RAW.RECEIPTS
  COMMENT = 'Stream to track new receipt files uploaded to the stage';

-- Grant permissions on the stream (as ACCOUNTADMIN)
USE ROLE ACCOUNTADMIN;
GRANT SELECT ON STREAM RECEIPTS_PROCESSING_DB.RAW.RECEIPTS_STREAM TO ROLE ETL_SERVICE_ROLE;

-- Grant task execution permissions
GRANT EXECUTE TASK ON ACCOUNT TO ROLE ETL_SERVICE_ROLE;
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO ROLE ETL_SERVICE_ROLE;

-- Grant schema permissions for task creation (switch to SYSADMIN)
USE ROLE SYSADMIN;
GRANT CREATE TASK ON SCHEMA RECEIPTS_PROCESSING_DB.RAW TO ROLE ETL_SERVICE_ROLE;

-- ============================================================================
-- 6. Create Automated Processing Task
-- ============================================================================
-- This task automatically executes the AI_EXTRACT notebook when new files arrive

USE ROLE SYSADMIN;
USE DATABASE RECEIPTS_PROCESSING_DB;
USE SCHEMA RAW;

-- Create task to process new receipts automatically
-- Note: The notebook 'receipts-extractor_ai_extract' must exist in RECEIPTS_PROCESSING_DB.RAW
CREATE TASK IF NOT EXISTS AUTO_PROCESS_NEW_RECEIPTS
  WAREHOUSE = RECEIPTS_PARSE_COMPLETE_WH
  SCHEDULE = '1 MINUTE'
  COMMENT = 'Automatically process new receipt files using AI_EXTRACT notebook'
  WHEN SYSTEM$STREAM_HAS_DATA('RECEIPTS_STREAM')
AS
  EXECUTE NOTEBOOK RECEIPTS_PROCESSING_DB.RAW.receipts_extractor_ai_extract();

-- Grant permissions on the task (as ACCOUNTADMIN)
USE ROLE ACCOUNTADMIN;
GRANT OWNERSHIP ON TASK RECEIPTS_PROCESSING_DB.RAW.AUTO_PROCESS_NEW_RECEIPTS TO ROLE ETL_SERVICE_ROLE;

-- Note: The task is created in SUSPENDED state by default
-- To start automated processing, run:
-- ALTER TASK RECEIPTS_PROCESSING_DB.RAW.AUTO_PROCESS_NEW_RECEIPTS RESUME;

-- ============================================================================
-- 7. Verify Setup
-- ============================================================================

USE ROLE SYSADMIN;

-- Show created objects
SHOW WAREHOUSES LIKE 'RECEIPTS_PARSE_COMPLETE_WH';
SHOW DATABASES LIKE 'RECEIPTS_PROCESSING_DB';
SHOW SCHEMAS IN DATABASE RECEIPTS_PROCESSING_DB;
SHOW STAGES IN SCHEMA RECEIPTS_PROCESSING_DB.RAW;
SHOW STREAMS IN SCHEMA RECEIPTS_PROCESSING_DB.RAW;
SHOW TASKS IN SCHEMA RECEIPTS_PROCESSING_DB.RAW;

-- Show grants for ETL_SERVICE_ROLE (requires ACCOUNTADMIN)
USE ROLE ACCOUNTADMIN;
SHOW GRANTS TO ROLE ETL_SERVICE_ROLE;

-- ============================================================================
-- Setup Complete
-- ============================================================================

-- Display summary
SELECT 'Setup complete!' AS status,
       'RECEIPTS_PARSE_COMPLETE_WH' AS warehouse_name,
       'RECEIPTS_PROCESSING_DB' AS database_name,
       'RAW' AS schema_name,
       'RECEIPTS' AS stage_name,
       'RECEIPTS_STREAM' AS stream_name,
       'AUTO_PROCESS_NEW_RECEIPTS' AS task_name,
       'receipts_extractor_ai_extract' AS notebook_name,
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

-- ============================================================================
-- Task Management
-- ============================================================================

-- Start automated processing (resume the task):
ALTER TASK RECEIPTS_PROCESSING_DB.RAW.AUTO_PROCESS_NEW_RECEIPTS RESUME;

-- Stop automated processing (suspend the task):
ALTER TASK RECEIPTS_PROCESSING_DB.RAW.AUTO_PROCESS_NEW_RECEIPTS SUSPEND;

-- Check task status:
SHOW TASKS LIKE 'AUTO_PROCESS_NEW_RECEIPTS' IN SCHEMA RECEIPTS_PROCESSING_DB.RAW;

-- View task execution history:
SELECT *
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
  SCHEDULED_TIME_RANGE_START => DATEADD('day', -7, CURRENT_TIMESTAMP()),
  TASK_NAME => 'AUTO_PROCESS_NEW_RECEIPTS'
))
ORDER BY SCHEDULED_TIME DESC;

-- Manually execute the notebook:
EXECUTE NOTEBOOK RECEIPTS_PROCESSING_DB.RAW.receipts_extractor_ai_extract();

-- Check if stream has data (new files):
SELECT SYSTEM$STREAM_HAS_DATA('RECEIPTS_PROCESSING_DB.RAW.RECEIPTS_STREAM');
*/

