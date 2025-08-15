# DAG config
import sys
import os
from docker.types import Healthcheck

SERVICE_NAME = "jupyter-service"
JOVYAN_UID = "1000"
JOVYAN_GID = "100"

c = get_config()

c.JupyterHub.spawner_class = "jhub.SwarmSpawner"
c.JupyterHub.ip = "0.0.0.0"
c.JupyterHub.port = 443

# https://jupyterhub.readthedocs.io/en/stable/getting-started/networking-basics.html
# hub_ip and hub_port are used when the proxy is remote or isoldated
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_port = 443

# Config required to seperate the proxy from JupyterHub
c.JupyterHub.cleanup_proxy = False
c.JupyterHub.cleanup_servers = False
c.ConfigurableHTTPProxy.should_start = False
c.ConfigurableHTTPProxy.api_url = "http://proxy:444"

# number of allowed servers, 0 means unlimited
c.JupyterHub.active_server_limit = 0

# HTTPS / SSL setup
c.JupyterHub.ssl_key = os.path.join(os.sep, "etc", "ssl", "certs", "jupyterhub.key")
c.JupyterHub.ssl_cert = os.path.join(os.sep, "etc", "ssl", "certs", "jupyterhub.cert")

# First pulls can be really slow, so let's give it a big timeout
c.SwarmSpawner.start_timeout = 60 * 2
c.SwarmSpawner.http_timeout = 60

c.SwarmSpawner.jupyterhub_service_name = "{}_jupyterhub".format(SERVICE_NAME)
c.SwarmSpawner.networks = ["{}_default".format(SERVICE_NAME)]

# Paths
home_path = os.path.join(os.sep, "home", "jovyan")
mount_dirs = ["work"]
r_env_path = os.path.join(os.sep, "opt", "conda", "envs", "r")

root_dir = {}

for dir in mount_dirs:
    path = os.path.join(home_path, dir)
    persistent_storage_path = os.path.join(path, "persistent_storage")
    r_libs_path = "{}:{}:{}".format(
        os.path.join(persistent_storage_path, "R", "libs"),
        os.path.join(r_env_path, "lib", "R", "library"),
        os.path.join(r_env_path, "lib"),
    )
    python3_path = os.path.join(persistent_storage_path, "python3")
    julia_path = os.path.join(persistent_storage_path, "julia")

    root_dir[dir] = {
        "path": path,
        "r_libs": r_libs_path,
        "python3": python3_path,
        "julia_path": julia_path,
    }

conda_path = os.path.join(os.sep, "opt", "conda")
before_notebook_path = os.path.join(os.sep, "usr", "local", "bin", "before-notebook.d")
start_notebook_path = os.path.join(os.sep, "usr", "local", "bin", "start-notebook.d")
r_env_path = os.path.join(conda_path, "envs", "r")
r_environ_path = os.path.join(r_env_path, "lib", "R", "etc", "Renviron")
r_conf_path = os.path.join(os.sep, "etc", "rstudio", "rserver.conf")
jupyter_startup_files_path = os.path.join(os.sep, "jupyter_startup_files")
jupyter_share_path = os.path.join(conda_path, "share", "jupyter")

general_configs = [
    {
        "config_name": "{}_1_deactivate_auto_conda_base_config".format(SERVICE_NAME),
        "filename": os.path.join(
            before_notebook_path, "1_deactivate_auto_conda_base.py"
        ),
        "uid": JOVYAN_UID,
        "gid": JOVYAN_GID,
        "mode": 0o555,
    },
    {
        "config_name": "{}_2_set_default_conda_env_config".format(SERVICE_NAME),
        "filename": os.path.join(before_notebook_path, "2_set_default_conda_env.py"),
        "uid": JOVYAN_UID,
        "gid": JOVYAN_GID,
        "mode": 0o555,
    },
    {
        "config_name": "{}_3_append_to_notebook_config".format(SERVICE_NAME),
        "filename": os.path.join(before_notebook_path, "3_append_to_notebook.py"),
        "uid": JOVYAN_UID,
        "gid": JOVYAN_GID,
        "mode": 0o555,
    },
    {
        "config_name": "{}_4_create_ipython_profile_start_config".format(SERVICE_NAME),
        "filename": os.path.join(
            before_notebook_path, "4_create_ipython_profile_start.py"
        ),
        "uid": JOVYAN_UID,
        "gid": JOVYAN_GID,
        "mode": 0o555,
    },
    {
        "config_name": "{}_5_create_r_libs_path_config".format(SERVICE_NAME),
        "filename": os.path.join(before_notebook_path, "5_create_r_libs_path.py"),
        "uid": JOVYAN_UID,
        "gid": JOVYAN_GID,
        "mode": 0o555,
    },
    {
        "config_name": "{}_6_set_jupyter_kernels_config".format(SERVICE_NAME),
        "filename": os.path.join(before_notebook_path, "6_set_jupyter_kernels.py"),
        "uid": JOVYAN_UID,
        "gid": JOVYAN_GID,
        "mode": 0o555,
    },
    {
        "config_name": "{}_7_set_python_pip_aliases_config".format(SERVICE_NAME),
        "filename": os.path.join(before_notebook_path, "7_set_python_pip_aliases.py"),
        "uid": JOVYAN_UID,
        "gid": JOVYAN_GID,
        "mode": 0o555,
    },
    {
        "config_name": "{}_8_welcome_message_config".format(SERVICE_NAME),
        "filename": os.path.join(before_notebook_path, "8_welcome_message.py"),
        "uid": JOVYAN_UID,
        "gid": JOVYAN_GID,
        "mode": 0o555,
    },
    {
        "config_name": "{}_update_path_env_config".format(SERVICE_NAME),
        "filename": os.path.join(jupyter_startup_files_path, "update_path_env.py"),
        "uid": JOVYAN_UID,
        "gid": JOVYAN_GID,
        "mode": 0o555,
    },
    {
        "config_name": "{}_r_environ_config".format(SERVICE_NAME),
        "filename": r_environ_path,
        "uid": JOVYAN_UID,
        "gid": JOVYAN_GID,
        "mode": 0o440,
    },
    {
        "config_name": "{}_r_server_config".format(SERVICE_NAME),
        "filename": r_conf_path,
        "uid": JOVYAN_UID,
        "gid": JOVYAN_GID,
        "mode": 0o440,
    },
]

