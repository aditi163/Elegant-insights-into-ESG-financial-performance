import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="ESG Cinematic Dashboard",
    layout="wide",
    page_icon="🌿"
)

# ------------------- Custom Dark Theme CSS -------------------
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stAppViewContainer"] {
    background-color: #121212;
    color: #e0e0e0;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
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
</style>
""", unsafe_allow_html=True)

# ------------------- Load Data -------------------
@st.cache_data(show_spinner=False)  # <-- changed from st.cache to st.cache_data
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
# Ensure sidebar code is executed always - no conditional blocks skipping it
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

# (Rest of your dashboard code for metric cards and plots remains the same...)

# Continue your metric cards, plots, and footer code as before
