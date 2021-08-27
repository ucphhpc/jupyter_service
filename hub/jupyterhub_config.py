import os
c = get_config()

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'
# IP as seen on the docker network. Can also be a hostname.
c.JupyterHub.hub_connect_ip = "jupyterhub"

c.JupyterHub.base_url = '/base_url'

c.JupyterHub.port = 8000

# Config required to seperate the proxy from JupyterHub
c.JupyterHub.cleanup_servers = False
c.ConfigurableHTTPProxy.should_start = False
c.ConfigurableHTTPProxy.api_url = 'http://proxy:8001'

# Which Spawner to use
c.JupyterHub.spawner_class = 'jhub.SwarmSpawner'

# First pulls can be really slow, so let's give it a big timeout
c.SwarmSpawner.start_timeout = 60 * 15

c.SwarmSpawner.jupyterhub_service_name = 'jupyter-service_jupyterhub'

c.SwarmSpawner.networks = ["jupyter-service_default"]

notebook_dir = os.environ.get('NOTEBOOK_DIR') or '/home/jovyan/work/'
c.SwarmSpawner.notebook_dir = notebook_dir

# 'args' is the command to run inside the service
c.SwarmSpawner.container_spec = {
    'env': {'JUPYTER_ENABLE_LAB': '1'}
}

# Before the user can select which image to spawn,
# user_options has to be enabled
c.SwarmSpawner.use_user_options = True

# Available docker images the user can spawn
c.SwarmSpawner.images = [
    {'image': 'jupyter/base-notebook:latest',
     'name': 'Jupyter Notebook'
     }
]

# Authenticator -> remote user header
c.JupyterHub.authenticator_class = 'jhubauthenticators.DummyAuthenticator'
c.DummyAuthenticator.password = 'password'

# Pass the encoded username to the spawner
c.Authenticator.enable_auth_state = True

# Service that checks for inactive notebooks
# Defaults to kill services that hasen't been used for 2 hour
c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': "python3 cull_idle_servers.py --timeout=7200".split(),
    },
]