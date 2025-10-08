import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE CONFIG ---
st.set_page_config(page_title="ESG & Financial Insights", layout="wide")

# --- CUSTOM CSS FOR THEME ---
st.markdown("""
    <style>
    body {
        background-color: #0d1117;
        color: #e6e6e6;
    }
    [data-testid="stSidebar"] {
        background-color: #111418;
        color: white;
    }
    h1, h2, h3, h4 {
        color: #00FF7F;
        font-weight: 700;
    }
    .sidebar-header {
        color: black;
        font-weight: 900;
        font-size: 16px;
        margin-top: 20px;
    }
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("company_esg_financial_dataset.csv")
    return df

data = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.title("Filters")

st.sidebar.markdown('<div class="sidebar-header">Select Industry</div>', unsafe_allow_html=True)
industry = st.sidebar.selectbox(" ", options=["All"] + sorted(data['Industry'].unique().tolist()), key="industry_filter")

st.sidebar.markdown('<div class="sidebar-header">Select Region</div>', unsafe_allow_html=True)
regions = ["All", "Asia", "Europe", "North America", "South America", "Africa", "Oceania", "Middle East"]
region = st.sidebar.selectbox("  ", options=regions, key="region_filter")

st.sidebar.markdown('<div class="sidebar-header">Select ESG Score Range</div>', unsafe_allow_html=True)
score_range = st.sidebar.slider("   ", 0, 100, (20, 80), key="range_filter")

# --- APPLY FILTERS ---
filtered = data.copy()
if industry != "All":
    filtered = filtered[filtered["Industry"] == industry]
if region != "All":
    filtered = filtered[filtered["Region"].str.contains(region, case=False, na=False)]
filtered = filtered[(filtered["ESG_Score"] >= score_range[0]) & (filtered["ESG_Score"] <= score_range[1])]

# --- HEADER ---
st.markdown("<h1 style='text-align:center;'>ESG & Financial Performance Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- MAIN CONTENT ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("ESG Score Distribution")
    fig, ax = plt.subplots(facecolor="#0d1117")
    sns.histplot(filtered["ESG_Score"], kde=True, color="#00FF7F", ax=ax)
    ax.set_facecolor("#0d1117")
    ax.set_xlabel("ESG Score", color="white")
    ax.set_ylabel("Frequency", color="white")
    ax.tick_params(colors="white")
    st.pyplot(fig)

with col2:
    st.subheader("ESG Score by Industry (Box Plot)")
    fig, ax = plt.subplots(facecolor="#0d1117")
    sns.boxplot(
        data=filtered,
        x="Industry",
        y="ESG_Score",
        palette="Greens",
        linewidth=2,
        fliersize=0
    )
    ax.set_facecolor("#0d1117")
    ax.set_xlabel("Industry", color="white")
    ax.set_ylabel("ESG Score", color="white")
    ax.tick_params(colors="white", labelrotation=45)
    st.pyplot(fig)

st.markdown("---")

# --- CORRELATION ---
st.subheader("Correlation Between ESG Score & Financial Performance")
fig, ax = plt.subplots(facecolor="#0d1117")
sns.scatterplot(
    data=filtered,
    x="ESG_Score",
    y="Financial_Performance",
    color="#00FF7F",
    s=70
)
ax.set_facecolor("#0d1117")
ax.set_xlabel("ESG Score", color="white")
ax.set_ylabel("Financial Performance", color="white")
ax.tick_params(colors="white")
st.pyplot(fig)

# --- STOCK PERFORMANCE SECTION ---
st.subheader("Stock Performance Comparison")
stock_symbol = st.text_input("Enter a Stock Symbol (e.g., AAPL, TSLA):")

if stock_symbol:
    try:
        stock_data = yf.download(stock_symbol, period="1y")
        fig, ax = plt.subplots(facecolor="#0d1117")
        ax.plot(stock_data["Close"], color="#00FF7F", linewidth=2)
        ax.set_facecolor("#0d1117")
        ax.set_xlabel("Date", color="white")
        ax.set_ylabel("Closing Price", color="white")
        ax.tick_params(colors="white")
        st.pyplot(fig)
    except Exception as e:
        st.error("Error fetching stock data. Please check the symbol.")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>© 2025 ESG Financial Dashboard | Designed by Aditi</p>",
    unsafe_allow_html=True
)
