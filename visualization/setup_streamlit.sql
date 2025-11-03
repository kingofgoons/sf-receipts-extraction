-- ============================================================================
-- Streamlit App Setup for Cost Comparison Dashboard
-- ============================================================================
-- This script creates the Streamlit app in Snowflake
-- ============================================================================

USE ROLE SYSADMIN;
USE DATABASE RECEIPTS_PROCESSING_DB;
USE SCHEMA PUBLIC;

-- ============================================================================
-- 1. Create Streamlit App Stage (if using file-based approach)
-- ============================================================================

CREATE STAGE IF NOT EXISTS STREAMLIT_APPS
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'Stage for Streamlit app files';

-- Upload the Streamlit app file
-- PUT file://visualization/extraction_cost_comparison.py @RECEIPTS_PROCESSING_DB.PUBLIC.STREAMLIT_APPS AUTO_COMPRESS=FALSE;

-- ============================================================================
-- 2. Create Streamlit App
-- ============================================================================

CREATE OR REPLACE STREAMLIT extraction_cost_dashboard
  ROOT_LOCATION = '@RECEIPTS_PROCESSING_DB.PUBLIC.STREAMLIT_APPS'
  MAIN_FILE = 'extraction_cost_comparison.py'
  QUERY_WAREHOUSE = 'RECEIPTS_PARSE_COMPLETE_WH'
  COMMENT = 'Dashboard to compare AI_COMPLETE vs AI_EXTRACT extraction costs';

-- ============================================================================
-- 3. Grant Permissions
-- ============================================================================

USE ROLE ACCOUNTADMIN;

-- Grant usage to SYSADMIN
GRANT USAGE ON STREAMLIT RECEIPTS_PROCESSING_DB.PUBLIC.extraction_cost_dashboard 
  TO ROLE SYSADMIN;

-- Grant usage to ETL_SERVICE_ROLE
GRANT USAGE ON STREAMLIT RECEIPTS_PROCESSING_DB.PUBLIC.extraction_cost_dashboard 
  TO ROLE ETL_SERVICE_ROLE;

-- Grant access to ACCOUNT_USAGE views (required for cost data)
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE SYSADMIN;
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE ETL_SERVICE_ROLE;

-- ============================================================================
-- 4. Verify Setup
-- ============================================================================

USE ROLE SYSADMIN;

-- Show the Streamlit app
SHOW STREAMLITS LIKE 'extraction_cost_dashboard' IN SCHEMA RECEIPTS_PROCESSING_DB.PUBLIC;

-- ============================================================================
-- 5. Access the Dashboard
-- ============================================================================

/*
To access the dashboard:

1. In Snowsight, navigate to:
   Projects » Streamlit » extraction_cost_dashboard

2. Or get the URL:
   SELECT SYSTEM$GET_STREAMLIT_URL('RECEIPTS_PROCESSING_DB.PUBLIC.extraction_cost_dashboard');

3. Share with others:
   GRANT USAGE ON STREAMLIT RECEIPTS_PROCESSING_DB.PUBLIC.extraction_cost_dashboard TO ROLE <ROLE_NAME>;

*/

-- ============================================================================
-- Setup Complete
-- ============================================================================

SELECT 'Streamlit app created!' AS status,
       'extraction_cost_dashboard' AS app_name,
       'RECEIPTS_PROCESSING_DB.PUBLIC' AS location,
       'Navigate to Projects » Streamlit in Snowsight' AS access_instructions;

