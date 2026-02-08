import streamlit as st
from logic import generate_file_signature, verify_signature, generate_keys

st.set_page_config(page_title="VoteChain | RSA Secure Signing")
st.title("VoteChain")
st.subheader("RSA Digital Signatures with PyCryptodome")

# Helper to manage keys in session state for the demo
if 'private_key' not in st.session_state:
    priv, pub = generate_keys()
    st.session_state.private_key = priv
    st.session_state.public_key = pub

tab_sign, tab_verify = st.tabs(["Sign Document", "Verify Authenticity"])

with tab_sign:
    st.header("Generate RSA Signature")
    file_to_sign = st.file_uploader("Upload document to sign", type=["pdf", "docx", "txt"])
    
    if st.button("Sign with Private Key"):
        if file_to_sign:
            with st.spinner("Signing..."):
                signature = generate_file_signature(file_to_sign, st.session_state.private_key)
                st.success("Document signed with RSA-2048!")
                
                st.download_button(
                    label="Download .sig file",
                    data=signature,
                    file_name=f"{file_to_sign.name}.sig",
                    mime="application/octet-stream"
                )
        else:
            st.error("Please upload a document.")

with tab_verify:
    st.header("Verify RSA Signature")
    col1, col2 = st.columns(2)
    with col1:
        doc = st.file_uploader("Upload original document", key="verify_doc")
    with col2:
        sig = st.file_uploader("Upload .sig file", key="verify_sig")

    if st.button("Verify Identity"):
        if doc and sig:
            # signature_file.read() returns bytes, which is what PyCryptodome needs
            is_valid = verify_signature(doc, sig.read(), st.session_state.public_key)
            
            if is_valid:
                st.success("✅ RSA Verification Successful! The sender's identity and document integrity are confirmed.")
            else:
                st.error("❌ RSA Verification Failed! The document is altered or the signature is invalid.")