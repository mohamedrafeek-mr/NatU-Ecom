"""ASGI entry point for the project.

Like ``wsgi.py``, this module exists so that ``ecompro.asgi`` can be
imported if any tooling or deployment configuration still refers to it.
It simply forwards to the implementation inside ``config/asgi.py``.
"""

from config.asgi import application