c.SwarmSpawner.configs = general_configs

# Which user state varibales should be used to format the to-be-spawned config
c.SwarmSpawner.user_format_attributes = ["mount_data", "user_data", "name"]

# Environments
general_env = {
    "NOTEBOOK_DIR": root_dir["work"]["path"],
    "NB_UID": JOVYAN_UID,
    "NB_GID": JOVYAN_GID,
    "IPYTHON_STARTUP_DIR": jupyter_startup_files_path,
    "JUPYTER_KERNEL_PYTHON3_PYTHONUSERBASE": root_dir["work"]["python3"],
    "DEFAULT_CONDA_ENVIRONMENT": "python3",
    "HISTFILE": "{}/.bash_history_dag".format(root_dir["work"]["path"]),
}

r_env = general_env.copy()
r_env["DEFAULT_CONDA_ENVIRONMENT"] = "r"
r_libs_paths = [
    os.path.join(r_env_path, "lib", "R", "library"),
    os.path.join(r_env_path, "lib"),
]
r_env["LD_LIBRARY_PATH"] = "{}:{}:{}".format(
    ":".join(r_libs_paths), root_dir["work"]["r_libs"], os.path.join(os.sep, "lib")
)
r_env["R_LIBS_USER"] = root_dir["work"]["r_libs"]
r_env["R_ENVIRON_USER"] = r_environ_path

julia_env = general_env.copy()
julia_env["DEFAULT_CONDA_ENVIRONMENT"] = ""
julia_env["JULIA_DEPOT_PATH"] = root_dir["work"]["julia_path"]
julia_env["JUPYTER_KERNEL_JULIA_JULIA_DEPOT_PATH"] = root_dir["work"]["julia_path"]

# Set the default environment and the
# standard path that JupyterLab should start in
c.SwarmSpawner.container_spec = {
    "env": general_env,
    "workdir": root_dir["work"]["path"],
    "args": [
        "/usr/local/bin/start-singleuser.sh",
        "--ServerApp.ip=0.0.0.0",
        "--ServerApp.port=8888",
        "--LabApp.default_url=/lab/tree/work",
    ],
    # TODO, adjust this to be more linient than the default upstream value
    # https://github.com/jupyter/docker-stacks/blob/abea5caf78da2dbe1af0ded0b1e184191016ba57/images/base-notebook/Dockerfile#L71
    # Something like --interval=1m --timeout=10s --retries=3 might do the trick
    "healthcheck": Healthcheck(test=["NONE"]),
}

# Before the user can select which image to spawn,
# user_options has to be enabled
c.SwarmSpawner.use_user_options = True

worker_nodes = {
    "constraints": [
        "node.role == worker",
    ]
}

# Available docker images the user can spawn
c.SwarmSpawner.images = [
    {
        "image": "ucphhpc/datascience-notebook:4.3.6",
        "name": "Datascience Notebook with Python",
        "placement": worker_nodes,
    },
    {
        "image": "ucphhpc/statistics-notebook:4.3.6",
        "name": "Statistics Notebook with Python",
        "placement": worker_nodes,
    },
    {
        "image": "ucphhpc/r-notebook:4.3.6",
        "name": "R Notebook with R-Studio",
        "env": r_env,
        "placement": worker_nodes,
    },
    {
        "image": "ucphhpc/gpu-notebook:4.3.6",
        "name": "AI Notebook",
        "placement": worker_nodes,
    },
    {
        "image": "ucphhpc/chemistry-notebook:4.2.4",
        "name": "Chemistry Notebook with Diffpy",
        "placement": worker_nodes,
    },
    {
        "image": "ucphhpc/geo-notebook:4.3.6",
        "name": "Geo Notebook",
        "placement": worker_nodes,
    },
    {
        "image": "ucphhpc/bio-notebook:4.3.6",
        "name": "Bio Notebook",
        "env": r_env,
        "placement": worker_nodes,
    },
    {
        "image": "ucphhpc/julia-notebook:4.3.6",
        "name": "Julia Notebook",
        "env": julia_env,
        "placement": worker_nodes,
    },
    {
        "image": "ucphhpc/cern-notebook:4.3.6",
        "name": "CERN Notebook",
        "placement": worker_nodes,
    },
    {
        "image": "ucphhpc/fenics-notebook:4.2.6",
        "name": "Finite Element Notebook with FEniCS",
        "placement": worker_nodes,
    },
    {
        "image": "ucphhpc/ocean-notebook:4.3.6",
        "name": "Ocean Notebook",
        "placement": worker_nodes,
    },
    {
        "image": "ucphhpc/qsharp-notebook:4.3.6",
        "name": "Q# Notebook",
        "placement": worker_nodes,
    },
]

# Authenticator
c.JupyterHub.authenticator_class = "jhubauthenticators.DummyAuthenticator"

# Service that checks for inactive notebooks
c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [sys.executable, "-m", "jupyterhub_idle_culler", "--timeout=7200"],
    }
]

# As defined by https://github.com/jupyterhub/jupyterhub-idle-culler
c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "description": "Culls idle servers",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
        ],
        "services": ["jupyterhub-idle-culler-service"],
    }
]
