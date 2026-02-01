from invoke import task
"""Start a live-reloading Sphinx documentation server.

Runs "sphinx-autobuild source/ build/" using the provided Invoke context,
which serves the documentation locally and watches the 'source/' directory
for changes, rebuilding output into 'build/' automatically.

Parameters
----------
c : invoke.Context
    Invoke context used to run shell commands.
"""

@task
def build(c):
    c.run("sphinx-autobuild source/ build/")