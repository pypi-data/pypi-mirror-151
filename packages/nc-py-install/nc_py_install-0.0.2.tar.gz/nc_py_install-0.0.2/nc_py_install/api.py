"""File contains implementations of wrapper functions for Python and Pip API."""

import logging
import sys
from dataclasses import dataclass
from importlib import invalidate_caches
from importlib.metadata import PackageNotFoundError, files, requires, version
from os import environ, makedirs, path, remove
from pathlib import Path
from re import IGNORECASE, MULTILINE, search, sub
from subprocess import DEVNULL, CalledProcessError, TimeoutExpired, run
from typing import Dict, List, Tuple, Union
from warnings import warn

try:
    import requirements
except ImportError:  # pragma: no cover
    requirements = None  # pragma: no cover


@dataclass
class Options:
    """Dataclass with runtime properties."""

    _app_data: str = ""
    dev: bool = False
    pip_present: bool = False
    pip_version: tuple = (0, 0, 0)
    pip_local: bool = False

    @property
    def app_data(self) -> str:
        return self._app_data

    @app_data.setter
    def app_data(self, value):
        self._app_data = path.abspath(value)

    @property
    def core_userbase(self) -> str:
        if self.python_local:
            return path.dirname(path.dirname(sys.executable))
        init_local_dir()
        return self.local_dir

    @property
    def local_dir(self):
        return str(path.join(self.app_data, ".local"))

    @property
    def python_local(self) -> bool:
        return sys.executable.startswith(self.app_data)


OPTIONS = Options()
Log = logging.getLogger("pyfrm.install")


def update_pip_info() -> None:
    OPTIONS.pip_local = False
    OPTIONS.pip_version = check_pip()
    _pip = OPTIONS.pip_version[0] >= 21
    if _pip:
        _location = get_package_location("pip")
        if _location:
            if _location.startswith(OPTIONS.app_data):
                OPTIONS.pip_local = True
        else:
            Log.warning("Cant determine pip location, assume that it is global.")
    OPTIONS.pip_present = _pip


def init_local_dir() -> None:
    if not path.isdir(OPTIONS.local_dir):
        Log.info("Creating local directory: %s", OPTIONS.local_dir)
        try:
            makedirs(OPTIONS.local_dir, mode=0o764)
        except OSError as e:
            Log.error("[REPORT]Can not create `local` directory.")
            raise OSError from e


def get_modified_env(userbase: str = "", python_path: str = "") -> dict:
    modified_env = dict(environ)
    modified_env["PYTHONUSERBASE"] = userbase if userbase else OPTIONS.core_userbase
    if python_path:
        modified_env["PYTHONPATH"] = python_path
    modified_env["_PIP_LOCATIONS_NO_WARN_ON_MISMATCH"] = "1"
    return modified_env


def get_site_packages(userbase: str = "") -> str:
    _env = get_modified_env(userbase=userbase)
    try:
        _result = run(
            [sys.executable, "-m", "site", "--user-site"],
            capture_output=True,
            check=True,
            env=_env,
        )
        return _result.stdout.decode("utf-8").rstrip("\n")
    except (OSError, ValueError, TypeError, TimeoutExpired, CalledProcessError) as _exception_info:
        Log.exception("Exception %s:", type(_exception_info).__name__)
        return ""


def check_pip() -> tuple:
    _ret = (0, 0, 0)
    pckg_version = get_package_version("pip")
    if pckg_version:
        m_groups = search(r"(\d+(\.\d+){0,2})", pckg_version, flags=MULTILINE + IGNORECASE)
        if m_groups:
            pip_version = tuple(map(int, str(m_groups.groups()[0]).split(".")))
            return pip_version if len(pip_version) > 2 else pip_version + (0,)
    return _ret


def remove_pip_warnings(pip_output: str) -> str:
    return sub(r"^\s*WARNING:.*\n?", "", pip_output, flags=MULTILINE + IGNORECASE)


def pip_call(params, userbase: str = "", python_path: str = "", user=False, cache=None) -> Tuple[bool, str]:
    Log.debug("pip_call(USERBASE<%s> PATH<%s>)", userbase, python_path)
    try:
        etc = ["--disable-pip-version-check"]
        _env = get_modified_env(userbase=userbase, python_path=python_path)
        if user:
            etc += ["--user"]
        if cache is False:
            etc += ["--no-cache-dir"]
        elif cache is True:
            etc += ["--cache-dir", _env["PYTHONUSERBASE"]]
        Log.debug("_env=<%s>", _env)
        pip_run_args = [sys.executable, "-m", "pip"] + params + etc
        Log.debug("_args=<%s>", pip_run_args)
        _result = run(pip_run_args, capture_output=True, check=False, env=_env)
        _stderr = _result.stderr.decode("utf-8")
        _stdout = _result.stdout.decode("utf-8")
        if _stderr:
            Log.debug("pip.stderr:\n%s".rstrip("\n"), _stderr)
        if _stdout:
            Log.debug("pip.stdout:\n%s".rstrip("\n"), _stdout)
        if not remove_pip_warnings(_stderr):
            return True, _stdout
        return False, _stderr
    except (OSError, ValueError, TypeError, TimeoutExpired) as _exception_info:
        return False, f"Exception {type(_exception_info).__name__}: {str(_exception_info)}"


