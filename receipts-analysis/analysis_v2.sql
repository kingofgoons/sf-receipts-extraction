-- ============================================================================
-- Receipt Analytics Queries for V2 Receipts (Pricing Tables)
-- ============================================================================
-- This script contains analytical queries for V2 receipt data with pricing tables
-- Extracted by receipts-extractor.ipynb using prompt_text_v2 and resp_schema_v2
-- ============================================================================

USE ROLE SYSADMIN;
USE DATABASE RECEIPTS_PROCESSING_DB;
USE SCHEMA RAW;
USE WAREHOUSE RECEIPTS_PARSE_COMPLETE_WH;

-- ============================================================================
-- Prerequisite: Create Flattened View for V2 Pricing Tables
-- ============================================================================
-- Since V2 receipts have nested pricing_tables arrays, we need to flatten them first

CREATE OR REPLACE VIEW v2_pricing_flattened AS
SELECT
    e.relative_path AS receipt_filename,
    e.extracted_data:vendor.vendor_name::STRING AS vendor_name,
    e.extracted_data:transaction.transaction_id::STRING AS transaction_id,
    TRY_TO_DATE(e.extracted_data:transaction.date::STRING) AS transaction_date,
    e.extracted_data:transaction.payment_method::STRING AS payment_method,
    e.extracted_data:customer.company_name::STRING AS company_name,
    e.extracted_data:campaign.name::STRING AS campaign_name,
    TRY_TO_DECIMAL(REPLACE(REPLACE(e.extracted_data:financials.subtotal::STRING, '$', ''), ',', ''), 10, 2) AS subtotal,
    TRY_TO_DECIMAL(REPLACE(REPLACE(e.extracted_data:financials.tax::STRING, '$', ''), ',', ''), 10, 2) AS tax,
    TRY_TO_DECIMAL(REPLACE(REPLACE(e.extracted_data:financials.total::STRING, '$', ''), ',', ''), 10, 2) AS total,
    -- Flatten pricing_tables array
    pt.value:table_name::STRING AS pricing_table_name,
    -- Flatten markets within each pricing table
    m.value:market::STRING AS market,
    TRY_TO_DECIMAL(REPLACE(REPLACE(m.value:minimum_usd::STRING, '$', ''), ',', ''), 10, 2) AS minimum_usd,
    TRY_TO_DECIMAL(REPLACE(REPLACE(m.value:reach::STRING, ',', ''), ',', ''), 38, 0) AS reach
FROM extracted_receipt_data e,
    LATERAL FLATTEN(input => e.extracted_data:pricing_tables) pt,
    LATERAL FLATTEN(input => pt.value:markets) m;

-- ============================================================================
-- Analytics for V2 Receipts (Pricing Tables)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Spending Analysis by Vendor
-- ----------------------------------------------------------------------------
-- Analyze receipt count and total spending by vendor

SELECT 
    vendor_name,
    COUNT(DISTINCT receipt_filename) AS receipt_count,
    COUNT(*) AS total_market_entries,
    SUM(total) AS total_spending,
    AVG(total) AS avg_receipt_amount,
    SUM(minimum_usd) AS total_minimum_commitments,
    SUM(reach) AS total_reach
FROM v2_pricing_flattened
GROUP BY vendor_name
ORDER BY total_spending DESC;

-- ----------------------------------------------------------------------------
-- 2. Analysis by Pricing Table Type
-- ----------------------------------------------------------------------------
-- Compare different pricing models (Geographic, Demographic, Device, etc.)

SELECT 
    pricing_table_name,
    COUNT(DISTINCT receipt_filename) AS receipt_count,
    COUNT(*) AS total_markets,
    AVG(minimum_usd) AS avg_minimum_spend,
    SUM(minimum_usd) AS total_minimum_spend,
    AVG(reach) AS avg_reach,
    SUM(reach) AS total_reach
FROM v2_pricing_flattened
WHERE pricing_table_name IS NOT NULL
GROUP BY pricing_table_name
ORDER BY total_minimum_spend DESC;

-- ----------------------------------------------------------------------------
-- 3. Market Analysis by Region
-- ----------------------------------------------------------------------------
-- Identify most valuable markets and their reach

SELECT 
    market,
    COUNT(DISTINCT receipt_filename) AS receipt_count,
    COUNT(*) AS times_targeted,
    AVG(minimum_usd) AS avg_minimum_spend,
    SUM(minimum_usd) AS total_minimum_spend,
    AVG(reach) AS avg_reach,
    SUM(reach) AS total_reach
