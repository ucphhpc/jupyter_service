#!/opt/conda/bin/python
import os
import subprocess


def expanduser(path):
    return os.path.expanduser(path)


def exists(path):
    return os.path.exists(expanduser(path))


def makedirs(path):
    try:
        os.makedirs(expanduser(path))
        return True, "Created: {}".format(path)
    except IOError as err:
        return False, "Failed to create the directory path: {} - {}".format(path, err)


local_py3_base = os.environ.get("JUPYTER_KERNEL_PYTHON3_PYTHONUSERBASE", None)

aliases = []
if local_py3_base:
    pip = f'alias pip="PYTHONUSERBASE={local_py3_base} PIP_PREFIX={local_py3_base} pip"'
    pip3 = (
        f'alias pip3="PYTHONUSERBASE={local_py3_base} PIP_PREFIX={local_py3_base} pip3"'
    )

    python = f'alias python="PYTHONUSERBASE={local_py3_base} python"'
    python3 = f'alias python3="PYTHONUSERBASE={local_py3_base} python3"'
    aliases.extend([pip, pip3, python, python3])

    python_versions = ["3.10", "3.11", "3.12"]
    for version in python_versions:
        python_version = (
            f'alias python{version}="PYTHONUSERBASE={local_py3_base} python{version}"'
        )
        python_version_m = (
            f'alias python{version}m="PYTHONUSERBASE={local_py3_base} python{version}m"'
        )
        aliases.extend([python_version, python_version_m])

    # Ensure the local_py3_base is present
    if not exists(local_py3_base):
        created, message = makedirs(local_py3_base)
        if not created:
            print(message)

home = os.environ.get("HOME", None)
if aliases and home:
    alias_path = os.path.join(home, ".bash_aliases")
    if not os.path.exists(alias_path):
        os.mknod(alias_path, mode=0o664)

    for alias in aliases:
        subprocess.run(
            ["echo '{}' >> {}/.bash_aliases".format(alias, home)], shell=True
        )
