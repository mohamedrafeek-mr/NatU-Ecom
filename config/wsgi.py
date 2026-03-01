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

# The project root directory *is* the ecompro package. When the repository
# is checked out directly into a directory named "ecompro" this is enough
# to allow "import ecompro" (parent_dir contains a folder called
# ``ecompro``).  On Render the clone lands in ``/opt/render/project/src``
# which isn’t named after the package, so the normal import logic would
# fail.  To support both cases we create a lightweight module object
# that points at the project root and register it under the canonical
# package name.  That lets code elsewhere continue to use
# ``ecompro.foo`` imports without rewriting everything.
if os.path.basename(proj_root) != 'ecompro':
    import types
    if 'ecompro' not in sys.modules:
        pkg = types.ModuleType('ecompro')
        pkg.__path__ = [proj_root]
        sys.modules['ecompro'] = pkg

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
