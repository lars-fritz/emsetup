import streamlit as st
import pandas as pd

st.set_page_config(page_title="User Manual", layout="wide")
st.title("📘 User Manual: Emission & Tokenomics Simulator")

st.markdown("""
This user manual explains how to use the Emission & Tokenomics Simulator effectively, understand each parameter, 
and interpret the simulation results across all pages of the application.
""")

# Table of Contents with jump links
st.markdown("""
## 📋 Table of Contents
1. [Introduction](#introduction)
2. [Main Page: Emission Simulator](#main-page-emission-simulator)
3. [Passive User Simulator](#passive-user-simulator)
4. [Active User Simulator](#active-user-simulator)
5. [Example Use Cases](#example-use-cases)
6. [FAQs](#faqs)
7. [Glossary](#glossary)
""")

# Introduction
st.header("Introduction", anchor="introduction")
st.markdown("""
The Emission & Tokenomics Simulator is a powerful tool designed to help you visualize and understand:

- How token emissions affect circulating supply over time
- How protocol fees get distributed to token holders
- The difference between passive and active token holding strategies
- The impact of different tokenomic parameters on valuation and user earnings

This simulator models a token ecosystem with distinct token types:
- **Voting tokens (xTokens)**: Participate in fee distribution and governance
- **Locked tokens**: Count towards total supply but not towards voting power
- **Weekly emissions**: New tokens released into circulation each week, decreasing over time

The simulator consists of three interconnected pages:
1. **Main Page**: Configure core tokenomics parameters and view supply/valuation projections
2. **Passive User**: Compare passive holding vs. self-compounding strategies
3. **Active User**: Explore advanced strategies with voting and multiplier staking
""")

# Main Page
st.header("Main Page: Emission Simulator", anchor="main-page-emission-simulator")
st.markdown("""
### Parameter Settings

The main page allows you to adjust key tokenomic parameters:

| Parameter | Description |
|-----------|-------------|
| **Initial xTokens** | Starting amount of voting tokens in circulation |
| **Locked Tokens** | Tokens reserved for team, treasury, or future distribution (non-voting) |
| **Initial Token Price** | Starting price of the token in USD |
| **Weekly Fee Revenue** | Protocol fee revenue generated each week in USD |
| **Initial Weekly Emission** | Number of new tokens released in the first week |
| **Emission Decay per Week** | Percentage by which emissions decrease each week |
| **Number of Weeks** | Time horizon for the simulation |

### Understanding the Charts

The main page provides several charts to visualize the tokenomic model:

1. **Weekly Token Emissions**: Shows how many new tokens enter circulation each week, gradually decreasing based on the decay rate.

2. **Emissions & Supply Over Time**: Displays two key metrics:
   - **Circulating Voting Supply**: Total tokens available for voting (xTokens)
   - **Total Supply (FDV)**: All tokens, including locked ones

3. **Valuation Over Time**: Estimates market cap based on:
   - **Valuation**: Price × circulating supply
   - **FDV (Fully Diluted Valuation)**: Price × total supply

4. **Cumulative Protocol Fees**: Shows total revenue collected over time

### Tips for Main Page
- Start with realistic parameters based on comparable projects
- Experiment with different decay rates to find optimal emission schedules
- Use the expanded data table to examine specific weeks in detail
""")

# Passive User Page
st.header("Passive User Simulator", anchor="passive-user-simulator")
st.markdown("""
### Overview

The Passive User page models two holding strategies for tokens:
1. **Self-voting**: Simply holding tokens and receiving proportional fees
2. **Self-compounding (lsTokens)**: Automatically reinvesting earned fees

### Parameter Settings

| Parameter | Description |
|-----------|-------------|
| **Your Token Holdings** | Number of tokens you own and use for voting |

### Understanding the Charts

1. **Relative Cumulative Earnings (%)**: Shows your ROI as a percentage of initial investment
2. **Fee Earnings Over Time**: Displays weekly and cumulative fee earnings
3. **Self-Compounding Earnings**: Shows how reinvesting fees increases holdings over time
4. **Relative Earnings Comparison**: Compares ROI between self-voting and self-compounding
5. **lsToken Holdings Over Time**: Visualizes growth of tokens through compounding

### Key Insights from Passive User Page
- Self-compounding typically outperforms simple holding over longer timeframes
- As circulating supply increases due to emissions, individual fee share decreases
- The compounding effect becomes more significant with longer time horizons
""")

