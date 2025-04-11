import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Active User Fee Earnings", layout="wide")
st.title("🚀 Active User Fee Earnings")

# --- Pull simulation settings from main page ---
try:
    initial_xtokens = st.session_state.initial_xtokens
    locked_tokens = st.session_state.locked_tokens
    initial_price = st.session_state.initial_price
    weekly_fees = st.session_state.weekly_fees
    base_emission = st.session_state.base_emission
    decay_percent = st.session_state.decay_percent
    weeks = st.session_state.weeks
except AttributeError:
    st.error("⚠️ Please visit the main page first to set the tokenomics parameters.")
    st.stop()

# Sidebar inputs
with st.sidebar:
    st.header("Active User Settings")

    my_tokens = st.number_input("Your Token Holdings", value=10_000, format="%d")

    voting_tokens = st.number_input("Tokens for Voting on Fees", value=3000, max_value=my_tokens)
    multiplier_tokens = st.number_input("Tokens for Multiplier Staking", value=3000, max_value=my_tokens - voting_tokens)

    volume_tokens = my_tokens - voting_tokens - multiplier_tokens
    st.markdown(f"**Tokens for Volume-based Emissions**: {volume_tokens} tokens")

    st.markdown(f"**Total Value:** ${my_tokens * initial_price:,.2f}")

# --- Simulation setup ---
weeks_array = np.arange(weeks)
decay_rate = 1 - (decay_percent / 100)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)
circulating_supply = initial_xtokens + cumulative_emissions

# --- Multiplier Logic ---
max_multiplier = 20
growth_rate = 0.07
multiplier_array = 1 + (max_multiplier - 1) * (1 - np.exp(-growth_rate * weeks_array))

# --- Fee Calculation for Voting ---
voting_share = voting_tokens / circulating_supply
voting_weekly_fees = voting_share * weekly_fees
user_cumulative_fees = np.cumsum(voting_weekly_fees)
relative_pct = (user_cumulative_fees / (my_tokens * initial_price)) * 100

# --- Cumulative Voting Fees Plot ---
st.subheader("📊 Cumulative Voting Fees")
st.line_chart(user_cumulative_fees)

# --- Volume Emissions Inputs ---
st.subheader("📦 Emissions from Trading Volume (Multiplier Asset)")

col1, col2, col3 = st.columns(3)
with col1:
    asset_weight = st.number_input("Asset Weight (% of Total Emissions)", value=10.0, step=0.5) / 100
with col2:
    total_volume = st.number_input("Total Volume on Asset ($)", value=100_000_000, step=1_000_000)
with col3:
    user_volume = st.number_input("Your Weekly Volume ($)", value=2_000_000, step=100_000)

# --- Volume Emissions Logic ---
asset_weekly_emissions = weekly_emissions * asset_weight
user_share_of_volume = user_volume / total_volume
user_weekly_rewards = user_share_of_volume * asset_weekly_emissions
user_cumulative_rewards = np.cumsum(user_weekly_rewards)

# --- Data Aggregation ---
df = pd.DataFrame({
    "Week": weeks_array,
    "Voting Weekly Fees": voting_weekly_fees,
    "Cumulative Voting Fees": user_cumulative_fees,
    "Relative Voting Earnings (%)": relative_pct,
    "Volume Weekly Rewards": user_weekly_rewards,
    "Cumulative Volume Rewards": user_cumulative_rewards,
    "Multiplier": multiplier_array
}).set_index("Week")

# --- ROI Plot ---
st.subheader("💸 Relative ROI from Voting Over Time (%)")
st.line_chart(df["Relative Voting Earnings (%)"])

# --- Data Table ---
with st.expander("📋 Show Simulation Data"):
    st.dataframe(df.style.format({
        "Voting Weekly Fees": "%.2f",
        "Cumulative Voting Fees": "%.2f",
        "Relative Voting Earnings (%)": "%.2f",
        "Volume Weekly Rewards": "%.2f",
        "Cumulative Volume Rewards": "%.2f",
        "Multiplier": "%.2f"
    }))
