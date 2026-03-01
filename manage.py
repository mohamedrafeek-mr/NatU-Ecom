#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # We want Python to resolve the ``ecompro`` package name to the
    # *project directory* (the folder that contains the apps, config,
    # etc.), not the inner package that lives at
    # ``<projectroot>/ecompro``.  To ensure this regardless of the
    # current working directory we only put the parent of the project
    # root on ``sys.path`` and remove the project itself if Python added
    # it automatically.
    base_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = base_dir  # this directory contains manage.py
    parent_dir = os.path.dirname(project_root)

    # Make sure the parent directory is the first entry so that the
    # outer ``ecompro`` namespace package (project root) is found before
    # any inner packages.  The script directory itself can remain on the
    # path as well.
    if sys.path:
        sys.path[0] = parent_dir
    else:
        sys.path.insert(0, parent_dir)

    # Include the project root on the path too; we removed this earlier to
    # avoid the nested package, but since that directory has now been
    # deleted the risk is gone.  Having the project root available allows
    # ``import config`` to work.  It also provides access to the app
    # packages without requiring additional manipulation.
    if project_root not in sys.path:
        sys.path.insert(1, project_root)

    # When the project directory isn’t literally named ``ecompro`` we must
    # still make the package importable under that name so that the
    # rest of the codebase (and any deployment commands) can continue to
    # refer to ``ecompro.*``.  Mirror the logic used in wsgi.py.
    if os.path.basename(project_root) != 'ecompro':
        import types
        if 'ecompro' not in sys.modules:
            pkg = types.ModuleType('ecompro')
            pkg.__path__ = [project_root]
            sys.modules['ecompro'] = pkg

    # Use the standalone config package for settings.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
