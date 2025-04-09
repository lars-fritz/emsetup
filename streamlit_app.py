import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Token Emission Simulator", layout="wide")
st.title("📈 Token Emission Schedule Simulator")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Simulation Settings")

initial_tokens = st.sidebar.number_input("Initial Token Supply", value=16_000_000)
initial_price = st.sidebar.number_input("Initial Token Price ($)", value=0.45, step=0.01)
weekly_fees = st.sidebar.number_input("Weekly Fee Revenue ($)", value=20_000)
base_emission = st.sidebar.number_input("Initial Weekly Emission", value=300_000)
decay_rate = st.sidebar.number_input("Decay Rate per Week (e.g., 0.98)", value=0.98)
weeks = st.sidebar.slider("Number of Weeks to Simulate", min_value=10, max_value=520, value=104)
my_tokens = st.sidebar.number_input("Your Token Holdings", value=10_000)

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

    st.subheader("📦 Cumulative Protocol Fees Collected")
    st.line_chart(df.set_index("Week")[["Cumulative Fees ($)"]])

    st.subheader("💼 Your Cumulative Fee Earnings")
    st.line_chart(df.set_index("Week")[["Your Cumulative Fees ($)"]])

# --- Optional Data Table ---
with st.expander("📋 See Raw Data Table"):
    st.dataframe(df.style.format({
        "Weekly Emission": "{:,.0f}",
        "Total Supply": "{:,.0f}",
        "Valuation ($)": "${:,.0f}",
        "Your Fee Share ($)": "${:,.2f}",
        "Your Cumulative Fees ($)": "${:,.2f}"
    }))
