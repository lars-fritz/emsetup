import streamlit as st
import pandas as pd
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Active User – Voting Emissions", layout="wide")
st.title("🗳️ Token Allocation: Voting, Multiplying, Hatching")

# --- Shared Tokenomics from Main Page ---
try:
    initial_xtokens = st.session_state.initial_xtokens
    locked_tokens = st.session_state.locked_tokens
    initial_price = st.session_state.initial_price
    base_emission = st.session_state.base_emission
    decay_percent = st.session_state.decay_percent
    weekly_fees = st.session_state.weekly_fees
    weeks = st.session_state.weeks
except AttributeError:
    st.error("⚠️ Please visit the main page first to set the tokenomics parameters.")
    st.stop()

decay_rate = 1 - (decay_percent / 100)

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("User Setup")

    my_total_tokens = st.number_input("🎒 Your Total Token Holdings", value=10_000, format="%d")

    st.markdown("### 📊 Allocation (must sum to 100%)")
    voting_pct = st.slider("Voting Allocation (%)", 0, 100, 40)
    multiplying_pct = st.slider("Multiplier Allocation (%)", 0, 100, 30)
    hatching_pct = 100 - voting_pct - multiplying_pct

    if voting_pct + multiplying_pct > 100:
        st.error("⚠️ Total allocation exceeds 100%. Adjust sliders.")
        st.stop()

    st.markdown(f"- 🗳️ Voting: `{voting_pct}%` → {my_total_tokens * voting_pct / 100:.0f} tokens")
    st.markdown(f"- 🚀 Multiplying: `{multiplying_pct}%` → {my_total_tokens * multiplying_pct / 100:.0f} tokens")
    st.markdown(f"- 🐣 Hatching: `{hatching_pct}%` → {my_total_tokens * hatching_pct / 100:.0f} tokens")

# --- Emission & Supply Simulation ---
weeks_array = np.arange(weeks)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)
circulating_supply = initial_xtokens + cumulative_emissions

# --- Token Allocations ---
voting_tokens = my_total_tokens * voting_pct / 100

# --- Calculate Weekly Fees Based on Dynamic Share of Weekly Fee Pool ($20k) ---
voting_share = voting_tokens / circulating_supply
voting_weekly_fees = voting_share * weekly_fees
voting_cumulative_fees = np.cumsum(voting_weekly_fees)

# --- DataFrame ---
df = pd.DataFrame({
    "Week": weeks_array,
    "Voting Share": voting_share,
    "Weekly Fees": voting_weekly_fees,
    "Cumulative Fees": voting_cumulative_fees
}).set_index("Week")

# --- Plot ---
st.subheader("📈 Cumulative Fees from Voting Over Time")
st.line_chart(df["Cumulative Fees"])

