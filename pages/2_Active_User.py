import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Active User", layout="wide")
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

decay_rate = 1 - (decay_percent / 100)

# Sidebar inputs
with st.sidebar:
    st.header("Active User Settings")

    my_tokens = st.number_input("Your Token Holdings", value=10_000, format="%d")
    staking_mode = st.radio("Staking Mode", ["Voting (earn fees)", "Multiplier staking (no fees at first)"])

    st.markdown(f"**Current Value:** ${my_tokens * initial_price:,.2f}")

# --- Simulate emissions and supply ---
weeks_array = np.arange(weeks)
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

df = pd.DataFrame({
    "Week": weeks_array,
    "Multiplier": multiplier_used,
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

# --- Data Table ---
with st.expander("📋 Show Simulation Data"):
    st.dataframe(df.style.format({
        "Multiplier": "%.2f",
        "Your Weekly Fees": "%.2f",
        "Cumulative Fees": "%.2f",
        "Relative Earnings (%)": "%.2f"
    }))
