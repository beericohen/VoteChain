Installation & Setup
====================

Prerequisites
-------------
* Python 3.8+
* Pip

1. Create Environment
---------------------
It is recommended to use a virtual environment:

.. code-block:: bash

   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate

2. Install Dependencies
-----------------------
Install the required packages (Streamlit, PyCryptodome, Sphinx):

.. code-block:: bash

   pip install -r requirements.txt

3. Running the System
---------------------
**Run the application:**

.. code-block:: bash

   inv run

The application will open in your default web browser at ``http://localhost:8501``.

4. Building Documentation
-------------------------
To regenerate this documentation site:

.. code-block:: bash

   inv build