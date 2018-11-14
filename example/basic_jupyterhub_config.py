import os
from jhub.mount import SSHFSMounter

c = get_config()

c.JupyterHub.spawner_class = 'jhub.SwarmSpawner'

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'

c.JupyterHub.base_url = '/base_url'

# First pulls can be really slow, so let's give it a big timeout
c.SwarmSpawner.start_timeout = 60 * 15

c.SwarmSpawner.jupyterhub_service_name = 'jupyter-service_jupyterhub'

c.SwarmSpawner.networks = ["jupyter-service_default"]

# The path at which the notebook will start
notebook_dir = os.environ.get('NOTEBOOK_DIR') or '/home/jovyan/work/'
c.SwarmSpawner.notebook_dir = notebook_dir

# 'args' is the command to run inside the service
c.SwarmSpawner.container_spec = {
    'args': ['/usr/local/bin/start-singleuser.sh',
             '--NotebookApp.ip=0.0.0.0',
             '--NotebookApp.port=8888'],
    'env': {'JUPYTER_ENABLE_LAB': '1'}
}

# Before the user can select which image to spawn,
# user_options has to be enabled
c.SwarmSpawner.use_user_options = True

# Available docker images the user can spawn
c.SwarmSpawner.dockerimages = [
    {'image': 'nielsbohr/base-notebook:latest',
     'name': 'Basic Python Notebook'}
]

# Authenticator, all users can use the default password. Only for dev/test
c.JupyterHub.authenticator_class = 'jhubauthenticators.DummyAuthenticator'
c.DummyAuthenticator.password = 'password'