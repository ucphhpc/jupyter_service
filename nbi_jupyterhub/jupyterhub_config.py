import os
import docker
import stat

c = get_config()
pwd = os.path.dirname(__file__)

c.JupyterHub.spawner_class = 'cassinyspawner.SwarmSpawner'
c.JupyterHub.hub_ip = '0.0.0.0'

c.JupyterHub.cleanup_servers = False

# First pulls can be really slow, so let's give it a big timeout
c.SwarmSpawner.start_timeout = 60 * 5

c.SwarmSpawner.jupyterhub_service_name = 'nbibda_service_jupyterhub'

c.SwarmSpawner.networks = ["nbibda_service_default"]

# 'args' is the command to run inside the service
c.SwarmSpawner.container_spec = {
    'args': ['/usr/local/bin/start-singleuser.sh'],
    # image needs to be previously pulled
    'Image': '127.0.0.1:5000/nbi_jupyter_notebook',
    'mounts': []
}

# The values here are too low for our OpenStack system
c.SwarmSpawner.resource_spec = {
    'cpu_limit': 1000000,
    'mem_limit': int(512 * 1e6),
    'cpu_reservation': 1000000,
    'mem_reservation': int(512 * 1e6),
}
