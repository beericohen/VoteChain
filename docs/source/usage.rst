User Guide & Demo Flow
======================

This guide walks you through the complete election process, from setup to verification.

Step 1: Admin Setup
-------------------
1. Navigate to the **Setup** page (Sidebar > Setup).
2. Click **Generate Government Keys** to initialize the Authority.
3. Click **Create Voter Keys** to generate key files for participants.
   * *Note:* Keys are saved in ``data/keys/``.

Step 2: Casting a Vote
----------------------
1. Navigate to the **Vote** page.
2. **Authenticate:** Upload your ``voter_X_priv.pem`` file.
   * *Security Check:* The system checks if this key has already voted.
3. **Select:** Choose your preferred candidate.
4. **Process:** Click **Confirm & Cast Vote**.
   * Watch the "Crypto Theater" (Blinding -> Signing -> Unblinding).
5. **Receipt:**
   * A success message will appear.
   * **Click "Download Receipt"** to save your proof of voting (``.txt`` file).

Step 3: Verification
--------------------
1. Navigate to the **Verify** page.
2. **Method A: Manual Entry**
   * Copy the code from your receipt and paste it into the text box.
3. **Method B: File Upload (Recommended)**
   * Drag and drop your downloaded receipt file.
   * The system automatically extracts the code.
4. Click **Search Blockchain**.
   * You will see the block details containing your encrypted vote.

Troubleshooting
---------------
* **"Access Denied: You have already voted!"**:
  The system enforces "One Person, One Vote". You cannot reuse a key.
* **"Government keys missing"**:
  You forgot to run Step 1 (Setup).