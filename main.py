import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="ESG Dashboard", layout="wide")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
    <style>
        body { background-color: #0d0d0d; color: white; }
        .sidebar .sidebar-content { background-color: #0f0f0f; }
        h1, h2, h3, h4, h5 { color: white; font-family: 'Helvetica Neue', sans-serif; }
        div[data-testid="stMetricValue"] { color: #00ff88; }
        .css-17eq0hr { background-color: #0f0f0f !important; }
        .stSelectbox label, .stSlider label { color: black !important; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
<h1 style='
    text-align:center;
    color:white;
    font-size:48px;
    font-weight:700;
    font-family:Helvetica Neue, Arial, sans-serif;
    letter-spacing:2px;
    margin-bottom:0;
'>ESG Financial Dashboard</h1>
<p style='
    text-align:center;
    color:#b0b0b0;
    font-size:16px;
    margin-top:4px;
    font-style:italic;
'>Elegant insights into ESG and financial performance</p>
""", unsafe_allow_html=True)

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("company_esg_financial_dataset.csv")
    return df

data = load_data()

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.markdown("<h2 style='color:white; font-weight:700;'>Filters</h2>", unsafe_allow_html=True)

industries = ["All"] + sorted(data["Industry"].dropna().unique().tolist())
regions = ["All"] + sorted(data["Region"].dropna().unique().tolist())

industry_filter = st.sidebar.selectbox("**Select Industry**", industries, key="industry")
region_filter = st.sidebar.selectbox("**Select Region**", regions, key="region")
score_range = st.sidebar.slider("**Select ESG Score Range**", 0, 100, (0, 100), key="score")

# -------------------- APPLY FILTERS --------------------
filtered = data.copy()
if industry_filter != "All":
    filtered = filtered[filtered["Industry"] == industry_filter]
if region_filter != "All":
    filtered = filtered[filtered["Region"] == region_filter]
filtered = filtered[(filtered["ESG_Overall"] >= score_range[0]) & (filtered["ESG_Overall"] <= score_range[1])]

# -------------------- METRIC CARDS --------------------
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Avg Revenue", f"₹{filtered['Revenue'].mean():,.0f}")
col2.metric("Avg Profit Margin", f"{filtered['ProfitMargin'].mean():.2f}%")
col3.metric("Avg ESG Score", f"{filtered['ESG_Overall'].mean():.2f}")
col4.metric("Max Market Cap", f"₹{filtered['MarketCap'].max():,.0f}")
col5.metric("Avg Growth Rate", f"{filtered['GrowthRate'].mean():.2f}%")

# -------------------- CHARTS --------------------
st.markdown("<hr style='border:1px solid #1a1a1a;'>", unsafe_allow_html=True)
st.markdown("### 📊 ESG & Financial Insights")

# Bar Chart — Avg ESG by Industry
fig_bar = px.bar(
    filtered.groupby("Industry")["ESG_Overall"].mean().sort_values(ascending=False).reset_index(),
    x="Industry",
    y="ESG_Overall",
    title="Average ESG Score by Industry",
    color="ESG_Overall",
    color_continuous_scale=["#004d40", "#00e676"],
)
fig_bar.update_layout(
    paper_bgcolor="#0d0d0d",
    plot_bgcolor="#0d0d0d",
    font=dict(color="white"),
    title_font=dict(size=18),
    xaxis=dict(title="", showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#1a1a1a")
)
st.plotly_chart(fig_bar, use_container_width=True)

# Box Plot — ESG Distribution by Region
fig_box = px.box(
    filtered,
    x="Region",
    y="ESG_Overall",
    color="Region",
    title="ESG Score Distribution by Region",
    color_discrete_sequence=px.colors.sequential.Greens_r,
)
fig_box.update_layout(
    paper_bgcolor="#0d0d0d",
    plot_bgcolor="#0d0d0d",
    font=dict(color="white"),
    xaxis=dict(title="", showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#1a1a1a"),
)
st.plotly_chart(fig_box, use_container_width=True)

# Scatter Plot — Market Cap vs ESG
fig_scatter = px.scatter(
    filtered,
    x="MarketCap",
    y="ESG_Overall",
    size="Revenue",
    color="Industry",
    hover_name="CompanyName",
    title="Market Cap vs ESG Score",
    color_discrete_sequence=px.colors.qualitative.Dark24
)
fig_scatter.update_layout(
    paper_bgcolor="#0d0d0d",
    plot_bgcolor="#0d0d0d",
    font=dict(color="white"),
    xaxis=dict(title="Market Cap", showgrid=True, gridcolor="#1a1a1a"),
    yaxis=dict(title="ESG Score", showgrid=True, gridcolor="#1a1a1a"),
)
st.plotly_chart(fig_scatter, use_container_width=True)

# -------------------- FOOTER --------------------
st.markdown("<hr style='border:1px solid #1a1a1a;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#777; font-size:13px;'>© 2025 ESG Insights | Designed by Aditi Reddy</p>",
    unsafe_allow_html=True
)
