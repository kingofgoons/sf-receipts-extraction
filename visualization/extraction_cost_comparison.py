"""
Streamlit app to compare costs between AI_COMPLETE and AI_EXTRACT extraction methods.
Designed to run in Snowflake Notebooks or Streamlit in Snowflake.
"""
import streamlit as st
import pandas as pd
import altair as alt
from snowflake.snowpark.context import get_active_session

# Get Snowflake session
session = get_active_session()

# Page config
st.set_page_config(
    page_title="Receipt Extraction Cost Comparison",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Receipt Extraction Cost Comparison")
st.markdown("### AI_COMPLETE vs AI_EXTRACT for V1 Receipts")

# ============================================================================
# Sidebar: Filters and Settings (define before tabs to use in queries)
# ============================================================================
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Date range filter
    days_back = st.slider("Days of history", 1, 90, 30)
    
    st.markdown("---")
    
    # Data refresh
    if st.button("🔄 Refresh Data"):
        st.experimental_rerun()
    
    st.markdown("---")
    
    # Info
    st.markdown("""
    ### About This Dashboard
    
    This dashboard compares the costs of two receipt extraction methods:
    
    **AI_COMPLETE**: 
    - Uses AI_PARSE_DOCUMENT + AI_COMPLETE
    - More complex, two-step process
    
    **AI_EXTRACT**:
    - Direct PDF processing
    - Single-step extraction
    
    **Data Sources**:
    - `SNOWFLAKE.ACCOUNT_USAGE.*`
    - Warehouse metering
    - Cortex function usage
    - Document AI usage
    - Notebook execution history
    """)
    
    st.markdown("---")
    st.caption("Built with Streamlit in Snowflake")

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏛️ Warehouse Costs", "🤖 Cortex Costs", "📈 Trends"])

# ============================================================================
# TAB 1: Overview
# ============================================================================
with tab1:
    st.header("Cost Comparison Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("AI_COMPLETE Approach")
        st.markdown("""
        **Warehouse**: `RECEIPTS_PARSE_COMPLETE_WH`
        
        **Process**:
        1. AI_PARSE_DOCUMENT (extract text from PDF)
        2. AI_COMPLETE (structure extraction with LLM)
        
        **Cortex Functions Used**:
        - Document AI (parsing)
        - AI_COMPLETE (claude-haiku-4-5)
        """)
    
    with col2:
        st.subheader("AI_EXTRACT Approach")
        st.markdown("""
        **Warehouse**: `RECEIPTS_AI_EXTRACT_WH`
        
        **Process**:
        1. AI_EXTRACT (direct PDF to structured data)
        
        **Cortex Functions Used**:
        - AI_EXTRACT (with responseFormat schema)
        """)
    
    # Summary metrics
    st.markdown("---")
    
    # Get receipt counts
    receipt_counts = session.sql("""
    SELECT 
        'AI_COMPLETE' AS method,
        COUNT(*) AS receipt_count
    FROM RECEIPTS_PROCESSING_DB.RAW.extracted_receipt_data
    UNION ALL
    SELECT 
        'AI_EXTRACT' AS method,
        COUNT(*) AS receipt_count
    FROM RECEIPTS_PROCESSING_DB.RAW.extracted_receipt_data_via_ai_extract
    """).to_pandas()
    
    col1, col2, col3 = st.columns(3)
    
    for _, row in receipt_counts.iterrows():
        if row['METHOD'] == 'AI_COMPLETE':
            with col1:
                st.metric("AI_COMPLETE Receipts", f"{row['RECEIPT_COUNT']:,}")
        else:
            with col2:
                st.metric("AI_EXTRACT Receipts", f"{row['RECEIPT_COUNT']:,}")
    
    with col3:
        total = receipt_counts['RECEIPT_COUNT'].sum()
        st.metric("Total Processed", f"{total:,}")

# ============================================================================
# TAB 2: Warehouse Costs
# ============================================================================
with tab2:
    st.header("Warehouse Credit Consumption")
    
    # Query warehouse costs (using days_back from sidebar)
    warehouse_costs = session.sql(f"""
    SELECT 
        WAREHOUSE_NAME,
        DATE_TRUNC('day', START_TIME) AS day,
        SUM(CREDITS_USED) AS total_credits,
        SUM(CREDITS_USED_COMPUTE) AS compute_credits,
        SUM(CREDITS_USED_CLOUD_SERVICES) AS cloud_services_credits,
        COUNT(*) AS num_queries
    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
    WHERE WAREHOUSE_NAME IN ('RECEIPTS_PARSE_COMPLETE_WH', 'RECEIPTS_AI_EXTRACT_WH')
      AND START_TIME >= DATEADD('day', -{days_back}, CURRENT_TIMESTAMP())
    GROUP BY WAREHOUSE_NAME, DATE_TRUNC('day', START_TIME)
    ORDER BY day DESC, WAREHOUSE_NAME
    """).to_pandas()
    
    if not warehouse_costs.empty:
        # Summary metrics
        col1, col2 = st.columns(2)
        
        with col1:
            complete_total = warehouse_costs[warehouse_costs['WAREHOUSE_NAME'] == 'RECEIPTS_PARSE_COMPLETE_WH']['TOTAL_CREDITS'].sum()
            st.metric("AI_COMPLETE Warehouse Credits", f"{complete_total:.2f}")
        
        with col2:
            extract_total = warehouse_costs[warehouse_costs['WAREHOUSE_NAME'] == 'RECEIPTS_AI_EXTRACT_WH']['TOTAL_CREDITS'].sum()
            st.metric("AI_EXTRACT Warehouse Credits", f"{extract_total:.2f}")
        
        # Daily trend chart
        st.subheader("Daily Warehouse Credit Usage")
        chart = alt.Chart(warehouse_costs).mark_line(point=True).encode(
            x=alt.X('DAY:T', title='Date'),
            y=alt.Y('TOTAL_CREDITS:Q', title='Credits Used'),
            color=alt.Color('WAREHOUSE_NAME:N', title='Warehouse'),
            tooltip=['DAY:T', 'WAREHOUSE_NAME:N', 'TOTAL_CREDITS:Q', 'NUM_QUERIES:Q']
        ).properties(height=400)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Detailed table
        with st.expander("View Detailed Warehouse Costs"):
            st.dataframe(warehouse_costs, use_container_width=True)
    else:
        st.info("No warehouse usage data available yet. Process some receipts first!")

# ============================================================================
# TAB 3: Cortex Function Costs
# ============================================================================
with tab3:
    st.header("Cortex AI Function Credit Consumption")
    
    # Cortex Document Processing costs (AI_PARSE_DOCUMENT)
    st.subheader("Cortex Document Processing (AI_PARSE_DOCUMENT)")
    doc_ai_costs = session.sql(f"""
    SELECT 
        DATE_TRUNC('day', START_TIME) AS day,
        COUNT(*) AS num_calls,
        SUM(CREDITS_USED) AS total_credits,
        AVG(CREDITS_USED) AS avg_credits_per_call
    FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_DOCUMENT_PROCESSING_USAGE_HISTORY
    WHERE START_TIME >= DATEADD('day', -{days_back}, CURRENT_TIMESTAMP())
    GROUP BY DATE_TRUNC('day', START_TIME)
    ORDER BY day DESC
    """).to_pandas()
    
    if not doc_ai_costs.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Calls", f"{doc_ai_costs['NUM_CALLS'].sum():,}")
        with col2:
            st.metric("Total Credits", f"{doc_ai_costs['TOTAL_CREDITS'].sum():.2f}")
        with col3:
            st.metric("Avg Credits/Call", f"{doc_ai_costs['AVG_CREDITS_PER_CALL'].mean():.4f}")
        
        st.dataframe(doc_ai_costs, use_container_width=True)
    else:
        st.info("No Cortex Document Processing usage data available yet.")
    
    st.markdown("---")
    
    # Cortex functions costs (AI_COMPLETE, AI_EXTRACT)
    st.subheader("Cortex Functions Costs (AI_COMPLETE & AI_EXTRACT)")
    cortex_costs = session.sql(f"""
    SELECT 
        FUNCTION_NAME,
        MODEL_NAME,
        DATE_TRUNC('day', START_TIME) AS day,
        COUNT(*) AS num_calls,
        SUM(TOKENS) AS total_tokens,
        SUM(TOKEN_CREDITS) AS total_credits,
        AVG(TOKEN_CREDITS) AS avg_credits_per_call
    FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_USAGE_HISTORY
    WHERE FUNCTION_NAME IN ('COMPLETE', 'AI_EXTRACT')
      AND START_TIME >= DATEADD('day', -{days_back}, CURRENT_TIMESTAMP())
    GROUP BY FUNCTION_NAME, MODEL_NAME, DATE_TRUNC('day', START_TIME)
    ORDER BY day DESC, FUNCTION_NAME, MODEL_NAME
    """).to_pandas()
    
    if not cortex_costs.empty:
        # Summary by function
        function_summary = cortex_costs.groupby('FUNCTION_NAME').agg({
            'NUM_CALLS': 'sum',
            'TOTAL_TOKENS': 'sum',
            'TOTAL_CREDITS': 'sum',
            'AVG_CREDITS_PER_CALL': 'mean'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        for _, row in function_summary.iterrows():
            with col1 if row['FUNCTION_NAME'] == 'COMPLETE' else col2:
                st.markdown(f"**{row['FUNCTION_NAME']}**")
                st.metric("Calls", f"{row['NUM_CALLS']:.0f}")
                st.metric("Total Tokens", f"{row.get('TOTAL_TOKENS', 0):,.0f}")
                st.metric("Credits", f"{row['TOTAL_CREDITS']:.2f}")
                st.metric("Avg/Call", f"{row['AVG_CREDITS_PER_CALL']:.4f}")
        
        # Trend chart
        st.subheader("Daily Cortex Function Usage")
        chart = alt.Chart(cortex_costs).mark_bar().encode(
            x=alt.X('DAY:T', title='Date'),
            y=alt.Y('TOTAL_CREDITS:Q', title='Credits Used'),
            color=alt.Color('FUNCTION_NAME:N', title='Function'),
            tooltip=['DAY:T', 'FUNCTION_NAME:N', 'MODEL_NAME:N', 'NUM_CALLS:Q', 'TOTAL_TOKENS:Q', 'TOTAL_CREDITS:Q']
        ).properties(height=400)
        
        st.altair_chart(chart, use_container_width=True)
        
        with st.expander("View Detailed Cortex Costs"):
            st.dataframe(cortex_costs, use_container_width=True)
    else:
        st.info("No Cortex function usage data available yet.")

# ============================================================================
# TAB 4: Trends & Comparison
# ============================================================================
with tab4:
    st.header("Cost Trends & Method Comparison")
    
    # Combined cost estimate
    st.subheader("Estimated Total Cost per Receipt")
    
    st.markdown("""
    **AI_COMPLETE Approach**:
    - AI_PARSE_DOCUMENT: ~0.001-0.005 credits per page
    - AI_COMPLETE (claude-haiku-4-5): ~0.01-0.05 credits per call
    - Warehouse compute: ~0.0001 credits per receipt
    - **Estimated Total**: ~0.011-0.055 credits per receipt
    
    **AI_EXTRACT Approach**:
    - AI_EXTRACT: ~0.01-0.06 credits per call (direct PDF processing)
    - Warehouse compute: ~0.0001 credits per receipt
    - **Estimated Total**: ~0.01-0.06 credits per receipt
    
    *Note: Actual costs vary by document complexity, length, and schema complexity*
    """)
    
    st.markdown("---")
    
    # Notebook execution costs
    st.subheader("Notebook Execution Costs")
    notebook_costs = session.sql("""
    SELECT 
        NOTEBOOK_NAME,
        DATE_TRUNC('hour', START_TIME) AS hour,
        SUM(CREDITS) AS total_credits,
        SUM(NOTEBOOK_EXECUTION_TIME_SECS) AS total_execution_secs,
        COUNT(*) AS num_executions,
        AVG(CREDITS) AS avg_credits_per_execution
    FROM SNOWFLAKE.ACCOUNT_USAGE.NOTEBOOKS_CONTAINER_RUNTIME_HISTORY
    WHERE NOTEBOOK_NAME IN ('receipts_extractor', 'receipts_extractor_ai_extract')
      AND START_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
    GROUP BY NOTEBOOK_NAME, DATE_TRUNC('hour', START_TIME)
    ORDER BY hour DESC, NOTEBOOK_NAME
    """).to_pandas()
    
    if not notebook_costs.empty:
        col1, col2 = st.columns(2)
        
        for _, row in notebook_costs.groupby('NOTEBOOK_NAME').agg({'TOTAL_CREDITS': 'sum', 'NUM_EXECUTIONS': 'sum'}).reset_index().iterrows():
            with col1 if 'receipts_extractor' == row['NOTEBOOK_NAME'] and 'ai_extract' not in row['NOTEBOOK_NAME'] else col2:
                st.metric(row['NOTEBOOK_NAME'], f"{row['TOTAL_CREDITS']:.3f} credits")
                st.caption(f"{row['NUM_EXECUTIONS']:.0f} executions")
        
        st.dataframe(notebook_costs, use_container_width=True)
    else:
        st.info("No notebook execution data available yet.")
    
    st.markdown("---")
    
    # Cost recommendations
    st.subheader("💡 Cost Optimization Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **When to Use AI_COMPLETE**:
        - ✅ Complex nested schemas
        - ✅ Need detailed prompt control
        - ✅ Custom extraction logic
        - ✅ High accuracy requirements
        """)
    
    with col2:
        st.markdown("""
        **When to Use AI_EXTRACT**:
        - ✅ Simpler schemas
        - ✅ Direct PDF processing (skip parsing)
        - ✅ Faster processing
        - ✅ Lower latency
        """)

# Footer
st.markdown("---")
st.caption("💡 Tip: Run both notebooks to collect cost data, then view this dashboard to compare efficiency")

