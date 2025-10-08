# pip install streamlit pandas plotly yfinance

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="ESG Cinematic Dashboard",
    layout="wide",
    page_icon="🌿",
)

# ------------------- Custom Green & White Theme -------------------
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stAppViewContainer"] {
    background-color: #f9fdf7;
    color: #1b3a2a;
    font-family: 'Helvetica', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #e0f2db;
    padding: 2rem;
    color: #1b3a2a;
    border-radius: 10px;
}
/* Sidebar headings - black & bold */
section[data-testid="stSidebar"] label {
    font-weight: 700 !important;
    color: #000000 !important;
}
/* Dropdown arrows */
[data-baseweb="select"] svg {
    fill: #1b3a2a !important;
}
/* Slider */
[data-baseweb="slider"] .baseweb-slider-thumb {
    background-color: #2e7d32 !important;
}
[data-baseweb="slider"] .baseweb-slider-track {
    background-color: #a7d5a1 !important;
}
/* Metric Cards */
.card {
    background: linear-gradient(135deg, #dff2e1, #b6e0a9);
    border-radius: 14px;
    min-width: 250px;
    padding: 20px;
    box-shadow: 0 6px 20px rgba(27,58,42,0.3);
    flex: 0 0 auto;
    transition: transform 0.2s;
    margin-bottom: 15px;
}
.card:hover { transform: translateY(-5px); }
.card-title { font-size: 14px; color: #1b3a2a; margin-bottom: 8px; }
.card-value { font-size: 22px; font-weight: 700; color: #2e7d32; }
.footer { text-align: center; color: #4b6f53; font-size: 13px; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ------------------- Load Data -------------------
@st.cache_data
def load_esg_data():
    df = pd.read_csv("company_esg_financial_dataset.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_esg_data()

# ------------------- Sidebar -------------------
with st.sidebar:
    st.header("Filters")
    industries = sorted(df["Industry"].dropna().unique())
    regions = sorted(df["Region"].dropna().unique())

    selected_industry = st.selectbox("Select Industry", industries)
    selected_region = st.selectbox("Select Region", regions)
    esg_min, esg_max = st.slider("Select ESG Overall Range", 0, 100, (40, 90))

filtered_df = df[
    (df["Industry"] == selected_industry) &
    (df["Region"] == selected_region) &
    (df["ESG_Overall"] >= esg_min) &
    (df["ESG_Overall"] <= esg_max)
]

# ------------------- Header -------------------
st.markdown("""
<div style='text-align:center; margin-bottom:20px;'>
    <h1 style='color:#1b3a2a; font-size:50px; font-weight:800; letter-spacing:2px;'>ESG Dashboard</h1>
    <p style='color:#4b6f53; font-size:16px; font-style:italic; letter-spacing:1.5px;'>Elegant insights into ESG & financial performance</p>
</div>
""", unsafe_allow_html=True)

# ------------------- Metric Cards -------------------
metrics = {
    "Avg Revenue": f"₹{filtered_df['Revenue'].mean():,.0f}",
    "Avg Profit Margin": f"{filtered_df['ProfitMargin'].mean():.2f}%",
    "Avg ESG Score": f"{filtered_df['ESG_Overall'].mean():.2f}",
    "Max Market Cap": f"₹{filtered_df['MarketCap'].max():,.0f}",
    "Avg Growth Rate": f"{filtered_df['GrowthRate'].mean():.2f}%"
}

metric_items = list(metrics.items())
for i in range(0, len(metric_items), 2):
    cols = st.columns(2)
    for j, (metric, value) in enumerate(metric_items[i:i+2]):
        with cols[j]:
            st.markdown(f"""
                <div class='card'>
                    <div class='card-title'>{metric}</div>
                    <div class='card-value'>{value}</div>
                </div>
            """, unsafe_allow_html=True)

# ------------------- Plots -------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("ESG Score Distribution")
    fig_hist = px.histogram(
        filtered_df,
        x="ESG_Overall",
        nbins=15,
        color_discrete_sequence=["#2e7d32"]
    )
    fig_hist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1b3a2a"),
        xaxis_title="ESG Overall",
        yaxis_title="Count"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("MarketCap vs ESG Score")
    fig_scatter = px.scatter(
        filtered_df,
        x="ESG_Overall",
        y="MarketCap",
        size="Revenue",
        color="ProfitMargin",
        hover_data=["CompanyName", "GrowthRate"],
        color_continuous_scale=px.colors.sequential.Greens
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1b3a2a"),
        xaxis_title="ESG Overall",
        yaxis_title="Market Cap"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ------------------- Profit Margin Box Plot -------------------
st.subheader("Profit Margin by Industry (Box Plot)")
fig_box = px.box(
    df,
    x="Industry",
    y="ProfitMargin",
    color="Industry",
    color_discrete_sequence=px.colors.qualitative.Prism,
    points="all"
)
fig_box.update_traces(
    boxmean='sd',
    marker=dict(size=7, opacity=0.8),
    line=dict(width=2)
)
fig_box.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#1b3a2a"),
    xaxis_title="Industry",
    yaxis_title="Profit Margin (%)",
    xaxis_tickangle=-45
)
st.plotly_chart(fig_box, use_container_width=True)

# ------------------- ESG Radar -------------------
st.subheader("ESG Component Breakdown (Radar Chart)")
categories = ['ESG_Environmental', 'ESG_Social', 'ESG_Governance']
avg_scores = [filtered_df[c].mean() for c in categories]
fig_radar = go.Figure(data=go.Scatterpolar(
    r=avg_scores,
    theta=categories,
    fill='toself',
    line_color="#2e7d32"
))
fig_radar.update_layout(
    polar=dict(bgcolor='#f9fdf7', radialaxis=dict(visible=True, color='#1b3a2a')),
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#1b3a2a"
)
st.plotly_chart(fig_radar, use_container_width=True)

# ------------------- Footer -------------------
st.markdown("<div class='footer'>🌿 ESG Dashboard &copy; 2025</div>", unsafe_allow_html=True)