FROM v2_pricing_flattened
WHERE market IS NOT NULL
GROUP BY market
ORDER BY total_minimum_spend DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- 4. Cost per Thousand Reach (CPM Equivalent)
-- ----------------------------------------------------------------------------
-- Calculate effective cost per thousand reach for each market

SELECT 
    market,
    pricing_table_name,
    COUNT(*) AS occurrences,
    AVG(minimum_usd) AS avg_minimum_spend,
    AVG(reach) AS avg_reach,
    AVG(minimum_usd / NULLIF(reach, 0) * 1000) AS avg_cpm_equivalent
FROM v2_pricing_flattened
WHERE reach > 0 AND minimum_usd > 0
GROUP BY market, pricing_table_name
ORDER BY avg_cpm_equivalent ASC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- 5. Vendor Pricing Strategy Analysis
-- ----------------------------------------------------------------------------
-- Analyze which pricing table types each vendor uses

SELECT 
    vendor_name,
    pricing_table_name,
    COUNT(*) AS usage_count,
    AVG(minimum_usd) AS avg_minimum,
    SUM(minimum_usd) AS total_minimum
FROM v2_pricing_flattened
GROUP BY vendor_name, pricing_table_name
ORDER BY vendor_name, total_minimum DESC;

-- ----------------------------------------------------------------------------
-- 6. High-Value Markets
-- ----------------------------------------------------------------------------
-- Identify markets with highest minimum spend requirements

SELECT 
    market,
    pricing_table_name,
    vendor_name,
    campaign_name,
    minimum_usd,
    reach,
    minimum_usd / NULLIF(reach, 0) * 1000 AS cpm_equivalent,
    transaction_date
FROM v2_pricing_flattened
WHERE minimum_usd IS NOT NULL
ORDER BY minimum_usd DESC
LIMIT 25;

-- ----------------------------------------------------------------------------
-- 7. Reach Analysis
-- ----------------------------------------------------------------------------
-- Analyze potential audience reach by pricing table type

SELECT 
    pricing_table_name,
    COUNT(DISTINCT market) AS unique_markets,
    SUM(reach) AS total_potential_reach,
    AVG(reach) AS avg_market_reach,
    MAX(reach) AS max_market_reach,
    MIN(reach) AS min_market_reach
FROM v2_pricing_flattened
WHERE reach IS NOT NULL
GROUP BY pricing_table_name
ORDER BY total_potential_reach DESC;

-- ----------------------------------------------------------------------------
-- 8. Campaign Pricing Summary
-- ----------------------------------------------------------------------------
-- Summary of all pricing tables per campaign

SELECT 
    campaign_name,
    vendor_name,
    transaction_date,
    COUNT(DISTINCT pricing_table_name) AS num_pricing_tables,
    COUNT(*) AS total_markets,
    SUM(minimum_usd) AS total_minimum_spend,
    SUM(reach) AS total_reach,
    total AS invoice_total
FROM v2_pricing_flattened
GROUP BY campaign_name, vendor_name, transaction_date, total
ORDER BY total_minimum_spend DESC;

-- ----------------------------------------------------------------------------
-- 9. Monthly Trends
-- ----------------------------------------------------------------------------
-- Track spending and reach over time

SELECT 
    DATE_TRUNC('month', transaction_date) AS month,
    COUNT(DISTINCT receipt_filename) AS receipt_count,
    COUNT(*) AS total_market_entries,
    SUM(total) AS total_spending,
    SUM(minimum_usd) AS total_minimum_commitments,
    SUM(reach) AS total_reach
FROM v2_pricing_flattened
WHERE transaction_date IS NOT NULL
GROUP BY DATE_TRUNC('month', transaction_date)
ORDER BY month DESC;

-- ----------------------------------------------------------------------------
-- 10. Pricing Efficiency by Vendor
-- ----------------------------------------------------------------------------
-- Calculate cost efficiency (spend per reach) for each vendor

SELECT 
    vendor_name,
    COUNT(DISTINCT receipt_filename) AS receipt_count,
    SUM(minimum_usd) AS total_minimum_spend,
    SUM(reach) AS total_reach,
    SUM(minimum_usd) / NULLIF(SUM(reach), 0) * 1000 AS overall_cpm_equivalent,
    AVG(minimum_usd / NULLIF(reach, 0) * 1000) AS avg_market_cpm_equivalent
FROM v2_pricing_flattened
WHERE reach > 0 AND minimum_usd > 0
GROUP BY vendor_name
ORDER BY overall_cpm_equivalent ASC;

-- ============================================================================
-- Advanced Analytics for V2 Receipts
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 11. Market Combination Analysis
-- ----------------------------------------------------------------------------
-- Which markets are commonly grouped together in campaigns?

