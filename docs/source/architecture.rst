System Architecture & Cryptography
==================================

Overview
--------
This system demonstrates a **Secure Electronic Voting** protocol protecting two conflicting requirements:
1. **Authentication:** Only eligible voters can vote, and only once.
2. **Anonymity:** No one (including the admin) can link a vote to a voter.

This is achieved using **Chaum's Blind Signatures** and a public **Blockchain**.

Core Components
---------------

1. The Registrar (Authority)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* **Role:** Manages keys and eligibility.
* **Tracking:** Uses ``data/voters_status.json`` to map ``Hash(User_Public_Key)`` to a boolean status.
* **Constraint:** Enforces "One Person, One Vote" at the signing phase.

2. The Ballot Box (Blockchain)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* **Role:** An append-only ledger stored in ``data/blockchain.json``.
* **Content:** Stores the *Unblinded* signed votes.
* **Anonymity:** The blockchain contains no user IDs, only the Authority's signature verifying the vote's legitimacy.

The Cryptographic Protocol (Blind Signatures)
---------------------------------------------

The system implements a workflow based on RSA Blind Signatures.

**Mathematical Theory (Chaum):**

Let the Authority have keys: Public $(e, n)$, Private $d$.
Let $m$ be the vote, and $r$ be a random secret factor chosen by the voter.

1.  **Blinding (User):**
    The user creates a "blinded" message $m'$:
    
    .. math:: m' = m \cdot r^e \pmod n

2.  **Blind Signing (Authority):**
    The Authority signs $m'$, verifying eligibility but not seeing $m$:
    
    .. math:: s' = (m')^d \pmod n

3.  **Unblinding (User):**
    The user removes the random factor $r$ to get the valid signature $s$:
    
    .. math:: s = s' \cdot r^{-1} \pmod n

    Result:

    .. math:: s = m^d \pmod n

    This is a valid signature on the original vote, m.

**Implementation Note:**
In this educational Python demo (`core/crypto_logic.py`), the complex modular arithmetic of steps 1 & 3 is simulated using hashing to visualize the *workflow* without the heavy computational overhead of raw RSA math implementation.

Verification Process
--------------------
Once a vote is on the blockchain:
1. The **Signature** proves it was approved by the Authority.
2. The **Receipt Code** (Hash of signature) allows the user to verify inclusion without revealing their identity.