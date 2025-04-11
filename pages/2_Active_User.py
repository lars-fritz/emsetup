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
    
    # Split tokens between voting and volume-based staking
    voting_tokens = st.number_input("Tokens for Voting on Fees", value=5000, max_value=my_tokens)
    volume_tokens = my_tokens - voting_tokens
    st.markdown(f"**Tokens for Volume-based Emissions**: {volume_tokens} tokens")

    staking_mode = st.radio("Staking Mode", ["Voting (earn fees)", "Multiplier staking (no fees at first)"])

    st.markdown(f"**Current Value:** ${my_tokens * initial_price:,.2f}")

# Simulation setup
weeks_array = np.arange(weeks)
decay_rate = 1 - (decay_percent / 100)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)
circulating_supply = initial_xtokens + cumulative_emissions

# --- Multiplier Logic ---
max_multiplier = 20
growth_rate = 0.07  # Adjust this to tweak how fast multiplier grows
multiplier_array = 1 + (max_multiplier - 1) * (1 - np.exp(-growth_rate * weeks_array))

# --- Fee Calculation for Voting ---
voting_share = voting_tokens / circulating_supply
voting_weekly_fees = voting_share * weekly_fees

# --- Volume-based Emissions Section (New feature) ---
st.subheader("📦 Emissions from Trading Volume (Multiplier Logic)")

# Inputs for volume-based emission
col1, col2, col3 = st.columns(3)
with col1:
    asset_weight = st.number_input("Asset Weight (% of total emissions)", value=10.0, step=0.5) / 100
with col2:
    total_volume = st.number_input("Total Volume on Asset ($)", value=100_000_000, step=1_000_000)
with col3:
    user_volume = st.number_input("Your Weekly Volume ($)", value=2_000_000, step=100_000)

# Emission to asset
asset_weekly_emissions = weekly_emissions * asset_weight

# User share of asset volume
user_share_of_volume = user_volume / total_volume
user_weekly_rewards = user_share_of_volume * asset_weekly_emissions
user_cumulative_rewards = np.cumsum(user_weekly_rewards)

# --- Cumulative Rewards ---
user_cumulative_fees = np.cumsum(voting_weekly_fees)
relative_pct = (user_cumulative_fees / (my_tokens * initial_price)) * 100

# Create DataFrame for voting and volume rewards
df = pd.DataFrame({
    "Week": weeks_array,
    "Voting Weekly Fees": voting_weekly_fees,
    "Cumulative Voting Fees": user_cumulative_fees,
    "Relative Voting Earnings (%)": relative_pct,
    "Volume Weekly Rewards": user_weekly_rewards,
    "Cumulative Volume Rewards": user_cumulative_rewards
}).set_index("Week")

# --- Plots ---
st.subheader("📊 Cumulative Fees and Rewards (Voting + Volume)")
st.line_chart(df[["Cumulative Voting Fees", "Cumulative Volume Rewards"]])

st.subheader("💸 Relative ROI Over Time (%)")
st.line_chart(df["Relative Voting Earnings (%)"])

# Data Table for Fee Earnings and Volume Rewards
with st.expander("📋 Show Simulation Data"):
    st.dataframe(df.style.format({
        "Voting Weekly Fees": "%.2f",
        "Cumulative Voting Fees": "%.2f",
        "Relative Voting Earnings (%)": "%.2f",
        "Volume Weekly Rewards": "%.2f",
        "Cumulative Volume Rewards": "%.2f"
    }))
