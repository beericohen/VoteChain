import sys
import os
# התיקון לנתיבים כדי שזה יעבוד חלק
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
import time
from Crypto.PublicKey import RSA
from core.crypto_logic import CryptoManager, BlindSignatureDemo
from core.blockchain import BlockchainManager

st.title("🗳️ Cast Your Vote")

if "bm" not in st.session_state:
    st.session_state.bm = BlockchainManager()

# --- Step 1: Authentication ---
st.subheader("1. Authenticate")
uploaded_file = st.file_uploader("Upload your Private Key (PEM)", type=['pem'])

if uploaded_file:
    private_key_bytes = uploaded_file.getvalue()
    
    # חילוץ המפתח הציבורי מתוך המפתח הפרטי כדי לבדוק זהות
    try:
        key_obj = RSA.import_key(private_key_bytes)
        public_key_pem = key_obj.publickey().export_key().decode('utf-8')
    except Exception as e:
        st.error(f"Invalid Key File: {e}")
        st.stop()

    # --- SECURITY CHECK: PREVENT DOUBLE VOTING ---
    if st.session_state.bm.has_voted(public_key_pem):
        st.error("⛔ Access Denied: You have already voted!")
        st.warning("One person, one vote. Please verify your receipt in the Verification page.")
        st.stop() # עוצר את הריצה כאן

    st.success("🔑 Key verified! You are eligible to vote.")
    
    # --- Step 2: Selection ---
    st.divider()
    st.subheader("2. Select Candidate")
    
    candidates = ["Alice", "Bob", "Charlie"]
    cols = st.columns(len(candidates))
    
    if "selected_candidate" not in st.session_state:
        st.session_state.selected_candidate = None

    for idx, name in enumerate(candidates):
        if cols[idx].button(f"Vote for {name}", use_container_width=True):
            st.session_state.selected_candidate = name

    if st.session_state.selected_candidate:
        st.info(f"You selected: **{st.session_state.selected_candidate}**")
        
        if st.button("Confirm & Cast Vote", type="primary"):
            
            # --- Step 3: Crypto Theater ---
            with st.status("🔐 Securing your vote...", expanded=True) as status:
                
                # 1. Blind
                st.write("🔒 Blinding your vote (hiding choice)...")
                blinded_vote = BlindSignatureDemo.blind(st.session_state.selected_candidate)
                time.sleep(1.0)
                
                # 2. Sign
                st.write("✍️ Government signing eligibility...")
                try:
                    with open("data/keys/gov_priv.pem", "rb") as f:
                        gov_priv = f.read()
                    signature = BlindSignatureDemo.sign_blinded(gov_priv, blinded_vote)
                    time.sleep(1.0)
                except FileNotFoundError:
                    st.error("Government keys missing! Run Setup first.")
                    st.stop()
                
                # 3. Unblind
                st.write("🔓 Unblinding signature...")
                final_sig = BlindSignatureDemo.unblind(signature)
                time.sleep(0.5)
                
                status.update(label="✅ Vote Secured & Signed!", state="complete")
            
            # --- Step 4: Submit to Chain ---
            receipt_code = CryptoManager.get_hash(final_sig)[:12]
            
            vote_package = {
                "candidate": st.session_state.selected_candidate,
                "signature": final_sig,
                "receipt": receipt_code
            }
            
            st.session_state.bm.add_vote(vote_package)
            
            # --- Mark user as voted ---
            st.session_state.bm.mark_as_voted(public_key_pem)
            
            # --- Step 5: Success & Receipt Download ---
            st.divider()
            st.balloons()
            st.success("🎉 Vote successfully cast!")
            
            # יצירת תוכן הקבלה
            receipt_text = f"""
OFFICIAL VOTING RECEIPT
-----------------------
Date: {time.ctime()}
Candidate: {st.session_state.selected_candidate}
Receipt Code: {receipt_code}

Digital Signature:
{final_sig}

Keep this file safe! You can use the Receipt Code to verify your vote on the blockchain.
            """
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.warning(f"🧾 Code: `{receipt_code}`")
            with col2:
                # כפתור הורדה
                st.download_button(
                    label="📥 Download Receipt",
                    data=receipt_text,
                    file_name=f"vote_receipt_{receipt_code}.txt",
                    mime="text/plain"
                )
            
            # מנקה את הבחירה כדי שלא ילחצו שוב בטעות (למרות שההגנה קיימת)
            del st.session_state.selected_candidate