def add_python_path(_path: str, first: bool = False) -> str:
    added_path = ""
    if _path:
        try:
            sys.path.pop(sys.path.index(_path))
        except (ValueError, IndexError):
            added_path = _path
        if first:
            sys.path.insert(0, _path)
        else:
            sys.path.append(_path)
        invalidate_caches()
    return added_path


def remove_python_path(_path: str) -> None:
    if _path:
        try:
            sys.path.pop(sys.path.index(_path))
            invalidate_caches()
        except (ValueError, IndexError):
            pass


def download_file(url: str, out_path: str) -> bool:
    n_download_clients = 2
    for _ in range(2):
        try:
            run(
                ["wget", "-q", "--no-check-certificate", url, "-O", out_path],
                timeout=90,
                stderr=DEVNULL,
                stdout=DEVNULL,
                check=True,
            )
            Log.debug("`%s` finished downloading.", out_path)
            return True
        except (CalledProcessError, TimeoutExpired):
            break
        except FileNotFoundError:
            n_download_clients -= 1
            break
    for _ in range(2):
        try:
            run(["curl", "-L", url, "-o", out_path], timeout=90, stderr=DEVNULL, stdout=DEVNULL, check=True)
            Log.debug("`%s` finished downloading.", out_path)
            return True
        except (CalledProcessError, TimeoutExpired):
            break
        except FileNotFoundError:
            n_download_clients -= 1
            break
    if not n_download_clients:
        Log.error("Both curl and wget cannot be found.")
    return False


def install_pip() -> bool:
    Log.info("Start installing local pip.")
    get_pip_path = str(path.join(OPTIONS.core_userbase, "get-pip.py"))
    if not download_file("https://bootstrap.pypa.io/get-pip.py", get_pip_path):
        Log.error("Cant download pip installer.")
        return False
    try:
        Log.info("Running get-pip.py...")
        _env = get_modified_env(OPTIONS.core_userbase)
        _result = run(
            [
                sys.executable,
                get_pip_path,
                "--user",
                "--cache-dir",
                OPTIONS.core_userbase,
                "--no-warn-script-location",
            ],
            capture_output=True,
            check=False,
            env=_env,
        )
        Log.debug("get-pip.stdout:\n%s", _result.stdout.decode("utf-8"))
        full_reply = _result.stderr.decode("utf-8")
        if full_reply:
            Log.debug("get-pip.stderr:\n%s", full_reply)
        if not remove_pip_warnings(full_reply):
            return True
        Log.error("get-pip returned:\n%s", full_reply)
    except (OSError, ValueError, TypeError, TimeoutExpired) as _exception_info:
        Log.exception("Exception %s:", type(_exception_info).__name__)
    finally:
        try:
            remove(get_pip_path)
        except OSError:
            Log.warning("Cant remove `%s`", get_pip_path)
    return False


def update_pip() -> bool:
    if not OPTIONS.pip_present:
        Log.error("No compatible pip found.")
        return False
    if OPTIONS.pip_local:
        _call_result, _message = pip_call(
            ["install", "--upgrade", "pip", "--no-warn-script-location"], user=True, cache=True
        )
        if not _call_result:
            return False
    return True


def remove_extra_from_pckg_name(name: str) -> str:
    return sub(r"\(.*?\)", "", sub(r"\[.*?]", "", name)).strip()


def get_package_version(name: str) -> Union[str, None]:
    name = remove_extra_from_pckg_name(name)
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def get_package_dependencies(name: str) -> Union[Dict[str, List[str]], None]:
    name = remove_extra_from_pckg_name(name)
    try:
        dependencies = requires(name)
    except PackageNotFoundError:
        return None
    if dependencies is None:
        dependencies = []
    requires_list = []
    optional_list = []
    for i in dependencies:
        i_info = i.split(";")
        if len(i_info) < 2:
            requires_list.append(i_info[0])
        elif i_info[1].find("optional") != -1:
            optional_list.append(i_info[0])
    return {"requires": requires_list, "optional": optional_list}


def get_package_location(name: str) -> str:
    name = remove_extra_from_pckg_name(name)
    try:
        files_list = files(name)
        if files_list is not None:
            for i in files_list:
                i_path = Path(i.locate())
                if i_path.name.lower() in ("metadata", "sources.txt"):
                    r = str(i_path.parent)
                    if i_path.parent.parent.name.lower() in ("site-packages", "dist-packages"):
                        r = str(i_path.parent.parent)
                    return r
    except PackageNotFoundError:
        pass
    return ""


