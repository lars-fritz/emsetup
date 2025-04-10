import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Active User", layout="wide")
st.title("🚀 Active User Fee Earnings")

# Sidebar inputs
with st.sidebar:
    st.header("Active User Settings")
    my_tokens = st.number_input("Your Token Holdings", value=10_000, format="%d")
    initial_price = st.number_input("Initial Token Price ($)", value=0.25, step=0.01, format="%.2f")
    bonus = st.slider("Participation Bonus Multiplier", 1.0, 3.0, 1.5, step=0.1)
    st.markdown(f"**Current Value:** ${my_tokens * initial_price:,.2f}")

# Constants
initial_xtokens = 16_000_000
locked_tokens = 84_000_000
weekly_fees = 20_000
base_emission = 800_000
decay_percent = 2.0
decay_rate = 1 - (decay_percent / 100)
weeks = 104

# Simulation
weeks_array = np.arange(weeks)
weekly_emissions = base_emission * (decay_rate ** weeks_array)
cumulative_emissions = np.cumsum(weekly_emissions)
circulating_supply = initial_xtokens + cumulative_emissions

user_share = my_tokens / circulating_supply
user_weekly_fees = user_share * weekly_fees * bonus
user_cumulative_fees = np.cumsum(user_weekly_fees)
relative_pct = (user_cumulative_fees / (my_tokens * initial_price)) * 100

df = pd.DataFrame({
    "Week": weeks_array,
    "Your Weekly Fees": user_weekly_fees,
    "Cumulative Fees": user_cumulative_fees,
    "Relative Earnings (%)": relative_pct
}).set_index("Week")

# Plot
st.subheader("💸 Relative Cumulative Earnings with Bonus (%)")
st.line_chart(df["Relative Earnings (%)"])

st.subheader("📊 Fee Earnings Over Time")
st.line_chart(df[["Your Weekly Fees", "Cumulative Fees"]])
