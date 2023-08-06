import subprocess
import sys
from os import path
from urllib import parse

import pytest

APP_DATA_DIR = path.abspath("./cloud_py_api")
ARGUMENTS = [sys.executable, "-m", "nc_py_install", "--appdata", parse.quote_plus(APP_DATA_DIR), "--target"]


@pytest.mark.parametrize(
    "package_name, version",
    (
        ("pg8000", "1.26.0"),
        ("pymysql", ""),
        ("pillow-heif", "0.2.2"),
        ("pillow-heif", ""),
        ("SQLAlchemy", ""),
    ),
)
def test_subpackages(package_name, version):
    # Check must fail here and return exitcode = 1
    r = subprocess.run(ARGUMENTS + [package_name] + ["--check"], capture_output=False)
    assert r.returncode == 1
    install_string = package_name + "==" + version if version else package_name
    # Install must succeed
    r = subprocess.run(ARGUMENTS + [install_string] + ["--install"], capture_output=False)
    assert r.returncode == 0
    if version:
        r = subprocess.run(ARGUMENTS + [package_name] + ["--update"], capture_output=False)
        assert r.returncode == 0
    # Clean up, by deleting package.
    r = subprocess.run(ARGUMENTS + [install_string] + ["--delete"], capture_output=False)
    assert r.returncode == 0
    # Call here `check` again to see that `delete` was successful.
    r = subprocess.run(ARGUMENTS + [package_name] + ["--check"], capture_output=False)
    assert r.returncode == 1
