import streamlit as st
import pandas as pd
import numpy as np

# Make sure we are working with standard decimal separator (period) for inputs
st.set_page_config(page_title="Token Emission Simulator", layout="wide")
st.title("📈 Token Emission Schedule Simulator")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Simulation Settings")

# Use explicit format settings for each input to prevent local formatting issues
initial_tokens = st.sidebar.number_input("Initial Token Supply", value=16000000, format="%d")
initial_price = st.sidebar.number_input("Initial Token Price ($)", value=0.45, step=0.01, format="%.2f")
weekly_fees = st.sidebar.number_input("Weekly Fee Revenue ($)", value=20000, step=1000, format="%d")
base_emission = st.sidebar.number_input("Initial Weekly Emission", value=300000, step=10000, format="%d")

# Input decay as a percentage (percent is used for clarity)
decay_percent = st.sidebar.number_input("Emission Decay per Week (%)", value=2.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
decay_rate = 1 - decay_percent / 100  # Convert percent to multiplier

weeks = st.sidebar.slider("Number of Weeks to Simulate", min_value=10, max_value=520, value=104, step=1)
my_tokens = st.sidebar.number_input("Your Token Holdings", value=10000, format="%d")

# Locked tokens (do not participate in voting but contribute to FDV)
locked_tokens = 84000000

# --- Simulation ---
weeks_list = np.arange(weeks)
emissions = base_emission * decay_rate ** weeks_list
cumulative_tokens = initial_tokens + np.cumsum(emissions)
total_supply = cumulative_tokens + locked_tokens  # Add locked tokens to total supply
valuations = cumulative_tokens * initial_price

# FDV calculation (fully diluted valuation)
fdv = total_supply * initial_price

your_share_pct = my_tokens / cumulative_tokens
your_weekly_fee_share = your_share_pct * weekly_fees
your_cumulative_fees = np.cumsum(your_weekly_fee_share)
total_cumulative_fees = np.cumsum([weekly_fees] * weeks)

# Calculate the initial investment and the relative earnings
initial_investment = my_tokens * initial_price
relative_cumulative_earnings = (your_cumulative_fees / initial_investment) * 100

# --- DataFrame ---
df = pd.DataFrame({
    "Week": weeks_list,
    "Weekly Emission": emissions,
    "Total Supply": cumulative_tokens,
    "Total Supply (with Locked Tokens)": total_supply,
    "FDV ($)": fdv,
    "Valuation ($)": valuations,
    "Cumulative Fees ($)": total_cumulative_fees,
    "Your Fee Share ($)": your_weekly_fee_share,
    "Your Cumulative Fees ($)": your_cumulative_fees,
    "Relative Cumulative Earnings (%)": relative_cumulative_earnings
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

    st.subheader("📦 Cumulative Protocol Fees")
    st.line_chart(df.set_index("Week")[["Cumulative Fees ($)"]])

with col2:
    st.subheader("💰 Valuation Over Time")
    st.line_chart(df.set_index("Week")[["Valuation ($)"]])

    st.subheader("💼 Your Cumulative Fee Earnings")
    st.line_chart(df.set_index("Week")[["Your Cumulative Fees ($)"]])

    st.subheader("📈 Relative Cumulative Fee Earnings (%)")
    st.line_chart(df.set_index("Week")[["Relative Cumulative Earnings (%)"]])

    st.subheader("💵 Fully Diluted Valuation (FDV) Over Time")
    st.line_chart(df.set_index("Week")[["FDV ($)"]])

# --- Optional Data Table ---
with st.expander("📋 See Raw Data Table"):
    # Ensure all numeric columns are formatted with US decimal style (periods, no commas)
    st.dataframe(df.style.format({
        "Weekly Emission": "%.0f",  # Rounded integer for emissions
        "Total Supply": "%.0f",     # Rounded integer for token supply (without locked tokens)
        "Total Supply (with Locked Tokens)": "%.0f",  # Rounded integer for total supply (with locked tokens)
        "FDV ($)": "%.2f",    # 2 decimal places for FDV
        "Valuation ($)": "%.2f",    # 2 decimal places for valuation
        "Your Fee Share ($)": "%.2f",  # 2 decimal places for user's fee share
        "Your Cumulative Fees ($)": "%.2f",  # 2 decimal places for cumulative fees
        "Cumulative Fees ($)": "%.2f",  # 2 decimal places for cumulative protocol fees
        "Relative Cumulative Earnings (%)": "%.2f"  # 2 decimal places for relative earnings in percent
    }))
