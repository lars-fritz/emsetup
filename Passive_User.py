import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Passive User", layout="wide")
st.title("🧍 Passive User Fee Earnings")

# User inputs
with st.sidebar:
    st.header("Passive User Settings")
    my_tokens = st.number_input("Your Token Holdings (Voting)", value=10_000, format="%d")
    initial_price = st.number_input("Initial Token Price ($)", value=0.25, step=0.01, format="%.2f")
    st.markdown(f"**Current Value:** ${my_tokens * initial_price:,.2f}")

# --- Shared assumptions (from Home.py) ---
initial_xtokens = 16_000_000
locked_tokens = 84_000_000
weekly_fees = 20_000
base_emission = 800_000
decay_percent = 2.0
decay_rate = 1 - (decay_percent / 100)
weeks = 104

# --- Simulate emissions and supply ---
weeks_array = np.arange(weeks)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)
circulating_supply = initial_xtokens + cumulative_emissions

# --- Passive user: Fixed holding ---
user_share = my_tokens / circulating_supply
user_weekly_fees = user_share * weekly_fees
user_cumulative_fees = np.cumsum(user_weekly_fees)
relative_pct = (user_cumulative_fees / (my_tokens * initial_price)) * 100

# --- Self-compounding version (lsToken) ---
my_ls_tokens = my_tokens
ls_token_holdings = []
ls_fees = []

for i in range(weeks):
    supply = circulating_supply[i]
    share = my_ls_tokens / supply
    weekly_fee = share * weekly_fees
    my_ls_tokens += weekly_fee / initial_price  # reinvest fees at fixed price
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
st.subheader("📊 Fee Earnings Over Time")
st.line_chart(df[["Your Weekly Fees", "Cumulative Fees"]])

st.subheader("💸 Relative Cumulative Earnings (%)")
st.line_chart(df["Relative Earnings (%)"])

st.subheader("🔁 Self-Compounding Earnings with lsToken")
st.line_chart(df[["lsToken Weekly Fees", "lsToken Cumulative Fees"]])

st.subheader("📈 Relative Earnings (%) – Passive vs lsToken")
st.line_chart(df[["Relative Earnings (%)", "lsToken Relative Earnings (%)"]])

st.subheader("📥 lsToken Holdings Over Time (Auto-compounding)")
st.line_chart(df["lsToken Holdings"])

# --- Optional: Show raw data ---
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
