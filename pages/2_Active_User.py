import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Active User", layout="wide")
st.title("🚀 Active User Fee Earnings")

# Sidebar inputs
with st.sidebar:
    st.header("Active User Settings")

    my_tokens = st.number_input("Your Token Holdings", value=10_000, format="%d")
    initial_price = st.number_input("Initial Token Price ($)", value=0.25, step=0.01, format="%.2f")

    staking_mode = st.radio("Staking Mode", ["Voting (earn fees)", "Multiplier staking (no fees at first)"])

    st.markdown(f"**Current Value:** ${my_tokens * initial_price:,.2f}")

# Constants
initial_xtokens = 16_000_000
locked_tokens = 84_000_000
weekly_fees = 20_000
base_emission = 800_000
decay_percent = 2.0
decay_rate = 1 - (decay_percent / 100)
weeks = 104

# Simulation setup
weeks_array = np.arange(weeks)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)
circulating_supply = initial_xtokens + cumulative_emissions

# --- Multiplier Logic (exponential growth toward max 20x) ---
max_multiplier = 20
growth_rate = 0.07  # tuning how fast multiplier grows
multiplier_array = 1 + (max_multiplier - 1) * (1 - np.exp(-growth_rate * weeks_array))

# Fee logic
if staking_mode == "Voting (earn fees)":
    user_share = my_tokens / circulating_supply
    user_weekly_fees = user_share * weekly_fees
else:
    # Multiplier staking, no fees early on, earn based on multiplier
    adjusted_tokens = my_tokens * multiplier_array
    user_share = adjusted_tokens / circulating_supply
    user_weekly_fees = user_share * weekly_fees

# Fee and value outputs
user_cumulative_fees = np.cumsum(user_weekly_fees)
relative_pct = (user_cumulative_fees / (my_tokens * initial_price)) * 100
token_value = my_tokens * initial_price

df = pd.DataFrame({
    "Week": weeks_array,
    "Multiplier": multiplier_array if staking_mode != "Voting (earn fees)" else np.ones(weeks),
    "Your Weekly Fees": user_weekly_fees,
    "Cumulative Fees": user_cumulative_fees,
    "Relative Earnings (%)": relative_pct
}).set_index("Week")

# --- Plots ---
st.subheader("📊 Fee Earnings Over Time")
st.line_chart(df[["Your Weekly Fees", "Cumulative Fees"]])

st.subheader("💸 Relative ROI Over Time (%)")
st.line_chart(df["Relative Earnings (%)"])

if staking_mode != "Voting (earn fees)":
    st.subheader("⚡ Multiplier Growth Over Time")
    st.line_chart(df["Multiplier"])

# Data Table
with st.expander("📋 Show Simulation Data"):
    st.dataframe(df.style.format({
        "Multiplier": "%.2f",
        "Your Weekly Fees": "%.2f",
        "Cumulative Fees": "%.2f",
        "Relative Earnings (%)": "%.2f"
    }))

