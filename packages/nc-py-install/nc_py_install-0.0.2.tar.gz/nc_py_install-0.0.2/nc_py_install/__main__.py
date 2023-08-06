"""
Cloud_Py_Api self install module, for usage as `python3 -m nc_py_install [args]`.
"""

import sys

from .cli import main as _main

if __name__ == "__main__":
    sys.exit(_main())
