import sys
import os
# תיקון נתיבים
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
import re  # נדרש כדי לחלץ את הקוד מהטקסט   
from core.blockchain import BlockchainManager

st.title("🔍 Verify Your Vote")

if "bm" not in st.session_state:
    st.session_state.bm = BlockchainManager()

st.subheader("Receipt Lookup")

# --- אזור הקלט (Input Area) ---
col1, col2 = st.columns(2)

with col1:
    manual_input = st.text_input("Enter Receipt Code manually", placeholder="e.g., a7f3...")

with col2:
    uploaded_receipt = st.file_uploader("📂 OR Upload Receipt File", type=['txt'])

# --- לוגיקה לחילוץ הקוד ---
search_code = manual_input  # ברירת מחדל: מה שהמשתמש הקליד

if uploaded_receipt:
    try:
        # קריאת תוכן הקובץ
        content = uploaded_receipt.read().decode("utf-8")
        
        # שימוש ב-Regex כדי למצוא את הקוד אחרי המילים "Receipt Code:"
        # מחפש רצף של אותיות ומספרים (hex)
        match = re.search(r"Receipt Code:\s*([a-fA-F0-9]+)", content)
        
        if match:
            extracted_code = match.group(1)
            st.success(f"📄 File extracted! Searching for: `{extracted_code}`")
            search_code = extracted_code
        else:
            st.error("❌ Invalid receipt format. Could not extract code.")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# --- ביצוע החיפוש ---
if st.button("Search Blockchain", type="primary"):
    if not search_code:
        st.warning("⚠️ Please enter a code or upload a receipt file.")
    else:
        chain = st.session_state.bm.get_chain()
        found = False
        
        # חיפוש בבלוקצ'יין
        for block in chain:
            if block["index"] == 0: continue # Skip genesis
            
            vote_data = block["vote"]
            
            # בדיקה האם הקוד תואם (תומך גם במבנה ישן וגם בחדש)
            current_receipt = None
            if isinstance(vote_data, dict):
                current_receipt = vote_data.get("receipt")
            
            if current_receipt == search_code:
                st.success(f"✅ Vote Verified! Found in **Block #{block['index']}**")
                
                # הצגת פרטי הבלוק בצורה יפה
                with st.expander("📄 View Block Details", expanded=True):
                    st.json(block)
                    st.caption(f"Block Hash: {block['hash']}")
                
                found = True
                break
        
        if not found:
            st.error(f"❌ Receipt `{search_code}` not found in the blockchain.")

st.divider()

st.subheader("⛓️ Blockchain Explorer")
st.write("Inspect the full immutable ledger:")

# הצגת השרשרת (מהסוף להתחלה - החדש ביותר למעלה)
chain = st.session_state.bm.get_chain()
if len(chain) > 1:
    for block in reversed(chain):
        # לא מציגים את ה-Genesis Block בצורה בולטת
        if block["index"] == 0: continue
        
        short_hash = block['hash'][:10]
        # ננסה לחלץ את הקוד להצגה בכותרת
        rec_disp = block['vote'].get('receipt', 'N/A') if isinstance(block['vote'], dict) else 'N/A'
        
        with st.expander(f"Block #{block['index']} | Receipt: {rec_disp} | Hash: {short_hash}..."):
            st.json(block)
else:
    st.info("No votes cast yet (Only Genesis Block exists).")