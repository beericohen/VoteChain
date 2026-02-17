from invoke import task
import os

@task
def run(c):
    """Run the Streamlit application."""
    c.run("python run_app.py")

@task
def build(c):
    """Build Sphinx documentation."""
    c.run("sphinx-autobuild docs/source/ docs/build/")

