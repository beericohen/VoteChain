import streamlit as st
import pandas as pd
from core.blockchain import BlockchainManager

st.title("📊 Election Results")

if "bm" not in st.session_state:
    st.session_state.bm = BlockchainManager()

chain = st.session_state.bm.get_chain()

# Tally votes
tally = {}
total_votes = 0

for block in chain:
    if block["index"] == 0: continue # Skip genesis
    
    vote_data = block["vote"]
    # Handle cases where vote might be string or dict (backward compatibility)
    candidate = vote_data.get("candidate") if isinstance(vote_data, dict) else "Unknown"
    
    tally[candidate] = tally.get(candidate, 0) + 1
    total_votes += 1

# Display Metrics
st.metric("Total Votes Cast", total_votes)

st.divider()
st.subheader("Candidate Standings")

# Display columns
cols = st.columns(3)
idx = 0
for candidate, count in tally.items():
    with cols[idx % 3]:
        st.metric(label=candidate, value=count)
    idx += 1

if total_votes == 0:
    st.info("No votes cast yet.")