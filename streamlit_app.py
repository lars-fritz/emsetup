import streamlit as st
import pandas as pd
import numpy as np

# Page setup
st.set_page_config(page_title="Token Emission Simulator", layout="wide")
st.title("📈 Token Emission Schedule Simulator")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Simulation Settings")

initial_tokens = st.sidebar.number_input("Initial Token Supply", value=16_000_000, format="%d")
initial_price = st.sidebar.number_input("Initial Token Price ($)", value=0.45, step=0.01, format="%.2f")
weekly_fees = st.sidebar.number_input("Weekly Fee Revenue ($)", value=20_000, step=1_000, format="%d")
base_emission = st.sidebar.number_input("Initial Weekly Emission", value=300_000, step=10_000, format="%d")
decay_percent = st.sidebar.number_input("Emission Decay per Week (%)", value=2.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
decay_rate = 1 - (decay_percent / 100)
weeks = st.sidebar.slider("Number of Weeks to Simulate", min_value=10, max_value=520, value=104)
my_tokens = st.sidebar.number_input("Your Token Holdings", value=10_000, format="%d")

# Locked tokens that don't count for voting, but do count for FDV
locked_tokens = 84_000_000

# --- Simulation ---
weeks_array = np.arange(weeks)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)
circulating_supply = initial_tokens + cumulative_emissions
total_supply = circulating_supply + locked_tokens
valuation = circulating_supply * initial_price
fdv = total_supply * initial_price

# Fee share calculations
user_share_ratio = my_tokens / circulating_supply
user_weekly_fees = user_share_ratio * weekly_fees
user_cumulative_fees = np.cumsum(user_weekly_fees)
cumulative_protocol_fees = np.cumsum(np.full(weeks, weekly_fees))

# Return on investment
initial_investment = my_tokens * initial_price
relative_earnings_pct = (user_cumulative_fees / initial_investment) * 100

# --- DataFrame for plotting ---
df = pd.DataFrame({
    "Week": weeks_array,
    "Weekly Emission": weekly_emissions,
    "Circulating Supply": circulating_supply,
    "Total Supply (with Locked Tokens)": total_supply,
    "Valuation ($)": valuation,
    "FDV ($)": fdv,
    "Your Weekly Fee Earnings ($)": user_weekly_fees,
    "Your Cumulative Fees ($)": user_cumulative_fees,
    "Cumulative Protocol Fees ($)": cumulative_protocol_fees,
    "Relative Cumulative Earnings (%)": relative_earnings_pct
})

df.set_index("Week", inplace=True)

# --- Plots ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🪙 Weekly Emissions")
    st.bar_chart(df["Weekly Emission"])

    st.subheader("📈 Circulating Supply")
    st.line_chart(df["Circulating Supply"])

    st.subheader("💸 Your Weekly Fee Earnings")
    st.line_chart(df["Your Weekly Fee Earnings ($)"])

    st.subheader("📦 Cumulative Protocol Fees")
    st.line_chart(df["Cumulative Protocol Fees ($)"])

with col2:
    st.subheader("💰 Valuation Over Time (Circulating Supply × Price)")
    st.line_chart(df["Valuation ($)"])

    st.subheader("💼 Your Cumulative Fee Earnings")
    st.line_chart(df["Your Cumulative Fees ($)"])

    st.subheader("📊 Relative Earnings vs Initial Investment (%)")
    st.line_chart(df["Relative Cumulative Earnings (%)"])

    st.subheader("💵 Fully Diluted Valuation (FDV)")
    st.line_chart(df["FDV ($)"])

# --- Optional Table ---
with st.expander("📋 Full Data Table"):
    st.dataframe(df.style.format({
        "Weekly Emission": "%.0f",
        "Circulating Supply": "%.0f",
        "Total Supply (with Locked Tokens)": "%.0f",
        "Valuation ($)": "%.2f",
        "FDV ($)": "%.2f",
        "Your Weekly Fee Earnings ($)": "%.2f",
        "Your Cumulative Fees ($)": "%.2f",
        "Cumulative Protocol Fees ($)": "%.2f",
        "Relative Cumulative Earnings (%)": "%.2f"
    }))
