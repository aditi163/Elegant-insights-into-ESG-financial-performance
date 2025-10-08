import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="ESG Cinematic Dashboard",
    layout="wide",
 
)

# ------------------- Custom Cinematic Dark Theme CSS -------------------
# Enhancements: Gradient Title, Polished Cards, Subtle Shadowing
st.markdown("""
<style>
/* General App View */
#MainMenu, footer {visibility: hidden;}
[data-testid="stAppViewContainer"] {
    background-color: #0d0d0d; /* Slightly darker base */
    color: #f0f0f0;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #1c1c1c; /* Darker, richer sidebar background */
    padding: 2rem;
    color: #f0f0f0;
    border-radius: 12px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.7); /* Deeper shadow */
    border-right: 1px solid #333333;
}
[data-testid="stSidebar"] h2 {
    color: #00C853 !important; /* Highlight sidebar header */
    font-weight: 700;
    border-bottom: 2px solid #333333;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

/* Cinematic Gradient Header */
.cinematic-header {
    text-align:center; 
    margin-bottom:40px;
}
.cinematic-header h1 {
    font-size: 60px;
    letter-spacing: 4px;
    margin: 0;
    font-weight: 900;
    text-transform: uppercase;
    /* Subtle Green-to-Grey Gradient */
    background: -webkit-linear-gradient(45deg, #00C853, #90ee90, #f0f0f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 4px 10px rgba(0, 200, 83, 0.4);
}
.subtitle { 
    color: #a0a0a0; 
    font-size: 18px; 
    font-style: italic;
    margin-top: 10px;
}

/* Metric Cards */
.card {
    background: #1c1c1c;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.6);
    transition: all 0.3s;
    text-align: center;
    border-left: 5px solid #00C853; /* Highlight strip */
    min-height: 120px;
}
.card:hover { 
    transform: translateY(-5px) scale(1.02); 
    box-shadow: 0 15px 30px rgba(0,200,83,0.4);
    border-left: 5px solid #90ee90;
}
.card-title { 
    font-size: 14px; 
    color: #909090; 
    margin-bottom: 8px; 
    font-weight: 600;
    text-transform: uppercase;
}
.card-value { 
    font-size: 32px; 
    font-weight: 800; 
    color: #90ee90; /* Brighter green for value */
}

/* Subheaders */
h2 {
    color: #00C853 !important;
    padding-top: 20px;
    padding-bottom: 10px;
    margin-top: 30px;
    border-bottom: 1px solid #333333;
}

</style>
""", unsafe_allow_html=True)

# ------------------- Load Data (Using st.cache_data) -------------------
@st.cache_data(show_spinner=False)
def load_esg_data():
    try:
        df = pd.read_csv("company_esg_financial_dataset.csv")
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        st.warning("CSV file not found. Loading mock data for demo.")
        data = {
            'CompanyName': ['Alpha Solutions', 'Beta Corp', 'Gamma Energy', 'Delta Finance', 'Epsilon Innovations', 'Zeta Tech', 'Eta Energy', 'Theta Finance', 'Iota Corp', 'Kappa Solutions', 'Alpha Innovate'],
            'Industry': ['Tech', 'Tech', 'Energy', 'Finance', 'Tech', 'Energy', 'Finance', 'Tech', 'Energy', 'Finance', 'Retail'],
            'Region': ['Asia', 'Asia', 'Europe', 'US', 'Europe', 'Asia', 'US', 'Europe', 'US', 'Asia', 'US'],
            'ESG_Overall': [85, 75, 55, 90, 60, 70, 80, 72, 65, 88, 70],
            'ESG_Environmental': [80, 70, 60, 95, 50, 65, 75, 70, 60, 90, 75],
            'ESG_Social': [88, 78, 50, 85, 65, 75, 85, 70, 70, 85, 80],
            'ESG_Governance': [87, 77, 55, 90, 65, 70, 80, 76, 65, 89, 75],
            'Revenue': [1500000, 1200000, 800000, 2000000, 950000, 1100000, 1600000, 1300000, 900000, 1800000, 1400000],
            'ProfitMargin': [18.5, 12.0, 7.5, 22.0, 10.5, 11.0, 15.0, 13.5, 8.0, 20.0, 14.5],
            'MarketCap': [50000000, 30000000, 15000000, 80000000, 25000000, 35000000, 60000000, 40000000, 20000000, 70000000, 45000000],
            'GrowthRate': [15.2, 10.1, 5.5, 18.0, 9.5, 10.5, 14.0, 12.5, 6.0, 17.0, 13.0]
        }
        df = pd.DataFrame(data)
    return df

df = load_esg_data()

# ------------------- Sidebar Filters -------------------
with st.sidebar:
    st.header("Data Selection")
    
    # Filter setup
    industries = sorted(df["Industry"].dropna().unique())
    regions = sorted(df["Region"].dropna().unique())

    selected_industry = st.selectbox("Select Industry", industries, index=industries.index('Tech') if 'Tech' in industries else 0)
    selected_region = st.selectbox("Select Region", regions, index=regions.index('US') if 'US' in regions else 0)
    esg_min, esg_max = st.slider("Select ESG Overall Range", 0, 100, (60, 95))

# Apply filters
filtered_df = df[
    (df["Industry"] == selected_industry) &
    (df["Region"] == selected_region) &
    (df["ESG_Overall"] >= esg_min) &
    (df["ESG_Overall"] <= esg_max)
]

# ------------------- Header (Cinematic Look) -------------------
st.markdown("""
<div class='cinematic-header'>
    <h1>ESG Dashboard</h1>
    <p class='subtitle'>A deep-dive into sustainable and financial performance</p>
</div>
""", unsafe_allow_html=True)

