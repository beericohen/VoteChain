import streamlit as st
import os
from core.crypto_logic import CryptoManager
from core.blockchain import BlockchainManager

st.title("🔧 Election Setup (Admin)")

if "bm" not in st.session_state:
    st.session_state.bm = BlockchainManager()

st.header("1. Government Keys")
if st.button("Generate Government Keys"):
    priv, pub = CryptoManager.generate_keys()
    st.session_state.bm.save_key("gov", priv, is_private=True)
    st.session_state.bm.save_key("gov", pub, is_private=False)
    st.success("✅ Government keys generated and saved!")

st.divider()

st.header("2. Voter Registration")
num_voters = st.number_input("Number of voters to generate", min_value=1, value=5)
if st.button("Create Voter Keys"):
    for i in range(1, num_voters + 1):
        priv, pub = CryptoManager.generate_keys(1024) # Smaller keys for speed
        st.session_state.bm.save_key(f"voter_{i}", pub, is_private=False)
        # In reality, private key goes to voter. Here we save locally for demo convenience.
        st.session_state.bm.save_key(f"voter_{i}", priv, is_private=True)
    st.success(f"✅ Created keys for {num_voters} voters in /data/keys")

st.divider()

st.header("3. Initialize Election")
if st.button("Reset & Initialize Blockchain"):
    st.session_state.bm.init_chain()
    st.success("🗳️ Election Ready! Blockchain reset to Genesis.")