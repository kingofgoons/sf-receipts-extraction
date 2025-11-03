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

-- Create dedicated warehouse for receipt parsing and AI_COMPLETE (parse.and.complete approach)
CREATE WAREHOUSE IF NOT EXISTS RECEIPTS_PARSE_COMPLETE_WH
  WITH 
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Warehouse for AI_PARSE_DOCUMENT + AI_COMPLETE extraction (receipts-extractor.ipynb)';

-- Create dedicated warehouse for AI_EXTRACT (direct PDF processing)
CREATE WAREHOUSE IF NOT EXISTS RECEIPTS_AI_EXTRACT_WH
  WITH 
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Warehouse for AI_EXTRACT direct PDF processing (receipts-extractor_ai_extract.ipynb)';

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
-- 3. Create Stages
-- ============================================================================

-- Create internal stage for receipt PDFs (in RAW schema)
USE SCHEMA RAW;

CREATE STAGE IF NOT EXISTS RECEIPTS
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'Stage for storing receipt PDF files with directory table enabled';

-- Refresh the stage metadata to initialize the directory table
ALTER STAGE RECEIPTS REFRESH;

-- Create stage for notebook files (in PUBLIC schema)
USE SCHEMA PUBLIC;

CREATE STAGE IF NOT EXISTS NOTEBOOKS
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'Stage for storing notebook .ipynb files for programmatic deployment';

ALTER STAGE NOTEBOOKS REFRESH;

-- ============================================================================
-- 4. Grant Permissions to ETL_SERVICE_ROLE (as ACCOUNTADMIN)
-- ============================================================================

USE ROLE ACCOUNTADMIN;

-- Grant warehouse usage for receipt processing (both warehouses)
GRANT USAGE ON WAREHOUSE RECEIPTS_PARSE_COMPLETE_WH TO ROLE ETL_SERVICE_ROLE;
GRANT USAGE ON WAREHOUSE RECEIPTS_PARSE_COMPLETE_WH TO ROLE SYSADMIN;
GRANT USAGE ON WAREHOUSE RECEIPTS_AI_EXTRACT_WH TO ROLE ETL_SERVICE_ROLE;
GRANT USAGE ON WAREHOUSE RECEIPTS_AI_EXTRACT_WH TO ROLE SYSADMIN;

-- Grant database usage
GRANT USAGE ON DATABASE RECEIPTS_PROCESSING_DB TO ROLE ETL_SERVICE_ROLE;
GRANT USAGE ON DATABASE RECEIPTS_PROCESSING_DB TO ROLE SYSADMIN;

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
-- Note: The notebook 'receipts-extractor_ai_extract' must exist in RECEIPTS_PROCESSING_DB.PUBLIC
CREATE TASK IF NOT EXISTS AUTO_PROCESS_NEW_RECEIPTS
  WAREHOUSE = RECEIPTS_AI_EXTRACT_WH
  SCHEDULE = '1 MINUTE'
  COMMENT = 'Automatically process new receipt files using AI_EXTRACT notebook'
  WHEN SYSTEM$STREAM_HAS_DATA('RECEIPTS_STREAM')
AS
  EXECUTE NOTEBOOK RECEIPTS_PROCESSING_DB.PUBLIC.receipts_extractor_ai_extract();

-- Grant permissions on the task (as ACCOUNTADMIN)
USE ROLE ACCOUNTADMIN;
GRANT OWNERSHIP ON TASK RECEIPTS_PROCESSING_DB.RAW.AUTO_PROCESS_NEW_RECEIPTS TO ROLE ETL_SERVICE_ROLE;

-- Note: The task is created in SUSPENDED state by default
-- To start automated processing, run:
-- ALTER TASK RECEIPTS_PROCESSING_DB.RAW.AUTO_PROCESS_NEW_RECEIPTS RESUME;

-- ============================================================================
-- 7. Upload and Create Notebooks
-- ============================================================================