WITH market_pairs AS (
    SELECT DISTINCT
        receipt_filename,
        pricing_table_name,
        market
    FROM v2_pricing_flattened
)
SELECT 
    m1.market AS market_1,
    m2.market AS market_2,
    COUNT(DISTINCT m1.receipt_filename) AS co_occurrence_count,
    SUM(v2.minimum_usd) AS total_combined_spend
FROM market_pairs m1
JOIN market_pairs m2 
    ON m1.receipt_filename = m2.receipt_filename 
    AND m1.pricing_table_name = m2.pricing_table_name
    AND m1.market < m2.market
JOIN v2_pricing_flattened v2
    ON m1.receipt_filename = v2.receipt_filename
    AND m1.market = v2.market
WHERE m1.market != m2.market
GROUP BY m1.market, m2.market
HAVING co_occurrence_count >= 2
ORDER BY co_occurrence_count DESC, total_combined_spend DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- 12. Pricing Table Distribution per Receipt
-- ----------------------------------------------------------------------------
-- How many pricing tables does each receipt typically have?

SELECT 
    num_tables,
    COUNT(*) AS receipt_count,
    AVG(total_spending) AS avg_total_spending,
    AVG(total_markets) AS avg_markets_per_receipt
FROM (
    SELECT 
        receipt_filename,
        COUNT(DISTINCT pricing_table_name) AS num_tables,
        MAX(total) AS total_spending,
        COUNT(*) AS total_markets
    FROM v2_pricing_flattened
    GROUP BY receipt_filename
)
GROUP BY num_tables
ORDER BY num_tables;

-- ----------------------------------------------------------------------------
-- 13. Top Campaigns by Total Reach
-- ----------------------------------------------------------------------------
-- Campaigns with the highest potential audience reach

SELECT 
    campaign_name,
    vendor_name,
    company_name,
    transaction_date,
    COUNT(DISTINCT pricing_table_name) AS num_pricing_models,
    COUNT(*) AS num_markets,
    SUM(reach) AS total_potential_reach,
    SUM(minimum_usd) AS total_minimum_spend,
    SUM(minimum_usd) / NULLIF(SUM(reach), 0) * 1000 AS campaign_cpm_equivalent
FROM v2_pricing_flattened
GROUP BY campaign_name, vendor_name, company_name, transaction_date
ORDER BY total_potential_reach DESC
LIMIT 15;

-- ----------------------------------------------------------------------------
-- 14. Market Pricing Consistency Check
-- ----------------------------------------------------------------------------
-- Check if same markets have consistent pricing across receipts

SELECT 
    market,
    pricing_table_name,
    COUNT(*) AS occurrences,
    MIN(minimum_usd) AS min_price,
    MAX(minimum_usd) AS max_price,
    AVG(minimum_usd) AS avg_price,
    STDDEV(minimum_usd) AS price_stddev,
    AVG(reach) AS avg_reach
FROM v2_pricing_flattened
WHERE market IS NOT NULL AND minimum_usd IS NOT NULL
GROUP BY market, pricing_table_name
HAVING COUNT(*) >= 2
ORDER BY occurrences DESC, price_stddev DESC
LIMIT 20;

-- ============================================================================
-- Data Quality Checks for V2 Receipts
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 15. Extraction Completeness Check
-- ----------------------------------------------------------------------------

WITH receipt_summary AS (
    SELECT 
        receipt_filename,
        MAX(vendor_name) AS vendor_name,
        MAX(transaction_date) AS transaction_date,
        MAX(total) AS total,
        COUNT(DISTINCT pricing_table_name) AS num_tables,
        COUNT(*) AS num_markets
    FROM v2_pricing_flattened
    GROUP BY receipt_filename
)
SELECT 
    COUNT(*) AS total_receipts,
    SUM(CASE WHEN vendor_name IS NOT NULL THEN 1 ELSE 0 END) AS has_vendor,
    SUM(CASE WHEN transaction_date IS NOT NULL THEN 1 ELSE 0 END) AS has_date,
    SUM(CASE WHEN total IS NOT NULL THEN 1 ELSE 0 END) AS has_total,
    SUM(CASE WHEN num_tables > 0 THEN 1 ELSE 0 END) AS has_pricing_tables,
    AVG(num_tables) AS avg_tables_per_receipt,
    AVG(num_markets) AS avg_markets_per_receipt
FROM receipt_summary;

-- ----------------------------------------------------------------------------
-- 16. Missing or Invalid Data
-- ----------------------------------------------------------------------------

