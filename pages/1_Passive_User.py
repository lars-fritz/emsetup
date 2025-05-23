import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Passive User", layout="wide")
st.title("🧍 Passive User Fee Earnings")

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

# --- Sidebar inputs ---
with st.sidebar:
    st.header("Passive User Settings")
    my_tokens = st.number_input("Your Token Holdings (Voting)", value=10_000, format="%d")
    st.markdown(f"**Current Value:** ${my_tokens * initial_price:,.2f}")

# --- Emission & Supply Simulation ---
weeks_array = np.arange(weeks)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)
circulating_supply = initial_xtokens + cumulative_emissions

# --- Passive user (fixed holding) ---
user_share = my_tokens / circulating_supply
user_weekly_fees = user_share * weekly_fees
user_cumulative_fees = np.cumsum(user_weekly_fees)
relative_pct = (user_cumulative_fees / (my_tokens * initial_price)) * 100

# --- Self-compounding user (lsToken) ---
my_ls_tokens = my_tokens
ls_token_holdings = []
ls_fees = []

for i in range(weeks):
    supply = circulating_supply[i]
    share = my_ls_tokens / supply
    weekly_fee = share * weekly_fees
    my_ls_tokens += weekly_fee / initial_price  # reinvest all fees
    ls_token_holdings.append(my_ls_tokens)
    ls_fees.append(weekly_fee)

cumulative_ls_fees = np.cumsum(ls_fees)
relative_ls_pct = (cumulative_ls_fees / (my_tokens * initial_price)) * 100

# --- DataFrame ---
df = pd.DataFrame({
    "Week": weeks_array,
    "Your Weekly Fees": user_weekly_fees,
    "Cumulative Fees": user_cumulative_fees,
    "Relative Earnings (%)": relative_pct,
    "lsToken Weekly Fees": ls_fees,
    "lsToken Cumulative Fees": cumulative_ls_fees,
    "lsToken Relative Earnings (%)": relative_ls_pct,
    "lsToken Holdings": ls_token_holdings,
}).set_index("Week")

# --- Plots ---
st.subheader("💸 Relative Cumulative Earnings (%) – Self voting")
st.line_chart(df["Relative Earnings (%)"])

st.subheader("📊 Fee Earnings Over Time – Self voting - weekly fees")
st.line_chart(df["Your Weekly Fees"])
st.subheader("📊 Fee Earnings Over Time – Self voting - cumulative fees")
st.line_chart(df["Cumulative Fees"])

st.subheader("🔁 Self-Compounding Earnings for passive participant with lsTokens - weekly fees")
st.line_chart(df["lsToken Weekly Fees"])
st.subheader("🔁 Self-Compounding Earnings for passive participant with lsTokens - cumulative fees")
st.line_chart(df["lsToken Cumulative Fees"])

st.subheader("📈 Relative Earnings (%) – Self voting vs lsToken")
st.line_chart(df[["Relative Earnings (%)", "lsToken Relative Earnings (%)"]])

st.subheader("📥 lsToken Holdings Over Time")
st.line_chart(df["lsToken Holdings"])

# --- Explanation ---
with st.expander("📘 Explanation of Calculation Logic"):
    st.markdown("""
    This simulation compares two types of passive token holders:

    #### 1. Passive Self-Voter
    - Simply holds tokens and receives weekly fees proportional to their share of circulating supply.
    - Circulating supply increases weekly due to emissions.
    - Your weekly fee = `your tokens / circulating supply * weekly fees`

    #### 2. Self-Compounding lsToken Holder
    - Reinvests (compounds) weekly fees into additional token holdings.
    - Reinvested value increases your share over time, giving higher future earnings.
    - Each week:
        - Earn fees based on current lsToken balance
        - Reinvest those fees to increase lsToken balance
        - `new balance = old balance + (weekly fees / price)`

    #### Relative Earnings
    - Relative earnings show % ROI over initial investment.
    - lsToken holders compound, so their ROI grows faster over time.

    This helps visualize how active fee compounding can outperform passive holding.
    """)

# --- Data Table ---
with st.expander("📋 Show Data Table"):
    st.dataframe(df.style.format({
        "Your Weekly Fees": "%.2f",
        "Cumulative Fees": "%.2f",
        "Relative Earnings (%)": "%.2f",
        "lsToken Weekly Fees": "%.2f",
        "lsToken Cumulative Fees": "%.2f",
        "lsToken Relative Earnings (%)": "%.2f",
        "lsToken Holdings": "%.2f"
    }))

