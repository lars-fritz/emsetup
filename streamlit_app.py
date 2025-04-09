import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Token Emission Simulator", layout="wide")
st.title("📈 Token Emission Schedule Simulator")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Simulation Settings")

initial_tokens = st.sidebar.number_input("Initial Token Supply", value=16000000, format="%d")
initial_price = st.sidebar.number_input("Initial Token Price ($)", value=0.45, step=0.01, format="%.2f")
weekly_fees = st.sidebar.number_input("Weekly Fee Revenue ($)", value=20000, step=1000, format="%d")
base_emission = st.sidebar.number_input("Initial Weekly Emission", value=300000, step=10000, format="%d")

# Input decay as a percentage
decay_percent = st.sidebar.number_input("Emission Decay per Week (%)", value=2.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
decay_rate = 1 - decay_percent / 100  # Convert percent to multiplier

weeks = st.sidebar.slider("Number of Weeks to Simulate", min_value=10, max_value=520, value=104, step=1)
my_tokens = st.sidebar.number_input("Your Token Holdings", value=10000, format="%d")

# --- Simulation ---
weeks_list = np.arange(weeks)
emissions = base_emission * decay_rate ** weeks_list
cumulative_tokens = initial_tokens + np.cumsum(emissions)
valuations = cumulative_tokens * initial_price

your_share_pct = my_tokens / cumulative_tokens
your_weekly_fee_share = your_share_pct * weekly_fees
your_cumulative_fees = np.cumsum(your_weekly_fee_share)
total_cumulative_fees = np.cumsum([weekly_fees] * weeks)

# --- DataFrame ---
df = pd.DataFrame({
    "Week": weeks_list,
    "Weekly Emission": emissions,
    "Total Supply": cumulative_tokens,
    "Valuation ($)": valuations,
    "Cumulative Fees ($)": total_cumulative_fees,
    "Your Fee Share ($)": your_weekly_fee_share,
    "Your Cumulative Fees ($)": your_cumulative_fees
})

# --- Layout Columns ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Token Supply Over Time")
    st.line_chart(df.set_index("Week")[["Total Supply"]])

    st.subheader("🪙 Weekly Emissions")
    st.bar_chart(df.set_index("Week")[["Weekly Emission"]])

    st.subheader("💸 Your Weekly Fee Earnings")
    st.line_chart(df.set_index("Week")[["Your Fee Share ($)"]])

with col2:
    st.subheader("💰 Valuation Over Time")
    st.line_chart(df.set_index("Week")[["Valuation ($)"]])

    st.subheader("📦 Cumulative Protocol Fees")
    st.line_chart(df.set_index("Week")[["Cumulative Fees ($)"]])

    st.subheader("💼 Your Cumulative Fee Earnings")
    st.line_chart(df.set_index("Week")[["Your Cumulative Fees ($)"]])

# --- Optional Data Table ---
with st.expander("📋 See Raw Data Table"):
    st.dataframe(df.style.format({
        "Weekly Emission": "%.0f",
        "Total Supply": "%.0f",
        "Valuation ($)": "%.2f",
        "Your Fee Share ($)": "%.2f",
        "Your Cumulative Fees ($)": "%.2f",
        "Cumulative Fees ($)": "%.2f"
    }))
