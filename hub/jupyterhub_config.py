import os
c = get_config()

c.JupyterHub.spawner_class = 'jhub.SwarmSpawner'

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'

c.JupyterHub.base_url = '/base_url'

# Config required to seperate the proxy from JupyterHub
c.JupyterHub.cleanup_servers = False

c.ConfigurableHTTPProxy.should_start = False

c.ConfigurableHTTPProxy.auth_token = "CONFIGPROXY_AUTH_TOKEN"

c.ConfigurableHTTPProxy.api_url = 'http://jupyter-service_proxy:8001'


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
c.SwarmSpawner.dockerimages = [
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

# Limit cpu/mem to 4 cores/8 GB mem
# During conjestion, kill random internal processes to limit
# available load to 1 core/ 2GB mem
# c.SwarmSpawner.resource_spec = {
#     'cpu_limit': int(8 * 1e9),
#     'mem_limit': int(8192 * 1e6),
#     'cpu_reservation': int(1 * 1e9),
#     'mem_reservation': int(1024 * 1e6),
# }