def get_userbase_for_app(app_name: str) -> str:
    if app_name:
        _app_packages_dir = path.join(OPTIONS.app_data, app_name)
        if not path.isdir(_app_packages_dir):
            Log.info("Creating app directory: %s", _app_packages_dir)
            makedirs(_app_packages_dir, mode=0o774)
        return _app_packages_dir
    return OPTIONS.core_userbase


def pckg_check(pckg_name: str, userbase: str = "") -> Tuple[list, list, list]:
    added_path = add_python_path(get_site_packages(userbase=userbase), first=True)
    installed_list = []
    not_installed_list = [{"package": pckg_name, "location": "", "version": ""}]
    not_installed_opt_list = []
    dependencies = get_package_dependencies(pckg_name)
    if dependencies is not None:
        not_installed_list.clear()
        for dependency in dependencies["requires"] + dependencies["optional"]:
            dependency = remove_extra_from_pckg_name(dependency)
            dependency_version = get_package_version(dependency)
            dependency_info = {
                "package": dependency,
                "version": dependency_version if dependency_version else "",
                "location": get_package_location(dependency),
            }
            if dependency_info["version"]:
                installed_list.append(dependency_info)
            elif dependency in dependencies["requires"]:
                not_installed_list.append(dependency_info)
                Log.error("Missing %s", dependency)
            else:
                not_installed_opt_list.append(dependency_info)
                Log.warning("Missing %s", dependency)
    remove_python_path(added_path)
    return installed_list, not_installed_list, not_installed_opt_list


def requirements_check(requirements_file: Union[Path, str], userbase: str = "") -> Tuple[list, list]:
    if requirements is None:
        warn("requirements data cannot be read without `requirements-parser` dependency")
        return [], []
    dependencies = []
    with open(requirements_file, "r", encoding="utf-8") as f:
        for req in requirements.parse(f):
            dependencies.append(req.name)
    installed_list = []
    not_installed_list = []
    added_path = add_python_path(get_site_packages(userbase=userbase), first=True)
    for dependency in dependencies:
        dependency_version = get_package_version(dependency)
        dependency_info = {
            "package": dependency,
            "version": dependency_version if dependency_version else "",
            "location": get_package_location(dependency),
        }
        if dependency_info["version"]:
            installed_list.append(dependency_info)
        else:
            not_installed_list.append(dependency_info)
    remove_python_path(added_path)
    return installed_list, not_installed_list


def pckg_install(pckg_name: str, userbase: str = "", extra_args=None) -> bool:
    if extra_args is None:
        extra_args = []
    if not OPTIONS.pip_present:
        if not install_pip():
            Log.error("Cant install local pip.")
            return False
        update_pip_info()
        if not OPTIONS.pip_present:
            Log.error("Cant run pip after local install.")
            return False
    from_file = pckg_name.startswith("-r ")
    if from_file:
        pip_args = ["install"] + pckg_name.split(sep=" ") + ["--no-warn-script-location"] + extra_args
    else:
        pip_args = ["install", pckg_name, "--no-warn-script-location"] + extra_args
    _result, _message = pip_call(pip_args, userbase=userbase, user=True, cache=True)
    if not _result:
        Log.error("Cant install %s. Pip output:\n%s", pckg_name, _message)
        return False
    if not from_file:
        clear_name = pckg_name.split("==")[0]
        added_path = add_python_path(get_site_packages(userbase=userbase), first=True)
        dependencies = get_package_dependencies(clear_name)
        remove_python_path(added_path)
        if dependencies and dependencies["optional"]:
            _result, _message = pip_call(
                ["install", pckg_name + "[optional]", "--no-warn-script-location"] + extra_args,
                userbase=userbase,
                user=True,
                cache=True,
            )
            if not _result:
                Log.warning("Cant install optional packages for %s. \n%s", clear_name, _message)
    return True


def pckg_delete(pckg_name: Union[str, list], userbase: str = "") -> bool:
    if isinstance(pckg_name, str):
        pckg_name = [pckg_name]
    _result, _message = pip_call(
        ["uninstall", "-y"] + pckg_name,
        userbase=userbase,
        cache=True,
    )
    if not _result:
        Log.warning("Cant uninstall packages for %s. Pip output:\n%s", pckg_name, _message)
        return False
    return True


def requirements_delete(requirements_file: Union[Path, str], userbase: str = "") -> None:
    if requirements is None:
        warn("requirements data cannot be read without `requirements-parser` dependency")
        return
    dependencies = []
    with open(requirements_file, "r", encoding="utf-8") as f:
        for req in requirements.parse(f):
            dependencies.append(req.name)
    pckg_delete(dependencies, userbase=userbase)
