import streamlit as st
import pandas as pd
import numpy as np

# Page setup
st.set_page_config(page_title="Emission Simulator", layout="wide")
st.title("📊 Emission & Tokenomics Simulator")

st.markdown("""
Welcome to the **Token Emission & Valuation Simulator**.  
Use the controls in the sidebar to explore how emissions, token supply, valuation, and fee generation evolve over time under customizable parameters.

This simulation distinguishes between:
- **Voting tokens** (xTokens) that participate in fee distribution,
- **Locked tokens** which count towards the total supply but not towards voting,
- **Weekly emissions** that decrease over time via a decay rate.
""")

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

# --- Emission Chart ---
st.subheader("📤 Weekly Token Emissions")
st.markdown("This plot shows how many tokens are emitted each week, declining based on the decay rate.")
st.line_chart(df["Weekly Emission"])

# --- Supply Chart ---
st.subheader("📈 Emissions & Supply Over Time")
st.markdown("Here you can see the growth of circulating (voting) supply and total supply including locked tokens.")
st.line_chart(df[["Circulating Voting Supply", "Total Supply (FDV)"]])

# --- Valuation Chart ---
st.subheader("💰 Valuation Over Time")
st.markdown("Circulating market cap and FDV are estimated using the current token price.")
st.line_chart(df[["Valuation ($)", "FDV ($)"]])

# --- Fee Chart ---
st.subheader("🧾 Cumulative Protocol Fees")
st.markdown("This shows the total protocol revenue (fees) accumulated over the simulation period.")
st.line_chart(df["Cumulative Fees ($)"])

# --- Table ---
with st.expander("📋 Show Data Table"):
    st.markdown("Explore the raw data behind the simulation.")
    st.dataframe(df.style.format({
        "Weekly Emission": "%.0f",
        "Circulating Voting Supply": "%.0f",
        "Total Supply (FDV)": "%.0f",
        "Valuation ($)": "%.2f",
        "FDV ($)": "%.2f",
        "Cumulative Fees ($)": "%.2f"
    }))
