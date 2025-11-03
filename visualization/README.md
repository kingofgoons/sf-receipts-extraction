# Receipt Extraction Cost Visualization

Streamlit app to compare costs between AI_COMPLETE and AI_EXTRACT extraction methods.

## What It Shows

This dashboard compares the cost and efficiency of two receipt extraction approaches:

### AI_COMPLETE Approach
- **Warehouse**: `RECEIPTS_PARSE_COMPLETE_WH`
- **Process**: AI_PARSE_DOCUMENT → AI_COMPLETE
- **Functions**: Document AI parsing + Claude Haiku LLM
- **File**: `receipts-extractor.ipynb`

### AI_EXTRACT Approach
- **Warehouse**: `RECEIPTS_AI_EXTRACT_WH`
- **Process**: AI_EXTRACT (direct PDF)
- **Functions**: AI_EXTRACT with responseFormat
- **File**: `receipts-extractor_ai_extract.ipynb`

## Dashboard Sections

### 📊 Overview
- Receipt counts by method
- Approach comparison
- Summary metrics

### 🏛️ Warehouse Costs
- Credit consumption by warehouse
- Daily trends
- Compute vs cloud services breakdown

### 🤖 Cortex Costs
- AI_PARSE_DOCUMENT usage
- AI_COMPLETE usage
- AI_EXTRACT usage
- Per-function cost analysis

### 📈 Trends
- Cost over time
- Notebook execution costs
- Cost per receipt estimates
- Optimization recommendations

## Setup

### Option 1: Run in Snowflake Streamlit

1. **Upload the app to Snowflake**:
```sql
-- Create a Streamlit app
CREATE STREAMLIT RECEIPTS_PROCESSING_DB.PUBLIC.extraction_cost_dashboard
  FROM '/visualization'
  MAIN_FILE = 'extraction_cost_comparison.py';
```

2. **Grant permissions**:
```sql
GRANT USAGE ON STREAMLIT RECEIPTS_PROCESSING_DB.PUBLIC.extraction_cost_dashboard 
  TO ROLE SYSADMIN;
```

3. **Open the app** in Snowsight

### Option 2: Run in Snowflake Notebook

1. Create a new notebook in Snowflake
2. Copy the contents of `extraction_cost_comparison.py`
3. Paste into a Python cell
4. Run the cell

## Requirements

The app queries these Snowflake usage views:
- `SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY`
- `SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_USAGE_HISTORY`
- `SNOWFLAKE.ACCOUNT_USAGE.DOCUMENT_AI_USAGE_HISTORY`
- `SNOWFLAKE.ACCOUNT_USAGE.NOTEBOOKS_CONTAINER_RUNTIME_HISTORY`

**Required Role**: ACCOUNTADMIN or a role with access to ACCOUNT_USAGE views

## Usage

1. **Process receipts** using both methods:
   - Run `receipts-extractor.ipynb` (AI_COMPLETE)
   - Run `receipts-extractor_ai_extract.ipynb` (AI_EXTRACT)

2. **Wait 15-30 minutes** for usage data to populate in ACCOUNT_USAGE views

3. **View the dashboard** to compare costs

## Data Sources

### Warehouse Costs
```sql
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE WAREHOUSE_NAME IN ('RECEIPTS_PARSE_COMPLETE_WH', 'RECEIPTS_AI_EXTRACT_WH')
```

### Cortex Function Costs
```sql
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_USAGE_HISTORY
WHERE FUNCTION_NAME IN ('AI_COMPLETE', 'AI_EXTRACT')
```

### Document AI Costs
```sql
FROM SNOWFLAKE.ACCOUNT_USAGE.DOCUMENT_AI_USAGE_HISTORY
```

## Cost Estimation

**Typical V1 Receipt Costs**:

| Method | Component | Est. Credits | Notes |
|--------|-----------|--------------|-------|
| AI_COMPLETE | AI_PARSE_DOCUMENT | 0.001-0.005 | Per page |
| AI_COMPLETE | AI_COMPLETE | 0.01-0.05 | Per extraction |
| AI_COMPLETE | Warehouse | ~0.0001 | Minimal |
| **AI_COMPLETE Total** | | **~0.011-0.055** | **Per receipt** |
| | | | |
| AI_EXTRACT | AI_EXTRACT | 0.01-0.06 | Per PDF |
| AI_EXTRACT | Warehouse | ~0.0001 | Minimal |
| **AI_EXTRACT Total** | | **~0.01-0.06** | **Per receipt** |

## Features

- ✅ Real-time cost tracking
- ✅ Side-by-side comparison
- ✅ Daily trend visualizations
- ✅ Per-receipt cost estimates
- ✅ Optimization recommendations
- ✅ Interactive filters

---

**Note**: Usage data in ACCOUNT_USAGE views has a latency of 15-30 minutes. Recent costs may not appear immediately.

