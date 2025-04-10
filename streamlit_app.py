import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Emission Simulator", layout="wide")
st.title("📊 Emission & Tokenomics Simulator")

# Sidebar inputs
with st.sidebar:
    st.header("Simulation Settings")

    initial_xtokens = st.number_input("Initial xTokens (Voting)", value=16_000_000, step=100_000, format="%d")
    locked_tokens = st.number_input("Locked Tokens (Non-Voting)", value=84_000_000, step=1_000_000, format="%d")
    initial_price = st.number_input("Initial Token Price ($)", value=0.25, step=0.01, format="%.2f")
    weekly_fees = st.number_input("Weekly Fee Revenue ($)", value=20_000, step=1_000, format="%d")
    base_emission = st.number_input("Initial Weekly Emission", value=800_000, step=10_000, format="%d")
    decay_percent = st.number_input("Emission Decay per Week (%)", value=2.0, step=0.1, format="%.1f")
    weeks = st.slider("Number of Weeks", min_value=10, max_value=520, value=104)
    decay_rate = 1 - (decay_percent / 100)

# Simulation logic
weeks_array = np.arange(weeks)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)

circulating_supply = initial_xtokens + cumulative_emissions
total_supply_fdv = locked_tokens + initial_xtokens + cumulative_emissions

valuation = circulating_supply * initial_price
fdv = total_supply_fdv * initial_price

cumulative_fees = np.cumsum(np.full(weeks, weekly_fees))

df = pd.DataFrame({
    "Week": weeks_array,
    "Weekly Emission": weekly_emissions,
    "Circulating Voting Supply": circulating_supply,
    "Total Supply (FDV)": total_supply_fdv,
    "Valuation ($)": valuation,
    "FDV ($)": fdv,
    "Cumulative Fees ($)": cumulative_fees
}).set_index("Week")

# Plots
st.subheader("📈 Emissions & Supply Over Time")
st.line_chart(df[["Weekly Emission", "Circulating Voting Supply", "Total Supply (FDV)"]])

st.subheader("💰 Valuation Over Time")
st.line_chart(df[["Valuation ($)", "FDV ($)"]])

st.subheader("🧾 Cumulative Protocol Fees")
st.line_chart(df["Cumulative Fees ($)"])

# Data table
with st.expander("📋 Show Data Table"):
    st.dataframe(df.style.format({
        "Weekly Emission": "%.0f",
        "Circulating Voting Supply": "%.0f",
        "Total Supply (FDV)": "%.0f",
        "Valuation ($)": "%.2f",
        "FDV ($)": "%.2f",
        "Cumulative Fees ($)": "%.2f"
    }))

