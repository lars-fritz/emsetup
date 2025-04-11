import streamlit as st
import pandas as pd
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Active User – Voting Emissions", layout="wide")
st.title("🗳️ Voting Tokens vs Weekly Fees")

# --- Shared Tokenomics from Main Page ---
try:
    initial_xtokens = st.session_state.initial_xtokens
    locked_tokens = st.session_state.locked_tokens
    initial_price = st.session_state.initial_price
    base_emission = st.session_state.base_emission
    decay_percent = st.session_state.decay_percent
    weeks = st.session_state.weeks
except AttributeError:
    st.error("⚠️ Please visit the main page first to set the tokenomics parameters.")
    st.stop()

decay_rate = 1 - (decay_percent / 100)

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("User Setup")

    my_total_tokens = st.number_input("Your Total Token Holdings", value=10_000, format="%d")
    voting_tokens = st.number_input("Tokens Allocated to Voting", value=5_000, max_value=my_total_tokens, format="%d")

    st.markdown("### Emission Asset Settings")
    emission_pct = st.slider("Asset Emission Share (%)", min_value=0, max_value=100, value=10)
    asset_volume = st.number_input("Total Asset Volume ($)", value=100_000_000, step=1_000_000, format="%d")

# --- Emission & Supply Simulation ---
weeks_array = np.arange(weeks)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)
circulating_supply = initial_xtokens + cumulative_emissions

# --- Asset Fee Emissions ---
asset_emission = (emission_pct / 100) * weekly_emissions

# --- User Share of Fees Based on Trade Volume Ownership ---
user_share_of_volume = my_total_tokens / asset_volume
voting_weekly_fees = user_share_of_volume * asset_emission

# --- Voting Token Share of Circulating Supply ---
voting_share_pct = (voting_tokens / circulating_supply) * 100

# --- DataFrame for Plotting ---
df = pd.DataFrame({
    "Week": weeks_array,
    "Voting Token Share (%)": voting_share_pct,
    "Voting Weekly Fees ($)": voting_weekly_fees
}).set_index("Week")

# --- Plot ---
st.subheader("🗳️ Voting Token Share vs Weekly Fees Earned")
st.line_chart(df[["Voting Token Share (%)", "Voting Weekly Fees ($)"]])
