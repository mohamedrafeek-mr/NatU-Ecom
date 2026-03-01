# try importing sitecustomize explicitly
try:
    import sitecustomize
    print('explicitly imported sitecustomize')
except Exception as e:
    print('failed to import sitecustomize', e)

import sys
print('in script, sys.path[0]=', sys.path[0])
import ecompro.wsgi
print('import succeeded')
