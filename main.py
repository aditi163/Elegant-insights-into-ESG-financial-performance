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

# ------------------- Custom Dark Theme CSS -------------------
st.markdown("""
<style>
/* Remove the line below that hides the sidebar content, and ensure sidebar padding/style is correct */
/* #MainMenu, footer, header {visibility: hidden;} */
[data-testid="stAppViewContainer"] {
    background-color: #121212;
    color: #e0e0e0;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
/* NOTE: The padding applied here should render the sidebar content which is correctly defined below */
[data-testid="stSidebar"] {
    background: #1e1e1e;
    padding: 2rem;
    color: #e0e0e0;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}
[data-testid="stSidebar"] h2 {
    color: #e0e0e0 !important;
    font-weight: 600;
}
.card {
    background: #1e1e1e;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.5);
    transition: transform 0.3s, box-shadow 0.3s;
    text-align: center;
    border: 1px solid #424242;
}
.card:hover { 
    transform: translateY(-8px); 
    box-shadow: 0 10px 25px rgba(0,200,83,0.3);
}
.card-title { font-size: 16px; color: #b0b0b0; margin-bottom: 6px; font-weight: 500;}
.card-value { font-size: 28px; font-weight: 700; color: #00C853; }
.footer { 
    text-align: center; 
    color: #a0a0a0; 
    font-size: 14px; 
    margin-top: 3rem; 
    padding-top: 1rem;
    border-top: 1px solid #424242;
}
/* Fixing the visibility of header/footer/mainmenu in wide-mode to keep sidebar */
#MainMenu, footer {visibility: hidden;}
/* Re-enabling the header if necessary, but hiding the main elements is often the cause of sidebar issues */
</style>
""", unsafe_allow_html=True)

# ------------------- Load Data -------------------
# RESOLUTION: Replaced st.cache with st.cache_data
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
# The content below is correctly placed within the sidebar using 'with st.sidebar:'
with st.sidebar:
    st.header("Filters")
    industries = sorted(df["Industry"].dropna().unique())
    regions = sorted(df["Region"].dropna().unique())

    selected_industry = st.selectbox("Select Industry", industries)
    selected_region = st.selectbox("Select Region", regions)
    esg_min, esg_max = st.slider("Select ESG Overall Range", 0, 100, (60, 95))

filtered_df = df[
    (df["Industry"] == selected_industry) &
    (df["Region"] == selected_region) &
    (df["ESG_Overall"] >= esg_min) &
    (df["ESG_Overall"] <= esg_max)
]

# ------------------- Header -------------------
st.markdown("""
<div style='text-align:center; margin-bottom:20px;'>
    <h1 style='font-size:50px; letter-spacing:2px; margin:0;'>ESG Dashboard</h1>
    <p class='subtitle'>Elegant insights into ESG & financial performance</p>
</div>
""", unsafe_allow_html=True)

# ------------------- Metric Cards -------------------
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
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    # ESG Score Distribution (Histogram)
    st.subheader("ESG Score Distribution")
    fig_hist = px.histogram(
        filtered_df,
        x="ESG_Overall",
        nbins=15,
        color_discrete_sequence=["#00C853"],
        title="Frequency of ESG Overall Scores"
    )
    fig_hist.update_traces(marker=dict(line=dict(width=1, color='rgba(0,0,0,0.2)')))
    fig_hist.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="ESG Overall Score", showgrid=True, gridcolor="#2b2b2b"),
        yaxis=dict(title="Count", showgrid=True, gridcolor="#2b2b2b"),
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # Scatter and Box plots side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("MarketCap vs ESG Score")
        fig_scatter = px.scatter(
            filtered_df,
            x="ESG_Overall",
            y="MarketCap",
            size="Revenue",
            color="ProfitMargin",
            hover_data=["CompanyName", "GrowthRate"],
            color_continuous_scale=px.colors.sequential.Viridis,
            title="Market Capitalization vs. ESG Performance"
        )
        fig_scatter.update_traces(marker=dict(line=dict(width=1, color='rgba(0,0,0,0.3)')))
        fig_scatter.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="ESG Overall Score", showgrid=True, gridcolor="#2b2b2b"),
            yaxis=dict(title="Market Cap (₹)", showgrid=True, gridcolor="#2b2b2b")
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("Profit Margin by Industry")
        fig_box = px.box(
            df,
            x="Industry",
            y="ProfitMargin",
            color="Industry",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            points="all",
            hover_data={"ProfitMargin": True, "Industry": True}
        )
        fig_box.update_traces(
            boxmean='sd',
            marker=dict(size=5, opacity=0.8, color="#00C853", line=dict(width=1, color='rgba(0,0,0,0.5)')),
            line=dict(width=2, color="#00C853"),
            fillcolor='rgba(0, 200, 83, 0.2)',
            opacity=0.8,
            jitter=0.4
        )
        fig_box.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title=dict(
                    text="Industry",
                    font=dict(color='#e0e0e0')
                ),
                tickangle=-30,
                showgrid=False,
                color='#e0e0e0'
            ),
            yaxis=dict(
                title=dict(
                    text="Profit Margin (%)",
                    font=dict(color='#e0e0e0')
                ),
                showgrid=True,
                gridcolor="#2b2b2b",
                color='#e0e0e0'
            )
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # ESG Radar Chart
    st.subheader("ESG Component Breakdown (Radar Chart)")
    categories = ['ESG_Environmental', 'ESG_Social', 'ESG_Governance']
    avg_scores = [filtered_df[c].mean() for c in categories]
    r_values = avg_scores + avg_scores[:1]
    theta_values = categories + categories[:1]

    fig_radar = go.Figure(data=go.Scatterpolar(
        r=r_values,
        theta=theta_values,
        fill='toself',
        line_color="#00C853",
        line=dict(width=4),
        marker=dict(size=8),
        hovertemplate="<b>%{theta}</b>: %{r:.2f}<extra></extra>"
    ))
    fig_radar.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        polar=dict(
            bgcolor='#1e1e1e',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="#2b2b2b",
                linecolor="#424242",
                color='#e0e0e0'
            ),
            angularaxis=dict(
                linecolor='#424242'
            )
        ),
        font_size=14,
        title="Average Component Scores"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ------------------- Footer -------------------
st.markdown("<div class='footer'>🌿 ESG Dashboard &copy; 2025 </div>", unsafe_allow_html=True)
