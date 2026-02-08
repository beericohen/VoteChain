Code Documentation
==================

The project is divided into two main components:

1. **User Interface (`app.py`):** Handles the Streamlit frontend, file uploads, and session state management.
2. **Logic (`logic.py`):** Contains the core cryptographic functions (RSA key generation, signing, and verification).

Cryptographic Logic
-------------------

The ``logic`` module handles all security operations using the **PyCryptodome** library.
It utilizes **RSA-2048** for key pairs and **SHA-256** for hashing document content before signing.

.. automodule:: logic
   :members:
   :undoc-members:
   :show-inheritance:

Streamlit Interface
-------------------

The interface is built using Streamlit widgets. Key features include:

* **Session State:** Stores the private and public keys temporarily so they persist between re-runs of the script (e.g., when clicking buttons).
* **Tabs:** Separates the "Sign" and "Verify" workflows for better UX.
* **File Uploader:** Allows processing of PDF, DOCX, and TXT files as binary streams.