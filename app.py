import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

st.set_page_config(
    page_title="TradeWatch Investigation",
    layout="wide",
    initial_sidebar_state="expanded"
)

INVESTIGATION_STEPS = {
    "Data Gathering": {
        "status": "Completed",
        "timestamp": "24/09/2025, 10:25:12 am",
        "icon": "✅",
        "description": "Collect trade data and market context."
    },
    "Pattern Analysis": {
        "status": "Completed",
        "timestamp": "24/09/2025, 10:35:45 am",
        "icon": "✅",
        "description": "Analyze trading patterns and behaviors."
    },
    "Risk Assessment": {
        "status": "In Progress",
        "timestamp": "24/09/2025, 10:38:22 am",
        "icon": "⏳",
        "description": "Evaluate compliance risk exposure."
    },
    "Recommendation": {
        "status": "Pending",
        "timestamp": "24/09/2025, 11:15:00 am",
        "icon": "⚪",
        "description": "AI-driven investigation outcome."
    }
}

if 'current_step' not in st.session_state:
    st.session_state['current_step'] = "Risk Assessment" # Start on the main data page

def generate_price_data(start_price=185.0, num_points=30):
    dates = pd.date_range(start='2025-09-26 09:00', periods=num_points, freq='15min')
    prices = start_price + np.cumsum(np.random.normal(0, 0.5, num_points))
    df = pd.DataFrame({'Time': dates, 'Price': prices.round(2)})
    df = df.set_index('Time')
    return df

def generate_liquidity_data():
    metrics = ['Bid-Ask Spread', 'Depth of Market', 'Order Imbalance', 'Execution Time']
    values = np.random.uniform(0.1, 5, len(metrics))
    df = pd.DataFrame({'Metric': metrics, 'Value': values.round(2)})
    return df

def generate_alerts_data():
    np.random.seed(42)
    data = {
        'Severity': np.random.randint(1, 10, 20),
        'Frequency': np.random.randint(1, 15, 20),
        'Alert Type': np.random.choice(['Insider Trading', 'Spoofing', 'Wash Trading', 'Market Manipulation'], 20),
        'Volume Impact': np.random.uniform(1000, 50000, 20)
    }
    df = pd.DataFrame(data)
    return df

def generate_pattern_data():
    dates = pd.date_range(start='2025-01-01', periods=12, freq='M')
    pattern_score = np.random.uniform(50, 95, 12)
    baseline = 75
    df = pd.DataFrame({'Month': dates, 'Score': pattern_score.round(1), 'Baseline': baseline})
    df['Month'] = df['Month'].dt.strftime('%Y-%m')
    return df

def render_risk_assessment_page():
    """Renders the two-column page with AI Reasoning and Evidence Visualization."""
    st.markdown("## Investigation Details")
    
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("### Risk Assessment Details")
        st.button("Export Details ⬇️", key="export_details_ra")
        st.markdown("---")
        
        with st.container(border=True): 
            st.subheader("AI Reasoning")
            st.write("Comprehensive risk evaluation using multi-factor analysis including regulatory risk indicators, market impact assessment, and compliance scoring. Risk factors weighted based on scenario-specific parameters for insider trading detection.")
            st.write("Overall risk assessment indicates low probability of compliance violation. Market conditions and trader behavior align with legitimate trading activities.")

            # Score and Status inline
            st.markdown(
                """
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <b>Analysis Score: 0.27</b>
                    <span style="font-weight: bold; color: green;">Status: current</span>
                </div>
                """, 
                unsafe_allow_html=True
            )

        st.markdown("---")
        with st.container(border=True):
            st.subheader("Input Parameters")
            
            param_col1, param_col2 = st.columns(2)
            with param_col1:
                st.caption("**Risk Factors**")
                st.markdown("12 primary indicators")
                st.caption("**Market Context**")
                st.markdown("High volatility period")

            with param_col2:
                st.caption("**Regulatory Framework**")
                st.markdown("SEC, FINRA guidelines")
                st.caption("**Compliance History**")
                st.markdown("Clean record - 24 months")

    with col_right:
        with st.container(border=True):
            st.markdown("### Evidence Visualization")
            st.write("Comprehensive data analysis for ALERT-2025-001847")
            
            st.button("Export Charts ⬇️", key="export_charts_btn_ra")

            tab_titles = ["Price Analysis", "Liquidity Metrics", "Related Alerts", "Pattern Detection"]
            tab_price, tab_liquidity, tab_alerts, tab_pattern = st.tabs(tab_titles)

            with tab_price: 
                st.subheader("Price Movement Timeline")
                price_df = generate_price_data()
                st.line_chart(price_df['Price'])

                st.subheader("Volume Analysis")
                volume_df = pd.DataFrame(
                    np.random.randint(6000, 24000, 10),
                    index=[f'10:{i*5:02d}' for i in range(10)],
                    columns=['Volume']
                )
                st.bar_chart(volume_df)

            with tab_liquidity:
                st.subheader("Key Liquidity Indicators")
                liquidity_df = generate_liquidity_data()
                chart = alt.Chart(liquidity_df).mark_bar().encode(
                    x=alt.X('Metric:N', sort=None),
                    y='Value:Q',
                    tooltip=['Metric', 'Value']
                ).properties(title='Current Liquidity Profile')
                st.altair_chart(chart, use_container_width=True)

            with tab_alerts:
                st.subheader("Alert Frequency vs. Severity")
                alerts_df = generate_alerts_data()
                chart = alt.Chart(alerts_df).mark_circle().encode(
                    x='Frequency',
                    y='Severity',
                    size=alt.Size('Volume Impact', scale=alt.Scale(range=[100, 1000])),
                    color='Alert Type',
                    tooltip=['Alert Type', 'Severity', 'Frequency', 'Volume Impact']
                ).properties(title='Alert Distribution by Type and Impact')
                st.altair_chart(chart, use_container_width=True)

            with tab_pattern:
                st.subheader("Monthly Pattern Score Trend")
                pattern_df = generate_pattern_data()
                base = alt.Chart(pattern_df).encode(x='Month')
                area = base.mark_area(opacity=0.3).encode(y=alt.Y('Score', title='Score'))
                line = base.mark_rule(color='red').encode(y='Baseline')
                st.altair_chart(area + line, use_container_width=True)