-- Step 1: Upload notebook files to the NOTEBOOKS stage
-- Organize notebooks in subdirectories for better separation
-- Run these commands from your local machine using SnowSQL:
/*
-- Upload AI_COMPLETE notebook and environment.yml to parse_and_complete/ directory
PUT file://receipts-processor/parse.and.complete/receipts-extractor.ipynb 
  @RECEIPTS_PROCESSING_DB.PUBLIC.NOTEBOOKS/parse_and_complete/ 
  AUTO_COMPRESS=FALSE;
PUT file://receipts-processor/parse.and.complete/environment.yml 
  @RECEIPTS_PROCESSING_DB.PUBLIC.NOTEBOOKS/parse_and_complete/ 
  AUTO_COMPRESS=FALSE;

-- Upload AI_EXTRACT notebook to ai_extract/ directory
PUT file://receipts-processor/ai.extract/receipts-extractor_ai_extract.ipynb 
  @RECEIPTS_PROCESSING_DB.PUBLIC.NOTEBOOKS/ai_extract/ 
  AUTO_COMPRESS=FALSE;

-- Or from Snowsight, manually upload files to their respective subdirectories in the NOTEBOOKS stage

-- Verify files are uploaded
LIST @RECEIPTS_PROCESSING_DB.PUBLIC.NOTEBOOKS/parse_and_complete/;
LIST @RECEIPTS_PROCESSING_DB.PUBLIC.NOTEBOOKS/ai_extract/;
*/

-- Step 2: Create notebooks from uploaded files in their subdirectories
USE ROLE SYSADMIN;
USE DATABASE RECEIPTS_PROCESSING_DB;
USE SCHEMA PUBLIC;

-- Create AI_COMPLETE notebook (uses AI_PARSE_DOCUMENT + AI_COMPLETE)
CREATE NOTEBOOK IF NOT EXISTS receipts_extractor
  FROM '@RECEIPTS_PROCESSING_DB.PUBLIC.NOTEBOOKS/parse_and_complete'
  MAIN_FILE = 'receipts-extractor.ipynb'
  QUERY_WAREHOUSE = 'RECEIPTS_PARSE_COMPLETE_WH'
  COMMENT = 'Receipt extraction using AI_PARSE_DOCUMENT + AI_COMPLETE approach (includes environment.yml)';

-- Create AI_EXTRACT notebook (direct PDF processing)
CREATE NOTEBOOK IF NOT EXISTS receipts_extractor_ai_extract
  FROM '@RECEIPTS_PROCESSING_DB.PUBLIC.NOTEBOOKS/ai_extract'
  MAIN_FILE = 'receipts-extractor_ai_extract.ipynb'
  QUERY_WAREHOUSE = 'RECEIPTS_AI_EXTRACT_WH'
  COMMENT = 'Receipt extraction using AI_EXTRACT direct PDF approach';

-- Grant permissions on notebooks to ETL_SERVICE_ROLE
USE ROLE ACCOUNTADMIN;
GRANT OWNERSHIP ON NOTEBOOK RECEIPTS_PROCESSING_DB.PUBLIC.receipts_extractor TO ROLE ETL_SERVICE_ROLE;
GRANT OWNERSHIP ON NOTEBOOK RECEIPTS_PROCESSING_DB.PUBLIC.receipts_extractor_ai_extract TO ROLE ETL_SERVICE_ROLE;

-- ============================================================================
-- 8. Verify Setup
-- ============================================================================

USE ROLE SYSADMIN;

-- Show created objects
SHOW WAREHOUSES LIKE 'RECEIPTS_%';
SHOW DATABASES LIKE 'RECEIPTS_PROCESSING_DB';
SHOW SCHEMAS IN DATABASE RECEIPTS_PROCESSING_DB;
SHOW STAGES IN SCHEMA RECEIPTS_PROCESSING_DB.RAW;
SHOW STAGES IN SCHEMA RECEIPTS_PROCESSING_DB.PUBLIC;
SHOW NOTEBOOKS IN SCHEMA RECEIPTS_PROCESSING_DB.PUBLIC;
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
       'RECEIPTS_PARSE_COMPLETE_WH, RECEIPTS_AI_EXTRACT_WH' AS warehouses,
       'RECEIPTS_PROCESSING_DB' AS database_name,
       'RAW, PUBLIC' AS schemas,
       'RECEIPTS (RAW), NOTEBOOKS (PUBLIC)' AS stages,
       'receipts_extractor, receipts_extractor_ai_extract' AS notebooks,
       'RECEIPTS_STREAM' AS stream_name,
       'AUTO_PROCESS_NEW_RECEIPTS' AS task_name,
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

