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

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("Active User Settings")
    my_tokens = st.number_input("Your Total Token Holdings", value=10_000, format="%d")

    st.subheader("🎯 Token Allocation (by amount)")
    vote_tokens = st.number_input("Tokens allocated to Voting", value=4000, step=100)
    multi_tokens = st.number_input("Tokens allocated to Multiplier Staking", value=3000, step=100)
    hatch_tokens = st.number_input("Tokens allocated to Hatching", value=3000, step=100)

# --- Validate Allocation ---
allocated_total = vote_tokens + multi_tokens + hatch_tokens
if allocated_total > my_tokens:
    st.error(f"🚫 Allocated {allocated_total:,} tokens but you only have {my_tokens:,}. Please reduce allocations.")
    st.stop()

# --- Simulate emissions and supply ---
weeks_array = np.arange(weeks)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)
circulating_supply = initial_xtokens + cumulative_emissions

# --- Voting Fee Calculation ---
vote_share = vote_tokens / circulating_supply
vote_weekly_fees = vote_share * weekly_fees
vote_cumulative_fees = np.cumsum(vote_weekly_fees)

# --- Plot ---
st.subheader("💸 Cumulative Fees from Voting Allocation")
df = pd.DataFrame({
    "Week": weeks_array,
    "Cumulative Voting Fees": vote_cumulative_fees
}).set_index("Week")

st.line_chart(df["Cumulative Voting Fees"])

# Optional display
with st.expander("📋 Show Token Allocation"):
    st.write(f"Total Tokens: `{my_tokens}`")
    st.write(f"- Voting: `{vote_tokens}`")
    st.write(f"- Multiplier Staking: `{multi_tokens}`")
    st.write(f"- Hatching: `{hatch_tokens}`")
    st.write(f"✅ Total Allocated: `{allocated_total}`")
