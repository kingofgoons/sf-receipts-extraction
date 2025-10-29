-- ============================================================================
-- Receipt Analytics Queries
-- ============================================================================
-- This script contains analytical queries for receipt data extracted by
-- receipts-extractor.ipynb (AI_COMPLETE) and receipts-extractor_ai_extract.ipynb (AI_EXTRACT)
-- ============================================================================

USE ROLE SYSADMIN;
USE DATABASE RECEIPTS_PROCESSING_DB;
USE SCHEMA RAW;
USE WAREHOUSE RECEIPTS_PARSE_COMPLETE_WH;

-- ============================================================================
-- Analytics for V1 Receipts (Line Items) - from AI_COMPLETE
-- View: receipt_analytics_vw
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Spending Analysis by Vendor
-- ----------------------------------------------------------------------------
-- Analyze receipt count, total spending, average amounts, and performance 
-- metrics (CPM, CTR) by vendor to identify top advertising partners

SELECT 
    vendor_name,
    COUNT(*) AS receipt_count,
    SUM(total_amount) AS total_spending,
    AVG(total_amount) AS avg_receipt_amount,
    AVG(cpm) AS avg_cpm,
    AVG(ctr_percent) AS avg_ctr
FROM receipt_analytics_vw
GROUP BY vendor_name
ORDER BY total_spending DESC;

-- ----------------------------------------------------------------------------
-- 2. Campaign Performance by Content Type
-- ----------------------------------------------------------------------------
-- Compare performance between Display, Video, and mixed campaigns to optimize
-- content strategy and budget allocation

SELECT 
    content_types,
    COUNT(*) AS campaign_count,
    AVG(total_amount) AS avg_spending,
    AVG(cpm) AS avg_cpm,
    AVG(ctr_percent) AS avg_ctr,
    AVG(bounce_rate_percent) AS avg_bounce_rate
FROM receipt_analytics_vw
WHERE content_types IS NOT NULL
GROUP BY content_types
ORDER BY campaign_count DESC;

-- ----------------------------------------------------------------------------
-- 3. Performance Metrics by Pricing Model
-- ----------------------------------------------------------------------------
-- Understanding performance across different pricing models (CPM, CPC, CPA, 
-- CPV, Flat Rate) to determine which delivers the best ROI

SELECT 
    pricing_model,
    COUNT(*) AS receipt_count,
    AVG(cpm) AS avg_cpm,
    AVG(ctr_percent) AS avg_ctr,
    AVG(bounce_rate_percent) AS avg_bounce_rate,
    SUM(total_amount) AS total_spending
FROM receipt_analytics_vw
WHERE pricing_model IS NOT NULL
GROUP BY pricing_model
ORDER BY receipt_count DESC;

-- ============================================================================
-- Analytics for V1 Receipts (Line Items) - from AI_EXTRACT
-- View: receipt_analytics_ai_extract_vw
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 4. Spending Analysis by Vendor (AI_EXTRACT)
-- ----------------------------------------------------------------------------

SELECT 
    vendor_name,
    COUNT(*) AS receipt_count,
    SUM(total_amount) AS total_spending,
    AVG(total_amount) AS avg_receipt_amount,
    AVG(cpm) AS avg_cpm,
    AVG(ctr_percent) AS avg_ctr
FROM receipt_analytics_ai_extract_vw
GROUP BY vendor_name
ORDER BY total_spending DESC;

-- ----------------------------------------------------------------------------
-- 5. Campaign Performance by Content Type (AI_EXTRACT)
-- ----------------------------------------------------------------------------

SELECT 
    content_types,
    COUNT(*) AS campaign_count,
    AVG(total_amount) AS avg_spending,
    AVG(cpm) AS avg_cpm,
    AVG(ctr_percent) AS avg_ctr,
    AVG(bounce_rate_percent) AS avg_bounce_rate
FROM receipt_analytics_ai_extract_vw
WHERE content_types IS NOT NULL
GROUP BY content_types
ORDER BY campaign_count DESC;

-- ----------------------------------------------------------------------------
-- 6. Performance Metrics by Pricing Model (AI_EXTRACT)
-- ----------------------------------------------------------------------------

SELECT 
    pricing_model,
    COUNT(*) AS receipt_count,
    AVG(cpm) AS avg_cpm,
    AVG(ctr_percent) AS avg_ctr,
    AVG(bounce_rate_percent) AS avg_bounce_rate,
    SUM(total_amount) AS total_spending
FROM receipt_analytics_ai_extract_vw
WHERE pricing_model IS NOT NULL
GROUP BY pricing_model
ORDER BY receipt_count DESC;

