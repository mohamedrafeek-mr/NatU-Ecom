# executed automatically by Python at startup when this directory is on sys.path
import os, sys

print('*** sitecustomize running; cwd=', os.getcwd())

# ensure that when the current working directory is the project root,
# the parent directory is available so that the project root itself can
# be imported as a package named "ecompro".

proj_root = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(proj_root)

print('sitecustomize paths:', proj_root, parent_dir)

if parent_dir not in sys.path:
    # insert at front so it takes precedence over proj_root itself
    sys.path.insert(0, parent_dir)

# optional: make sure proj_root is still on path as well
if proj_root not in sys.path:
    sys.path.insert(1, proj_root)

print('sys.path after modification', sys.path[:3])
