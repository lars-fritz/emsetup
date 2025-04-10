import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Token Emission Simulator", layout="wide")
st.title("📊 Token Emission Simulator")

# Tabs for passive vs. active user
tab1, tab2 = st.tabs(["🧍 Passive User", "🚀 Active User"])

# Common Inputs
with st.sidebar:
    st.header("🔧 Simulation Settings")

    initial_xtokens = st.number_input("Initial xTokens (Voting)", value=16_000_000, step=100_000, format="%d")
    locked_tokens = st.number_input("Locked Tokens (Non-Voting)", value=84_000_000, step=1_000_000, format="%d")
    initial_price = st.number_input("Initial Token Price ($)", value=0.25, step=0.01, format="%.2f")
    weekly_fees = st.number_input("Weekly Fee Revenue ($)", value=20_000, step=1_000, format="%d")
    base_emission = st.number_input("Initial Weekly Emission", value=800_000, step=10_000, format="%d")
    decay_percent = st.number_input("Emission Decay per Week (%)", value=2.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
    decay_rate = 1 - (decay_percent / 100)
    weeks = st.slider("Number of Weeks to Simulate", min_value=10, max_value=520, value=104)
    my_tokens = st.number_input("Your Token Holdings (Voting xTokens)", value=10_000, format="%d")

    my_token_value_usd = my_tokens * initial_price
    st.markdown(f"**Your Token Value:** ${my_token_value_usd:,.2f}")

# Core simulation function
def run_simulation(user_type="passive", bonus_multiplier=1.0):
    weeks_array = np.arange(weeks)
    weekly_emissions = base_emission * (decay_rate ** weeks_array)
    cumulative_emissions = np.cumsum(weekly_emissions)

    circulating_supply = initial_xtokens + cumulative_emissions
    total_supply_fdv = locked_tokens + initial_xtokens + cumulative_emissions

    valuation = circulating_supply * initial_price
    fdv = total_supply_fdv * initial_price

    user_share_ratio = my_tokens / circulating_supply
    user_weekly_fees = user_share_ratio * weekly_fees

    if user_type == "active":
        # Simulate bonus (e.g. boosted bribes, rewards, multiplier)
        user_weekly_fees *= bonus_multiplier

    user_cumulative_fees = np.cumsum(user_weekly_fees)
    cumulative_protocol_fees = np.cumsum(np.full(weeks, weekly_fees))
    initial_investment = my_tokens * initial_price
    relative_earnings_pct = (user_cumulative_fees / initial_investment) * 100

    df = pd.DataFrame({
        "Week": weeks_array,
        "Weekly Emission": weekly_emissions,
        "Circulating Voting Supply": circulating_supply,
        "Total Supply (FDV)": total_supply_fdv,
        "Valuation ($)": valuation,
        "FDV ($)": fdv,
        "Your Weekly Fee Earnings ($)": user_weekly_fees,
        "Your Cumulative Fees ($)": user_cumulative_fees,
        "Cumulative Protocol Fees ($)": cumulative_protocol_fees,
        "Relative Cumulative Earnings (%)": relative_earnings_pct
    }).set_index("Week")

    return df

# Passive User Tab
with tab1:
    st.subheader("🧍 Passive User Simulation")
    df_passive = run_simulation(user_type="passive")
    st.line_chart(df_passive["Relative Cumulative Earnings (%)"])
    st.line_chart(df_passive["FDV ($)"])

# Active User Tab
with tab2:
    st.subheader("🚀 Active User Simulation")

    active_bonus = st.slider("Reward Multiplier for Active Participation", 1.0, 3.0, 1.5, step=0.1)
    df_active = run_simulation(user_type="active", bonus_multiplier=active_bonus)

    st.line_chart(df_active["Relative Cumulative Earnings (%)"])
    st.line_chart(df_active["FDV ($)"])

# Optional Table
with st.expander("📋 Show Data Table (Passive User)"):
    st.dataframe(df_passive.style.format({
        "Your Weekly Fee Earnings ($)": "%.2f",
        "Your Cumulative Fees ($)": "%.2f",
        "Relative Cumulative Earnings (%)": "%.2f",
        "FDV ($)": "%.2f"
    }))

