"""Front-end WSGI module for the project.

This package is kept to support the traditional ``ecompro.wsgi`` import
path used by the deployment platform.  Gunicorn will execute this file
when you run ``gunicorn ecompro.wsgi``.

To make sure that Python treats the directory containing this file as a
package named ``ecompro`` we need the *parent of the project root* on
``sys.path`` rather than the project root itself.  When Render clones the
repository into ``/opt/render/project/src`` the project root is that
directory, so its parent is one level up.  We prepend the parent path
here so that ``import ecompro`` resolves to this directory rather than
looking for a subdirectory called ``ecompro``.
"""

import os
import sys

proj_root = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(proj_root)

# insert parent_dir first if not already present
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# we also keep proj_root on the path because the config package lives
# here and Django will try to import it when configuring settings.
if proj_root not in sys.path:
    sys.path.insert(1, proj_root)

from config.wsgi import application

# expose application under the traditional name
# application = application
