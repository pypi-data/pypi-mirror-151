"""
Import all possible stuff that can be used in `nc-py-frm` and `nc-py-api`
"""

from ._version import __version__
from .api import (
    OPTIONS,
    add_python_path,
    get_package_dependencies,
    get_package_location,
    get_package_version,
    get_site_packages,
    get_userbase_for_app,
    pckg_check,
    pckg_delete,
    pckg_install,
    remove_python_path,
    requirements_check,
    requirements_delete,
    update_pip_info,
)
from .cli import main
