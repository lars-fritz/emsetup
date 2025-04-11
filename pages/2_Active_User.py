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

    # Allow user to allocate tokens to voting and multiplier
    voting_tokens = st.number_input("Tokens for Voting on Fees", value=3000, max_value=my_tokens)
    multiplier_tokens = st.number_input("Tokens for Multiplier Staking", value=3000, max_value=my_tokens - voting_tokens)

    # Remainder automatically goes to volume staking
    volume_tokens = my_tokens - voting_tokens - multiplier_tokens
    st.markdown(f"**Tokens for Volume-based Emissions**: {volume_tokens} tokens")

    st.markdown(f"**Total Value:** ${my_tokens * initial_price:,.2f}")

# --- Simulation setup ---
weeks_array = np.arange(weeks)
decay_rate = 1 - (decay_percent / 100)

# Calculate emissions per week with exponential decay
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)

# Total circulating supply each week = initial tokens + emitted tokens up to that point
circulating_supply = initial_xtokens + cumulative_emissions

# --- Multiplier Logic for visual reference (not used directly in fees) ---
max_multiplier = 20
growth_rate = 0.07
# Simulates how a multiplier could grow with time (for general staking)
multiplier_array = 1 + (max_multiplier - 1) * (1 - np.exp(-growth_rate * weeks_array))

# --- Fee Calculation for Voting on Fees ---
# User's share of fees = (voting tokens / circulating supply) * weekly platform fees
voting_share = voting_tokens / circulating_supply
voting_weekly_fees = voting_share * weekly_fees
user_cumulative_fees = np.cumsum(voting_weekly_fees)

# ROI in % = Cumulative fees / initial token value
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
    platform_volume = st.number_input("Total Volume on Asset ($)", value=100_000_000, step=1_000_000)
with col3:
    user_volume = st.number_input("Your Weekly Volume ($)", value=2_000_000, step=100_000)

# --- Volume Emissions Logic with Staking Multiplier ---

# Explanation:
# 1. A base stake (e.g. 5000) represents competition from others.
# 2. Your effective stake increases by 5% each week (but not your actual tokens).
# 3. From the effective stake, we calculate a dynamic multiplier (1 + ratio * 3)
#    where ratio = effective / (effective + base_stake)
# 4. Your actual volume is boosted by this multiplier to get "effective volume"
# 5. You earn a share of emissions based on your effective volume share each week.

benchmark_stake = 5000
multiplied_stake = []

# Step 1: Compute weekly multipliers based on staking logic
for week in weeks_array:
    effective = volume_tokens * (1.05 ** week)  # Grows 5% weekly
    ratio = effective / (effective + benchmark_stake)
    multiplier = 1 + ratio * 3  # Boost max of 4x (1 + 3)
    multiplied_stake.append(multiplier)

multiplied_stake = np.array(multiplied_stake)

# Step 2: Effective volume = user_volume * multiplier
effective_user_volume = user_volume * multiplied_stake

# Step 3: Adjust platform volume to account for multiplier effect
adjusted_total_volume = platform_volume - user_volume + effective_user_volume

# Step 4: Compute weekly emissions to this asset
asset_weekly_emissions = weekly_emissions * asset_weight

# Step 5: Compute weekly user rewards from effective share of volume
user_volume_share = effective_user_volume / adjusted_total_volume
user_weekly_rewards = user_volume_share * asset_weekly_emissions
user_cumulative_rewards = np.cumsum(user_weekly_rewards)

# --- Baseline (No Multiplier) Rewards ---
baseline_rewards = (user_volume / platform_volume) * asset_weekly_emissions
cumulative_baseline_rewards = np.cumsum(baseline_rewards)

# --- Data Aggregation ---
df = pd.DataFrame({
    "Week": weeks_array,
    "Voting Weekly Fees": voting_weekly_fees,
    "Cumulative Voting Fees": user_cumulative_fees,
    "Relative Voting Earnings (%)": relative_pct,
    "Volume Weekly Rewards": user_weekly_rewards,
    "Cumulative Volume Rewards": user_cumulative_rewards,
    "Baseline Volume Rewards": baseline_rewards,
    "Cumulative Baseline Rewards": cumulative_baseline_rewards,
    "Volume Multiplier": multiplied_stake,
    "Multiplier Curve": multiplier_array
}).set_index("Week")

# --- ROI Plot ---
st.subheader("💸 Relative ROI from Voting Over Time (%)")
st.line_chart(df["Relative Voting Earnings (%)"])

# --- Weekly Comparison Plot ---
st.subheader("📈 Weekly Rewards from Volume Staking (with vs. without Multiplier)")
st.line_chart(df[["Volume Weekly Rewards", "Baseline Volume Rewards"]])

# --- Cumulative Comparison Plot ---
st.subheader("📊 Cumulative Rewards from Volume Staking")
st.line_chart(df[["Cumulative Volume Rewards", "Cumulative Baseline Rewards"]])

# --- Data Table ---
with st.expander("📋 Show Simulation Data"):
    st.dataframe(df.style.format({
        "Voting Weekly Fees": "%.2f",
        "Cumulative Voting Fees": "%.2f",
        "Relative Voting Earnings (%)": "%.2f",
        "Volume Weekly Rewards": "%.2f",
        "Cumulative Volume Rewards": "%.2f",
        "Baseline Volume Rewards": "%.2f",
        "Cumulative Baseline Rewards": "%.2f",
        "Volume Multiplier": "%.2f"
    }))
