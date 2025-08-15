#!/opt/conda/bin/python
import os
import subprocess

local_py3_base = os.environ.get("JUPYTER_KERNEL_PYTHON3_PYTHONUSERBASE", None)

aliases = []
if local_py3_base:
    pip = 'alias pip="PYTHONUSERBASE={} pip"'.format(local_py3_base)
    pip3 = 'alias pip3="PYTHONUSERBASE={} pip3"'.format(local_py3_base)

    python = 'alias python="PYTHONUSERBASE={} python"'.format(local_py3_base)
    python3 = 'alias python3="PYTHONUSERBASE={} python3"'.format(local_py3_base)
    aliases.extend([pip, pip3, python, python3])

    python_versions = ["3.10", "3.11"]
    for version in python_versions:
        python_version = (
            f'alias python{version}="PYTHONUSERBASE={local_py3_base} python{version}"'
        )
        python_version_m = (
            f'alias python{version}m="PYTHONUSERBASE={local_py3_base} python{version}m"'
        )
        aliases.extend([python_version, python_version_m])

home = os.environ.get("HOME", None)
if aliases and home:
    alias_path = os.path.join(home, ".bash_aliases")
    if not os.path.exists(alias_path):
        os.mknod(alias_path, mode=0o664)

    for alias in aliases:
        subprocess.run(
            ["echo '{}' >> {}/.bash_aliases".format(alias, home)], shell=True
        )
