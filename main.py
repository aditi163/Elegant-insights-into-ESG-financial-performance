import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="Elegant ESG Dashboard", layout="wide")

# ------------------- HEADER -------------------
st.markdown("""
<h1 style='
    text-align:center;
    color:white;
    font-size:48px;
    font-weight:700;
    font-family:Poppins, Helvetica, sans-serif;
    letter-spacing:1px;
    margin-bottom:5px;
'> ESG Dashboard </h1>
<p style='
    text-align:center;
    color:#d0d0d0;
    font-size:16px;
    font-style:italic;
    margin-top:-10px;
    letter-spacing:0.5px;
'> Elegant insights into ESG & Financial Performance </p>
""", unsafe_allow_html=True)

st.markdown("---")

# ------------------- LOAD DATA -------------------
@st.cache_data
def load_data():
    df = pd.DataFrame({
        "Company": ["TCS", "Infosys", "Reliance", "HDFC", "ITC", "Wipro", "Adani Green", "Axis Bank", "Nestle", "Tata Motors"],
        "Industry": ["Technology", "Technology", "Energy", "Finance", "Retail", "Technology", "Energy", "Finance", "Retail", "Automobile"],
        "Region": ["Asia"] * 10,
        "ESG_Overall": [78, 82, 68, 74, 88, 80, 70, 76, 85, 72],
        "Revenue": [50000, 46000, 120000, 70000, 40000, 30000, 25000, 35000, 42000, 38000],
        "ProfitMargin": [18, 20, 15, 22, 25, 17, 14, 19, 24, 16],
        "MarketCap": [1200000, 1100000, 2000000, 1500000, 800000, 700000, 650000, 900000, 1000000, 850000],
        "GrowthRate": [9.5, 8.2, 10.1, 7.9, 6.8, 8.5, 11.2, 7.5, 6.9, 9.0]
    })
    return df

df = load_data()

# ------------------- SIDEBAR -------------------
with st.sidebar:
    st.markdown("<h3 style='color:black; font-weight:700;'>🔍 Filters</h3>", unsafe_allow_html=True)

    industry = st.selectbox(
        "**Select Industry**",
        options=["All"] + sorted(df["Industry"].unique().tolist()),
        key="industry_filter"
    )

    region = st.selectbox(
        "**Select Region**",
        options=["All"] + sorted(df["Region"].unique().tolist()),
        key="region_filter"
    )

    esg_range = st.slider(
        "**Select ESG Score Range**",
        min_value=0, max_value=100, value=(20, 90),
        key="esg_range_filter"
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px; color:gray; text-align:center;'>Use filters to customize ESG insights.</p>", unsafe_allow_html=True)

# ------------------- FILTER LOGIC -------------------
filtered_df = df.copy()
if industry != "All":
    filtered_df = filtered_df[filtered_df["Industry"] == industry]
if region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region]
filtered_df = filtered_df[
    (filtered_df["ESG_Overall"] >= esg_range[0]) & (filtered_df["ESG_Overall"] <= esg_range[1])
]

# ------------------- METRICS -------------------
metrics = {
    "Avg Revenue": f"₹{filtered_df['Revenue'].mean():,.0f}",
    "Avg Profit Margin": f"{filtered_df['ProfitMargin'].mean():.2f}%",
    "Avg ESG Score": f"{filtered_df['ESG_Overall'].mean():.2f}",
    "Max Market Cap": f"₹{filtered_df['MarketCap'].max():,.0f}",
    "Avg Growth Rate": f"{filtered_df['GrowthRate'].mean():.2f}%"
}

st.markdown("<div style='display:flex; flex-wrap:wrap; gap:20px; justify-content:center;'>", unsafe_allow_html=True)
for metric, value in metrics.items():
    st.markdown(f"""
        <div style='
            background-color:#1a1a1a;
            border-radius:14px;
            width:300px;
            height:120px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
            box-shadow:0 4px 12px rgba(0,0,0,0.4);
            transition: transform 0.2s ease;
        '>
            <div style='font-size:14px; color:#b0b0b0; margin-bottom:4px; text-align:center;'>{metric}</div>
            <div style='font-size:20px; font-weight:700; color:#38bdf8; text-align:center;'>{value}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ------------------- GRAPHS -------------------

col1, col2 = st.columns(2)

# --- ESG Distribution (Box Plot - enhanced look) ---
with col1:
    st.subheader("📊 ESG Score Distribution")
    fig_box = px.box(
        filtered_df,
        x="Industry",
        y="ESG_Overall",
        color="Industry",
        title="Industry-wise ESG Distribution",
        points="all",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_box.update_layout(
        template='plotly_white',
        title_font=dict(size=18, color='#333'),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.05)",
        font=dict(color='#333', size=12),
        yaxis=dict(title='ESG Score', gridcolor='rgba(0,0,0,0.1)')
    )
    st.plotly_chart(fig_box, use_container_width=True)

# --- Revenue vs ESG (Scatter Plot) ---
with col2:
    st.subheader("💰 Revenue vs ESG Score")
    fig_scatter = px.scatter(
        filtered_df,
        x="Revenue",
        y="ESG_Overall",
        color="Industry",
        size="MarketCap",
        hover_name="Company",
        title="Revenue vs ESG Relationship",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_scatter.update_layout(
        template='plotly_white',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.05)",
        title_font=dict(size=18, color='#333'),
        font=dict(color='#333')
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- Profit Margin by Company ---
st.subheader("🏆 Profit Margin by Company")
fig_bar = px.bar(
    filtered_df.sort_values("ProfitMargin", ascending=False),
    x="Company",
    y="ProfitMargin",
    color="ProfitMargin",
    title="Company-wise Profit Margins",
    color_continuous_scale="Tealgrn"
)
fig_bar.update_layout(
    template='plotly_white',
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.05)",
    font=dict(color='#333'),
    title_font=dict(size=18, color='#333')
)
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>© 2025 ESG Insights | Designed by Aditi ✨</p>", unsafe_allow_html=True)
