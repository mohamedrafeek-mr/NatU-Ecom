"""WSGI config for ecompro project.

The outer package name changed during refactoring; the project root
itself is now the ``ecompro`` package.  When this file is executed
(either via ``gunicorn config.wsgi`` or ``python -m config.wsgi``) the
current working directory will usually be the project root, which means
``sys.path[0]`` is the project root.  Python will only recognize the
``ecompro`` package if the *parent of the project root* is on the path,
so we add it here.
"""

import os
import sys

# ensure parent dir is on path so ``import ecompro`` resolves to the
# project root folder instead of looking for a subdirectory named
# ``ecompro`` inside the project root.
proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.dirname(proj_root)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
