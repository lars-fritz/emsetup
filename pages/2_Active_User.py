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

# --- Fee Calculation ---
if staking_mode == "Voting (earn fees)":
    user_share = my_tokens / circulating_supply
    user_weekly_fees = user_share * weekly_fees
    multiplier_used = np.ones(weeks)
else:
    # Multiplier staking: rewards grow based on multiplier, no extra token amount
    adjusted_tokens = my_tokens * multiplier_array
    user_share = adjusted_tokens / circulating_supply
    user_weekly_fees = user_share * weekly_fees
    multiplier_used = multiplier_array

# --- Result outputs ---
user_cumulative_fees = np.cumsum(user_weekly_fees)
relative_pct = (user_cumulative_fees / (my_tokens * initial_price)) * 100

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

# Create a DataFrame for the cumulative rewards from trading volume
df_multiplier = pd.DataFrame({
    "Week": weeks_array,
    "User Weekly Multiplier Rewards": user_weekly_rewards,
    "Cumulative Multiplier Rewards": user_cumulative_rewards
}).set_index("Week")

# Plot the cumulative rewards
st.line_chart(df_multiplier["Cumulative Multiplier Rewards"])

# --- Plots ---
st.subheader("📊 Fee Earnings Over Time")
st.line_chart(df[["Your Weekly Fees", "Cumulative Fees"]])

st.subheader("💸 Relative ROI Over Time (%)")
st.line_chart(df["Relative Earnings (%)"])

if staking_mode != "Voting (earn fees)":
    st.subheader("⚡ Multiplier Growth Over Time")
    st.line_chart(df["Multiplier"])

# Data Table for Fee Earnings
with st.expander("📋 Show Simulation Data"):
    st.dataframe(df.style.format({
        "Multiplier": "%.2f",
        "Your Weekly Fees": "%.2f",
        "Cumulative Fees": "%.2f",
        "Relative Earnings (%)": "%.2f"
    }))
