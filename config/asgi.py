"""ASGI config for ecompro project.

When executed from the project root, Python's import path points at the
root directory itself.  In order to locate the top-level ``ecompro``
package (which is the project folder) we need the parent directory on
``sys.path``.  This mirrors the logic we apply in ``config/wsgi.py``.
"""

import os
import sys

proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.dirname(proj_root)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