# ------------------- Metric Cards -------------------
st.markdown("---")
st.subheader("Key Performance Indicators (KPIs)")

if not filtered_df.empty:
    avg_revenue = filtered_df['Revenue'].mean()
    avg_profit_margin = filtered_df['ProfitMargin'].mean()
    avg_esg_score = filtered_df['ESG_Overall'].mean()
    max_market_cap = filtered_df['MarketCap'].max()
    avg_growth_rate = filtered_df['GrowthRate'].mean()
else:
    avg_revenue = avg_profit_margin = avg_esg_score = max_market_cap = avg_growth_rate = 0

metrics = {
    "Avg Revenue": f"₹{avg_revenue:,.0f}",
    "Avg Profit Margin": f"{avg_profit_margin:.2f}%",
    "Avg ESG Score": f"{avg_esg_score:.2f}",
    "Max Market Cap": f"₹{max_market_cap:,.0f}",
    "Avg Growth Rate": f"{avg_growth_rate:.2f}%"
}

cols = st.columns(5)
for i, (metric, value) in enumerate(metrics.items()):
    with cols[i]:
        st.markdown(f"""
            <div class='card'>
                <div class='card-title'>{metric}</div>
                <div class='card-value'>{value}</div>
            </div>
        """, unsafe_allow_html=True)

# ------------------- PLOTS -------------------
st.markdown("---")

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    
    # === Row 1: Histogram and Scatter ===
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ESG Score Distribution")
        fig_hist = px.histogram(
            filtered_df,
            x="ESG_Overall",
            nbins=15,
            color_discrete_sequence=["#90ee90"],
            title="Frequency of ESG Overall Scores in Selection"
        )
        fig_hist.update_traces(
            marker=dict(line=dict(width=1, color='rgba(0,0,0,0.5)'), opacity=0.9),
            selector=dict(type='bar')
        )
        fig_hist.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(28,28,28,0.5)', # Slight background for plot area
            font=dict(color="#f0f0f0"),
            xaxis=dict(title="ESG Overall Score", showgrid=True, gridcolor="#2b2b2b"),
            yaxis=dict(title="Count", showgrid=True, gridcolor="#2b2b2b"),
            title_font_color="#f0f0f0",
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.subheader("Market Cap vs. ESG Score")
        fig_scatter = px.scatter(
            filtered_df,
            x="ESG_Overall",
            y="MarketCap",
            size="Revenue",
            color="ProfitMargin",
            hover_data=["CompanyName", "GrowthRate"],
            color_continuous_scale=px.colors.sequential.Plotly3, # Brighter, more distinct scale
            title="Market Capitalization vs. ESG Performance"
        )
        fig_scatter.update_traces(
            marker=dict(line=dict(width=1, color='rgba(0,0,0,0.4)'))
        )
        fig_scatter.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(28,28,28,0.5)',
            font=dict(color="#f0f0f0"),
            xaxis=dict(title="ESG Overall Score", showgrid=True, gridcolor="#2b2b2b"),
            yaxis=dict(title="Market Cap (₹)", showgrid=True, gridcolor="#2b2b2b"),
            title_font_color="#f0f0f0",
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # === Row 2: Box Plot and Radar Chart ===
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Profit Margin Distribution by Industry")
        fig_box = px.box(
            df, # Use the full DF for broader industry comparison
            x="Industry",
            y="ProfitMargin",
            color="Industry",
            color_discrete_sequence=px.colors.qualitative.D3, # Clean, distinct colors
            points="all",
            hover_data={"ProfitMargin": True, "Industry": True},
            title="Industry-wide Profit Margin Comparison"
        )
        fig_box.update_traces(
            boxmean='sd',
            marker=dict(size=6, opacity=0.8, line=dict(width=1, color='rgba(0,0,0,0.5)')),
            opacity=0.9,
            jitter=0.3
        )
        fig_box.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(28,28,28,0.5)',
            font=dict(color="#f0f0f0"),
            xaxis=dict(title="Industry", showgrid=False, color='#f0f0f0', tickangle=-15),
            yaxis=dict(title="Profit Margin (%)", showgrid=True, gridcolor="#2b2b2b", color='#f0f0f0'),
            showlegend=False,
            title_font_color="#f0f0f0",
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col4:
        st.subheader("ESG Component Breakdown")
        categories = ['ESG_Environmental', 'ESG_Social', 'ESG_Governance']
        avg_scores = [filtered_df[c].mean() for c in categories]
        r_values = avg_scores + avg_scores[:1]
        theta_values = categories + categories[:1]

        fig_radar = go.Figure(data=go.Scatterpolar(
            r=r_values,
            theta=theta_values,
            fill='toself',
            line_color="#90ee90", # Bright line color
            line=dict(width=5),
            marker=dict(size=10, symbol='circle', color="#00C853", line=dict(color="#f0f0f0", width=2)),
            opacity=0.7,
            hovertemplate="<b>%{theta}</b>: %{r:.2f}<extra></extra>"
        ))
        fig_radar.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                bgcolor='#1c1c1c', # Darker radar background
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="#333333",
                    linecolor="#555555",
                    color='#f0f0f0',
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    linecolor='#555555',
                    color='#f0f0f0',
                    tickfont=dict(size=12)
                )
            ),
            font_size=14,
            title=dict(text="Average Component Scores in Selection", font=dict(color="#f0f0f0"))
        )
        st.plotly_chart(fig_radar, use_container_width=True)


# ------------------- Footer -------------------
st.markdown("---")
st.markdown("<div class='footer'> ESG Dashboard &copy; 2025</div>", unsafe_allow_html=True)