# Active User Page  
st.header("Active User Simulator", anchor="active-user-simulator")
st.markdown("""
### Overview

The Active User page models more complex token usage strategies:
1. **Voting**: Direct fee earning through governance participation  
2. **Multiplier Staking**: Boosting volume-based rewards
3. **Hatching**: Reserved tokens (not actively modeled in this simulator)

### Parameter Settings

**Sidebar Settings:**
| Parameter | Description |
|-----------|-------------|
| **Your Token Holdings** | Total number of tokens you own |
| **Tokens for Voting** | Amount dedicated to fee earning |
| **Tokens for Multiplier** | Amount staked to boost volume rewards |
| **Tokens for Hatching** | Remaining tokens (calculated automatically) |

**Volume Emission Settings:**
| Parameter | Description |
|-----------|-------------|
| **Asset Weight** | Percentage of emissions allocated to volume-based rewards |
| **Total Volume on Asset** | Trading volume across all users |
| **Your Weekly Volume** | Your personal trading activity |

### Understanding the Charts

1. **Cumulative Voting Fees**: Shows fee earnings from your voting allocation
2. **Weekly Volume-Based Rewards**: Compares rewards with/without multiplier
3. **Cumulative Volume-Based Rewards**: Shows total rewards over time
4. **Relative ROI from Voting**: Shows percentage return on investment

### Key Insights from Active User Page
- Strategic token allocation can significantly increase earnings
- The multiplier grows over time, providing increasing returns
- Volume-based earnings can outpace fee earnings depending on your trading activity
- Finding the optimal balance between voting and multiplier staking depends on your trading behavior
""")

# Example Use Cases
st.header("Example Use Cases", anchor="example-use-cases")
st.markdown("""
### 1. New Token Launch Planning
Use the simulator to model different initial supply and emission schedules to find a sustainable balance between:
- Attractive rewards for early adopters
- Long-term supply growth that doesn't excessively dilute token value

### 2. Investor Strategy Optimization
- Compare different token allocation strategies across voting and multiplier staking
- Determine optimal holding period based on emission schedule and fee projections
- Evaluate whether active participation or passive holding fits your investment style

### 3. Protocol Parameter Tuning
- Model how different fee structures affect holder returns
- Test various emission decay rates to find balance between short-term incentives and long-term sustainability
- Assess how changing volume weights affects different user personas

### 4. Fee Distribution Analysis
- Understand how growing circulating supply impacts individual fee share
- Compare the benefits of direct fee distribution versus incentivized volume activities
- Model the impact of fee reinvestment on long-term returns
""")

# FAQs
st.header("FAQs", anchor="faqs")
with st.expander("What is emission decay?"):
    st.markdown("""
    Emission decay is the rate at which new token issuance decreases over time. For example, with a 2% decay rate, 
    each week's emission will be 98% of the previous week's amount. This creates a gradual reduction in new supply, 
    which can help maintain token value while still providing ongoing incentives.
    """)

with st.expander("What's the difference between Valuation and FDV?"):
    st.markdown("""
    - **Valuation (Market Cap)**: Token price × circulating supply. This represents the actual market value of all tokens currently in circulation.
    - **FDV (Fully Diluted Valuation)**: Token price × total supply (including locked tokens). This represents the theoretical value if all tokens were in circulation at the current price.
    
    FDV is always higher than the current market cap when there are locked or unvested tokens.
    """)

with st.expander("What are lsTokens in the passive user simulation?"):
    st.markdown("""
    lsTokens represent a "liquid staking" version of the token where:
    1. Your tokens automatically compound earned fees
    2. The reinvestment happens without manual intervention
    3. Your token balance grows over time

    Many DeFi protocols offer similar liquid staking derivatives that handle reinvestment automatically.
    """)

with st.expander("How does the multiplier work in the Active User page?"):
    st.markdown("""
    The multiplier boosts your effective trading volume, increasing your share of volume-based rewards:
    
    1. Your base multiplier depends on how many tokens you stake relative to a reference amount
    2. The multiplier grows over time (5% per week in this model)
    3. Higher multipliers mean your volume counts more when calculating reward distribution
    
    The formula is: `multiplier = 1 + 3 × (your_stake / (your_stake + reference_stake))`
    
    With maximum staking and time, the multiplier can approach 4x.
    """)

with st.expander("Can I export the simulation data?"):
    st.markdown("""
    Yes, you can view the full data table by expanding the "Show Data Table" section at the bottom of each page. 
    From there, you can copy the data to paste into a spreadsheet application like Excel or Google Sheets for further analysis.
    
    Future versions may include direct CSV export functionality.
    """)

# Glossary
st.header("Glossary", anchor="glossary")
st.markdown("""
| Term | Definition |
|------|------------|
| **xTokens** | Voting tokens that participate in fee distribution |
| **Emission** | New tokens released into circulation on a schedule |
| **Decay Rate** | Percentage by which emissions decrease each period |
| **Circulating Supply** | Total tokens currently available in the market |
| **FDV** | Fully Diluted Valuation (price × total supply) |
| **Multiplier** | Factor that boosts user volume for reward calculations |
| **Compounding** | Reinvesting returns to generate additional future returns |
| **Fee Share** | Portion of protocol fees distributed to a specific holder |
| **ROI** | Return on Investment (earnings as percentage of initial investment) |
| **Locked Tokens** | Tokens reserved for future use, not yet in circulation |
""")

# Feedback section
st.divider()
st.subheader("📝 Feedback")
st.markdown("""
We're continuously improving this simulator. If you have suggestions or feature requests, 
please let us know via our community channels.
""")

with st.expander("Version History"):
    st.markdown("""
    - **v1.0.0**: Initial release with main, passive, and active user simulations
    - **v1.1.0**: Added user manual and improved visualizations
    """)