SELECT 
    receipt_filename,
    vendor_name,
    CASE WHEN transaction_date IS NULL THEN 'Missing date' END AS issue_date,
    CASE WHEN total IS NULL OR total = 0 THEN 'Missing/zero amount' END AS issue_amount,
    CASE WHEN campaign_name IS NULL THEN 'Missing campaign' END AS issue_campaign,
    CASE WHEN pricing_table_name IS NULL THEN 'Missing table name' END AS issue_table,
    CASE WHEN market IS NULL THEN 'Missing market' END AS issue_market
FROM v2_pricing_flattened
WHERE transaction_date IS NULL 
   OR total IS NULL 
   OR total = 0 
   OR campaign_name IS NULL
   OR pricing_table_name IS NULL
   OR market IS NULL
LIMIT 50;

-- ============================================================================
-- Business Intelligence Queries
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 17. Most Expensive Markets (by Minimum Spend)
-- ----------------------------------------------------------------------------

SELECT 
    market,
    COUNT(DISTINCT vendor_name) AS num_vendors,
    COUNT(*) AS times_offered,
    AVG(minimum_usd) AS avg_minimum_spend,
    MAX(minimum_usd) AS max_minimum_spend,
    AVG(reach) AS avg_reach
FROM v2_pricing_flattened
WHERE minimum_usd IS NOT NULL
GROUP BY market
ORDER BY avg_minimum_spend DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- 18. Best Value Markets (by CPM Equivalent)
-- ----------------------------------------------------------------------------
-- Markets with the best reach per dollar

SELECT 
    market,
    pricing_table_name,
    COUNT(*) AS occurrences,
    AVG(minimum_usd) AS avg_minimum_spend,
    AVG(reach) AS avg_reach,
    AVG(reach / NULLIF(minimum_usd, 0)) AS avg_reach_per_dollar,
    AVG(minimum_usd / NULLIF(reach, 0) * 1000) AS avg_cpm_equivalent
FROM v2_pricing_flattened
WHERE minimum_usd > 0 AND reach > 0
GROUP BY market, pricing_table_name
ORDER BY avg_reach_per_dollar DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- 19. Vendor Market Coverage
-- ----------------------------------------------------------------------------
-- Which vendors offer the most diverse market options?

SELECT 
    vendor_name,
    COUNT(DISTINCT market) AS unique_markets,
    COUNT(DISTINCT pricing_table_name) AS unique_table_types,
    COUNT(*) AS total_market_offerings,
    SUM(minimum_usd) AS total_minimum_commitments,
    SUM(reach) AS total_potential_reach
FROM v2_pricing_flattened
GROUP BY vendor_name
ORDER BY unique_markets DESC, total_potential_reach DESC;

-- ----------------------------------------------------------------------------
-- 20. Campaign Budget Allocation
-- ----------------------------------------------------------------------------
-- How do campaigns distribute budget across pricing tables and markets?

SELECT 
    campaign_name,
    vendor_name,
    pricing_table_name,
    COUNT(*) AS num_markets,
    SUM(minimum_usd) AS table_minimum_spend,
    SUM(reach) AS table_total_reach,
    MAX(total) AS campaign_total
FROM v2_pricing_flattened
GROUP BY campaign_name, vendor_name, pricing_table_name, total
ORDER BY campaign_name, table_minimum_spend DESC;

-- ============================================================================
-- Comparison: V2 Pricing Summary vs Invoice Total
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 21. Validate Pricing vs Invoice Total
-- ----------------------------------------------------------------------------
-- Check if sum of minimum spends aligns with invoice totals

SELECT 
    receipt_filename,
    vendor_name,
    campaign_name,
    SUM(minimum_usd) AS sum_of_minimums,
    MAX(subtotal) AS invoice_subtotal,
    MAX(total) AS invoice_total,
    MAX(subtotal) - SUM(minimum_usd) AS difference
FROM v2_pricing_flattened
GROUP BY receipt_filename, vendor_name, campaign_name
HAVING ABS(MAX(subtotal) - SUM(minimum_usd)) > 100
ORDER BY ABS(difference) DESC;

-- ============================================================================
-- End of V2 Analytics Queries
-- ============================================================================

/*
NOTE: These queries assume V2 receipts have been processed with:
  - prompt_text_v2
  - resp_schema_v2 or resp_schema_v2b
  
The pricing_tables structure:
{
  "pricing_tables": [
    {
      "table_name": "Geographic Pricing",
      "markets": [
        {"market": "North America", "minimum_usd": "25000", "reach": "5000000"},
        ...
      ]
    },
    ...
  ]
}

For queries on V1 receipts (line items), see analysis.sql
*/

