# Make the project root a Python package named "ecompro".
# This allows imports such as ``import ecompro.accounts`` and keeps
# compatibility with deployment commands (`gunicorn ecompro.wsgi`).

# The package itself doesn't need to expose anything; its presence is
# sufficient for Python's import machinery.  We keep it empty so that
# it doesn't interfere with application logic.
