c = get_config()

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

c.JupyterHub.confirm_no_ssl = True

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
c.DockerSpawner.container_image = "nbi_jupyter:0.1"

from IPython.utils.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]