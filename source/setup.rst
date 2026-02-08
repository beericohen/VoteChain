Installation and Setup
======================

Follow these steps to set up the development environment and run the **VoteChain** application.

Prerequisites
-------------
* Python 3.8 or higher
* Git

1. Create a Virtual Environment
-------------------------------

First, clone the repository and navigate into the project folder. Then, create a virtual environment to isolate dependencies.

**For Windows:**

.. code-block:: console

    python -m venv .venv
    .venv\Scripts\activate

**For Linux / macOS:**

.. code-block:: console

    python3 -m venv .venv
    source .venv/bin/activate

2. Install Dependencies
-----------------------

Once the virtual environment is activated, install the required libraries (Streamlit, PyCryptodome, Sphinx, Invoke, etc.):

.. code-block:: console

   pip install -r requirements.txt


3. Running the Application
--------------------------

We use **Invoke** to manage tasks. You can run the Streamlit app with a single command:

.. code-block:: console

   invoke run

Alternatively, you can run it directly via Streamlit:

.. code-block:: console

   streamlit run app.py

4. Building Documentation
-------------------------

To serve the Sphinx documentation locally with live-reload:

.. code-block:: console

   invoke build