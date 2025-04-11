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
    my_tokens = st.number_input("Your Token Holdings", value=10_000, format="%d")

    st.subheader("🧮 Token Allocation (%)")
    vote_alloc = st.slider("Voting Allocation", 0, 100, 40)
    multi_alloc = st.slider("Multiplier Staking Allocation", 0, 100, 30)
    hatch_alloc = st.slider("Hatching Allocation", 0, 100, 30)

# --- Normalize Allocation ---
total_alloc = vote_alloc + multi_alloc + hatch_alloc
if total_alloc == 0:
    st.warning("⚠️ Please allocate at least one category.")
    st.stop()

vote_frac = vote_alloc / total_alloc
multi_frac = multi_alloc / total_alloc
hatch_frac = hatch_alloc / total_alloc

vote_tokens = my_tokens * vote_frac
multi_tokens = my_tokens * multi_frac
hatch_tokens = my_tokens * hatch_frac

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
