# app.py
import streamlit as st
from tokenomics import Tokenomics

st.set_page_config(page_title="XToken Egg Simulation", layout="wide")

st.title("🥚 XToken & Egg Simulation")

if "sim" not in st.session_state:
    st.session_state.sim = Tokenomics()

sim = st.session_state.sim

# Sidebar controls
st.sidebar.header("🔧 Settings")
if st.sidebar.button("Advance 1 Week"):  # Move time forward
    sim.advance_week()

with st.sidebar.expander("📈 Set Initial Parameters", expanded=False):
    init_token = st.number_input("Initial Token Supply", value=1000.0)
    init_xtoken = st.number_input("Initial XToken Supply", value=0.0)
    egg_emission = st.number_input("Initial Egg Emission Per Week", value=10.0)
    decay_rate = st.number_input("Egg Emission Decay (% per week)", value=10.0)
    if st.button("Start Simulation"):
        sim.reset(init_token, init_xtoken, egg_emission, decay_rate)

st.markdown(f"### Week {sim.week} | Emission: {sim.current_egg_emission:.2f} eggs")

# Display balances
st.subheader("📊 Balances")
st.write(sim.get_balances())

# Lock tokens into xtokens
st.subheader("🔒 Lock Tokens into XTokens")
lock_amt = st.number_input("Amount to Lock", min_value=0.0, value=0.0, step=1.0)
if st.button("Lock"):
    sim.lock_tokens(lock_amt)

# Speed exit
st.subheader("⚡ Speed Exit")
speed_exit_amt = st.number_input("XTokens to Speed Exit", min_value=0.0, value=0.0, step=1.0)
if st.button("Speed Exit"):
    sim.speed_exit(speed_exit_amt)

# Eggs Section
st.subheader("🥚 Eggs Inventory")
for egg in sim.eggs:
    st.write(egg)

# Hatching
st.subheader("🐣 Hatch Eggs")
available_eggs = [e for e in sim.eggs if not e['hatched'] and not e['rotted']]
selected_egg = st.selectbox("Choose Egg to Hatch", available_eggs, format_func=lambda e: f"{e['color']} Egg (Week {e['born']})")
with st.expander("Stake to Hatch"):
    use_xtoken = st.checkbox("Use XToken (1 required)", value=True)
    if st.button("Stake to Hatch Egg"):
        sim.stake_to_hatch(selected_egg, use_xtoken)

# Show Hatcher status
st.subheader("🧪 Hatcher")
for stake in sim.hatcher:
    st.write(stake)

# Governance, Multiplier, and other xtoken use cases will go here.

st.caption("Built with ❤️ using Streamlit")