-- ============================================================================
-- Comparison Queries - AI_COMPLETE vs AI_EXTRACT
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 7. Compare Extraction Methods by Vendor
-- ----------------------------------------------------------------------------
-- Compare results from AI_COMPLETE vs AI_EXTRACT to assess accuracy

SELECT 
    'AI_COMPLETE' AS extraction_method,
    vendor_name,
    COUNT(*) AS receipt_count,
    SUM(total_amount) AS total_spending
FROM receipt_analytics_vw
GROUP BY vendor_name

UNION ALL

SELECT 
    'AI_EXTRACT' AS extraction_method,
    vendor_name,
    COUNT(*) AS receipt_count,
    SUM(total_amount) AS total_spending
FROM receipt_analytics_ai_extract_vw
GROUP BY vendor_name

ORDER BY vendor_name, extraction_method;

-- ============================================================================
-- Advanced Analytics
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 8. Monthly Spending Trends
-- ----------------------------------------------------------------------------

SELECT 
    DATE_TRUNC('month', transaction_date) AS month,
    COUNT(*) AS receipt_count,
    SUM(total_amount) AS total_spending,
    AVG(cpm) AS avg_cpm,
    AVG(ctr_percent) AS avg_ctr
FROM receipt_analytics_vw
WHERE transaction_date IS NOT NULL
GROUP BY DATE_TRUNC('month', transaction_date)
ORDER BY month DESC;

-- ----------------------------------------------------------------------------
-- 9. Top Performing Campaigns
-- ----------------------------------------------------------------------------

SELECT 
    campaign_name,
    vendor_name,
    total_amount,
    cpm,
    ctr_percent,
    bounce_rate_percent,
    transaction_date
FROM receipt_analytics_vw
WHERE ctr_percent IS NOT NULL
ORDER BY ctr_percent DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- 10. Campaign Duration Analysis
-- ----------------------------------------------------------------------------

SELECT 
    campaign_name,
    vendor_name,
    period_startdate,
    period_enddate,
    DATEDIFF('day', period_startdate, period_enddate) AS campaign_days,
    total_amount,
    total_amount / NULLIF(DATEDIFF('day', period_startdate, period_enddate), 0) AS daily_spend
FROM receipt_analytics_vw
WHERE period_startdate IS NOT NULL 
  AND period_enddate IS NOT NULL
ORDER BY campaign_days DESC;

-- ----------------------------------------------------------------------------
-- 11. Budget vs Actual Spend
-- ----------------------------------------------------------------------------

SELECT 
    vendor_name,
    campaign_name,
    daily_budget,
    campaign_budget,
    total_amount AS actual_spend,
    campaign_budget - total_amount AS budget_remaining,
    (total_amount / NULLIF(campaign_budget, 0)) * 100 AS budget_utilization_pct
FROM receipt_analytics_vw
WHERE campaign_budget IS NOT NULL
  AND campaign_budget > 0
ORDER BY budget_utilization_pct DESC;

-- ============================================================================
-- Data Quality Checks
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 12. Extraction Completeness Check
-- ----------------------------------------------------------------------------

SELECT 
    COUNT(*) AS total_receipts,
    SUM(CASE WHEN vendor_name IS NOT NULL THEN 1 ELSE 0 END) AS has_vendor,
    SUM(CASE WHEN transaction_date IS NOT NULL THEN 1 ELSE 0 END) AS has_date,
    SUM(CASE WHEN total_amount IS NOT NULL THEN 1 ELSE 0 END) AS has_amount,
    SUM(CASE WHEN cpm IS NOT NULL THEN 1 ELSE 0 END) AS has_cpm,
    SUM(CASE WHEN ctr_percent IS NOT NULL THEN 1 ELSE 0 END) AS has_ctr
FROM receipt_analytics_vw;

-- ----------------------------------------------------------------------------
-- 13. Data Quality Issues
-- ----------------------------------------------------------------------------

SELECT 
    receipt_filename,
    vendor_name,
    CASE WHEN transaction_date IS NULL THEN 'Missing date' END AS issue_date,
    CASE WHEN total_amount IS NULL OR total_amount = 0 THEN 'Missing/zero amount' END AS issue_amount,
    CASE WHEN campaign_name IS NULL THEN 'Missing campaign' END AS issue_campaign
FROM receipt_analytics_vw
WHERE transaction_date IS NULL 
   OR total_amount IS NULL 
   OR total_amount = 0 
   OR campaign_name IS NULL;

-- ============================================================================
-- End of Analytics Queries
-- ============================================================================

