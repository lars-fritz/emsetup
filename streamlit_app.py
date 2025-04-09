import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("📈 Token Emission Schedule Simulator")

# --- Inputs ---
initial_tokens = st.number_input("Initial Token Supply", value=16000000)
initial_price = st.number_input("Initial Token Price ($)", value=0.45, step=0.01)
weekly_fees = st.number_input("Weekly Fee Revenue ($)", value=20000)
base_emission = st.number_input("Initial Weekly Emission", value=300000)
decay_rate = st.number_input("Decay Rate per Week (e.g., 0.98)", value=0.98)
weeks = st.slider("Number of Weeks to Simulate", min_value=10, max_value=520, value=104)

# --- Simulation ---
weeks_list = np.arange(weeks)
emissions = base_emission * decay_rate ** weeks_list
cumulative_tokens = initial_tokens + np.cumsum(emissions)
valuations = cumulative_tokens * initial_price
cumulative_fees = np.cumsum([weekly_fees] * weeks)

# --- DataFrame ---
df = pd.DataFrame({
    "Week": weeks_list,
    "Weekly Emission": emissions,
    "Total Supply": cumulative_tokens,
    "Valuation ($)": valuations,
    "Cumulative Fees ($)": cumulative_fees
})

# --- Charts ---
st.subheader("📊 Token Supply Over Time")
st.line_chart(df.set_index("Week")[["Total Supply"]])

st.subheader("💰 Valuation Over Time")
st.line_chart(df.set_index("Week")[["Valuation ($)"]])

st.subheader("🪙 Weekly Emissions")
st.bar_chart(df.set_index("Week")[["Weekly Emission"]])

st.subheader("📦 Cumulative Fees Collected")
st.line_chart(df.set_index("Week")[["Cumulative Fees ($)"]])

# --- Optional Table ---
with st.expander("See Raw Data"):
    st.dataframe(df)
