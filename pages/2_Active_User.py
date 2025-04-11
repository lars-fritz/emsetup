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

    my_tokens = st.number_input("Your Total Token Holdings", value=10_000, format="%d")
    
    # Allow users to specify how to split their tokens
    voting_percent = st.slider("Voting Token Allocation (%)", min_value=0, max_value=100, value=40)
    multiplying_percent = st.slider("Multiplying Token Allocation (%)", min_value=0, max_value=100, value=40)
    hatching_percent = st.slider("Hatching Token Allocation (%)", min_value=0, max_value=100, value=20)

    # Ensure the total percentage does not exceed 100%
    if voting_percent + multiplying_percent + hatching_percent != 100:
        st.warning("The total percentage of tokens must equal 100%. Adjust the sliders accordingly.")

    st.markdown(f"**Current Total Token Value:** ${my_tokens * initial_price:,.2f}")

    # Calculate the split token amounts
    voting_tokens = (voting_percent / 100) * my_tokens
    multiplying_tokens = (multiplying_percent / 100) * my_tokens
    hatching_tokens = (hatching_percent / 100) * my_tokens

    st.markdown(f"**Voting Tokens:** {voting_tokens}")
    st.markdown(f"**Multiplying Tokens:** {multiplying_tokens}")
    st.markdown(f"**Hatching Tokens:** {hatching_tokens}")

    # --- Asset receiving emission ---
    asset_percent = st.slider("Percentage of Emission Allocated to Asset (%)", min_value=0, max_value=100, value=10)
    total_asset_volume = 100_000_000  # $100 million

# --- Simulate emissions and supply ---
weeks_array = np.arange(weeks)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)
circulating_supply = initial_xtokens + cumulative_emissions

# --- Multiplier Logic ---
max_multiplier = 20
growth_rate = 0.07  # Adjust this to tweak how fast multiplier grows
multiplier_array = 1 + (max_multiplier - 1) * (1 - np.exp(-growth_rate * weeks_array))

# --- Fee Calculation for Voting Tokens ---
voting_share = voting_tokens / circulating_supply
voting_weekly_fees = voting_share * weekly_fees

# --- Fee Calculation for Multiplying Tokens ---
adjusted_multiplying_tokens = multiplying_tokens * multiplier_array
multiplying_share = adjusted_multiplying_tokens / circulating_supply
multiplying_weekly_fees = multiplying_share * weekly_fees

# --- Fee Calculation for Hatching Tokens ---
hatching_weekly_fees = np.zeros(weeks)  # Temporary zero values for hatching tokens

# --- Asset Receiving Emission ---
asset_weekly_emission = (asset_percent / 100) * weekly_emissions
asset_value_in_dollars = asset_weekly_emission * initial_price  # Convert to dollar value based on token price

# --- Combine Fee Calculations ---
total_weekly_fees = voting_weekly_fees + multiplying_weekly_fees + hatching_weekly_fees
total_cumulative_fees = np.cumsum(total_weekly_fees)

# --- Asset Volume Calculation ---
asset_cumulative_value = np.cumsum(asset_value_in_dollars)

# --- Result Outputs ---
df = pd.DataFrame({
    "Week": weeks_array,
    "Voting Weekly Fees": voting_weekly_fees,
    "Multiplying Weekly Fees": multiplying_weekly_fees,
    "Hatching Weekly Fees": hatching_weekly_fees,
    "Asset Emission Value ($)": asset_value_in_dollars,
    "Total Weekly Fees": total_weekly_fees,
    "Cumulative Fees ($)": total_cumulative_fees,
    "Asset Cumulative Value ($)": asset_cumulative_value
}).set_index("Week")

# --- Plots ---
st.subheader("📊 Fee Earnings Over Time")
st.line_chart(df[["Voting Weekly Fees", "Multiplying Weekly Fees", "Hatching Weekly Fees", "Total Weekly Fees"]])

st.subheader("💸 Asset Value Allocated Over Time")
st.line_chart(df["Asset Emission Value ($)"])

st.subheader("💰 Cumulative Fees and Asset Value Over Time")
st.line_chart(df[["Cumulative Fees ($)", "Asset Cumulative Value ($)"]])

# --- Data Table ---
with st.expander("📋 Show Simulation Data"):
    st.dataframe(df.style.format({
        "Voting Weekly Fees": "%.2f",
        "Multiplying Weekly Fees": "%.2f",
        "Hatching Weekly Fees": "%.2f",
        "Asset Emission Value ($)": "%.2f",
        "Total Weekly Fees": "%.2f",
        "Cumulative Fees ($)": "%.2f",
        "Asset Cumulative Value ($)": "%.2f"
    }))