def render_recommendation_page():
    """Renders the single-column Investigation Assessment page with Key Findings and Actions."""
    st.markdown("## Investigation Assessment")
    
    with st.container(border=True):
        col_status, col_confidence = st.columns([3, 1])

        with col_status:
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 20px;">
                    <h3 style="margin-right: 20px;">Investigation Assessment</h3>
                    <span style="background-color: #e09f3e; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">
                        Medium
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write(
                f"**Alert ID:** ALT-2025-001847 • **Scenario:** Insider Trading - Intraday • **Duration:** 00:02:34"
            )
            
        with col_confidence:
            st.markdown(
                """
                <div style="background-color: #38761d; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                    <p style="margin: 0; font-size: 16px; font-weight: bold;">✅ False Positive</p>
                    <p style="margin: 0; font-size: 14px;">Confidence: 73%</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("#### AI Analysis Summary")
        st.write(
            "Based on comprehensive analysis of trading patterns, market conditions, and trader behavior, this alert appears to be a **false positive**. The trading activity aligns with normal market-making operations during high volatility periods."
        )
        st.button("Web View", key="web_view_btn")
        st.write(
            "Key findings indicate legitimate hedging activities with proper risk management protocols. No unusual information flow or timing anomalies detected that would suggest insider trading behavior."
        )
        
        st.markdown("---")
        col_findings, col_assessment, col_actions = st.columns([1.5, 1.5, 1])

        with col_findings:
            st.subheader("Key Findings")
            findings = [
                "Trading volume consistent with historical patterns",
                "No unusual pre-announcement activity detected",
                "Proper risk management protocols followed",
                "Market conditions support legitimate trading rationale"
            ]
            for finding in findings:
                st.markdown(f"**✅** {finding}")

        with col_assessment:
            st.subheader("Risk Assessment")
            risk_data = {
                "Timing Risk": 30, "Volume Anomaly": 40, "Price Impact": 60, "Information Flow": 20
            }
            for factor, score in risk_data.items():
                st.markdown(f"**{factor}**")
                if score < 40: color = "green"
                elif score < 70: color = "orange"
                else: color = "red"
                st.progress(score, text=f"**{score}%**")

        with col_actions:
            st.markdown("<br><br>", unsafe_allow_html=True) 
            st.button("🚫 Override - Create Case", use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True) 
            st.button("✅ Accept False Positive", type="primary", use_container_width=True)

        st.markdown(f"---")
        st.caption(f"Last updated: {datetime.now().strftime('24/09/2025, %I:%M:%S %p').replace('AM', 'am').replace('PM', 'pm')}")
def render_data_gathering_page():
    """Renders the content for the Data Gathering step."""
    st.markdown("### Data Gathering & Integrity Check")
    
    st.container(border=True).write("Details about data sources and initial fetching logs will appear here.")
    
    col_l, col_r = st.columns(2)
    with col_l:
        with st.container(border=True):
            st.subheader("Data Source Overview")
            st.markdown("""
                - **Trade Data:** 1.2M transactions (Source: Internal Trading System)
                - **Market Data:** NYSE/NASDAQ prices, Volume, and News Sentiment (Source: Refinitiv)
                - **User Behavior:** Login times, Document access (Source: Compliance Logs)
            """)
    
    with col_r:
        with st.container(border=True):
            st.subheader("Data Quality Check")
            st.metric(label="Missing Values Rate", value="0.01%", delta="Low")
            st.metric(label="Data Integrity Score", value="99.8%", delta="High")
            st.markdown("---")
            st.markdown("**Key Findings:** Data is complete and consistent across sources.")

def render_pattern_analysis_page():
    """Renders the content for the Pattern Analysis step."""
    st.markdown("### Pattern Analysis Results")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Trade-News Correlation", value="0.75", delta="High Risk")
        st.markdown("Trades consistently executed **2 hours** before market-moving news.")
    with col2:
        st.metric(label="Volume Fluctuation", value="300%", delta="Significant Increase")
        st.markdown("Unusual spikes in trading volume for the investigated security.")

    st.subheader("Visualization: Trading Activity")
    
    chart_data = pd.DataFrame(
        np.random.randn(20, 3).cumsum(axis=0),
        columns=['Security A', 'Security B', 'Security C']
    )
    st.line_chart(chart_data)


def render_timeline_step(step_name, data):
    """Renders the clickable timeline step, designed to look like a label/card."""
    is_active = st.session_state['current_step'] == step_name
    
    status_color = {
        "Completed": "#4CAF50", 
        "In Progress": "#FFC107",
        "Pending": "#9E9E9E" 
    }.get(data['status'], "#9E9E9E")

    if st.sidebar.button(
        label=f"{data['icon']} {step_name}", 
        key=f"step_btn_{step_name}", 
        use_container_width=True
    ):
        st.session_state['current_step'] = step_name
    
    st.sidebar.markdown(
        f"""
        <style>
        /* Target the button based on its key to apply custom styling */
        .stButton button[key="step_btn_{step_name}"] {{
            border-left: 5px solid {'#1f77b4' if is_active else 'transparent'};
            background-color: {'#e6f2ff' if is_active else 'white'};
            text-align: left;
            padding: 10px 10px 10px 20px;
            margin-bottom: 5px;
            height: auto; /* Allow the button to resize */
            
            /* Custom text alignment for the card look */
            color: #333; /* Dark text */
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown(
        f"""
        <div style="
            margin-top: -15px; 
            padding: 0 10px 10px 25px; 
            border-left: 5px solid {'#1f77b4' if is_active else 'transparent'};
            background-color: {'#e6f2ff' if is_active else 'white'};
            ">
            <p style="font-size: 0.9em; color: green; margin: 0;">
                {data['description']}
            </p>
            <p style="font-size: 0.7em; color: #999; margin: 0;">
                {data['status']} <span style="float: right;">{data['timestamp']}</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if step_name != list(INVESTIGATION_STEPS.keys())[-1]:
        st.sidebar.markdown('<div style="height: 10px; border-left: 2px solid #ccc; margin-left: 25px;"></div>', unsafe_allow_html=True)


with st.sidebar:
    st.title("Investigation Timeline")
    st.text("AI driven analysis progress")
    st.markdown("---")    
    for step, data in INVESTIGATION_STEPS.items():
        render_timeline_step(step, data)
    completed_steps = [s for s in INVESTIGATION_STEPS.values() if s['status'] == 'Completed']
    progress_percent = int((len(completed_steps) / len(INVESTIGATION_STEPS)) * 100)
    
    st.progress(progress_percent, text=f"Overall Progress: {progress_percent}%")
    st.markdown("---")

st.header(f"Alert Overview: {st.session_state['current_step']}")

col1, col2 = st.columns([1, 1])
with col1:
    st.subheader(f"Alert Details")
    st.markdown(f" Alert ID: **{'AW-2025-09-15-001'}**  \n")
    st.markdown(f" Scenario: **Potential Insider Trading**  \n")
    st.markdown(f" Trader: **{'John Smith'}**  \n")
    st.markdown(f" Desk: **Equities - North America**  \n")

with col2:
    st.subheader("Trade Details")
    st.markdown(f" Instrument: **{'XYZ Corp (XYZ)'}**  \n")
    st.markdown(f" Quantity: **15,000 Shares**  \n")
    st.markdown(f" Price: **$185.50**  \n")
    st.markdown(f" Trade Date: **2025-09-15**  \n")

st.markdown("---")
current_step = st.session_state['current_step']

if current_step == "Data Gathering":
    render_data_gathering_page()
elif current_step == "Pattern Analysis":
    render_pattern_analysis_page()
elif current_step == "Risk Assessment":
    render_risk_assessment_page()
elif current_step == "Recommendation":
    render_recommendation_page()
