import streamlit as st

st.set_page_config(
    page_title="Secure Vote Demo",
    page_icon="🗳️",
    layout="centered"
)

st.title("🗳️ Secure Voting System")

st.markdown("""
### Welcome to the Future of Democracy

This system demonstrates how **Blind Signatures** and **Blockchain** technology can solve the voting paradox:
* **Authentication:** We know *who* you are.
* **Anonymity:** We don't know *what* you voted.

#### 👈 Select a page from the sidebar to begin.
""")

st.info("Ensure you have run the 'Setup' page first to initialize keys!")