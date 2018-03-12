import os
import docker
import pytest
import time


HUB_IMAGE_TAG = 'hub:test'
HUB_SERVICE_NAME = "jupyterhub"
NGINX_SERVICE_NAME = "nginx"
NGINX_IMAGE_TAG = 'nginx:test'
NETWORK_NAME = 'swarm_test'

hub_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(
    __file__))), 'hub')
nginx_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(
    __file__))), 'nginx')


@pytest.fixture(scope='function')
def swarm():
    """Initialize the docker swarm that's going to run the servers
    as services.
    """
    client = docker.from_env()
    client.swarm.init(advertise_addr="192.168.99.100")
    yield client.swarm.attrs
    client.swarm.leave(force=True)


@pytest.fixture(scope='function')
def network():
    """Create the overlay network that the hub and server services will
    use to communicate.
    """
    client = docker.from_env()
    network = client.networks.create(
        name=NETWORK_NAME,
        driver="overlay",
        options={"subnet": "192.168.0.0/20"},
        attachable=True
    )
    yield network
    network_id = network.id
    network.remove()
    removed = False
    while not removed:
        try:
            client.networks.get(network_id)
        except docker.errors.NotFound:
            removed = True


@pytest.fixture(scope='function')
def hub_image():
    """Build the images for the jupyterhub, nginx and notebook.
    """
    client = docker.from_env()

    # Build the image from the root of the package
    image = client.images.build(path=hub_dir, tag=HUB_IMAGE_TAG, rm=True,
                                pull=True)
    yield image
    image_id = image.id
    if type(image) == tuple:
        client.images.remove(image[0].tags[0], force=True)
    else:
        client.images.remove(image.tags[0], force=True)

    removed = False
    while not removed:
        try:
            client.images.get(image_id)
        except docker.errors.NotFound:
            removed = True


@pytest.fixture(scope='function')
def nginx_image():
    """Build the images for the jupyterhub, nginx and notebook. """
    client = docker.from_env()

    # Build the image from the root of the package
    image = client.images.build(path=nginx_dir, tag=NGINX_IMAGE_TAG, rm=True,
                                pull=True)
    yield image
    image_id = image.id
    if type(image) == tuple:
        client.images.remove(image[0].tags[0], force=True)
    else:
        client.images.remove(image.tags[0], force=True)

    removed = False
    while not removed:
        try:
            client.images.get(image_id)
        except docker.errors.NotFound:
            removed = True


@pytest.fixture
def hub_service(hub_image, swarm, network):
    """Launch the hub service.
    Note that we don't directly use any of the arguments,
    but those fixtures need to be in place before we can launch the service.
    """
    client = docker.from_env()
    config_path = os.path.join(hub_dir, 'jupyterhub_config.py')
    service = client.services.create(
        image=HUB_IMAGE_TAG,
        name=HUB_SERVICE_NAME,
        mounts=[
            ":".join(["/var/run/docker.sock", "/var/run/docker.sock", "rw"])],
        networks=[NETWORK_NAME],
        endpoint_spec=docker.types.EndpointSpec(ports={8000: 8000}))

    # Wait for the service's task to start running
    while service.tasks() and \
                    service.tasks()[0]["Status"]["State"] != "running":
        time.sleep(1)

    # And wait some more. This is...not great, but there seems to be
    # a period after the task is running but before the hub will accept
    # connections.
    # If the test code attempts to connect to the hub during that time,
    # it fails.
    time.sleep(10)

    yield service
    service_id = service.id
    service.remove()
    removed = False
    while not removed:
        try:
            client.services.get(service_id)
        except docker.errors.NotFound:
            removed = True


@pytest.fixture(scope='function')
def nginx_service(nginx_image, swarm, network):
    """The nginx service is spawned """
    client = docker.from_env()
    service = client.services.create(
        image=NGINX_IMAGE_TAG,
        name=NGINX_SERVICE_NAME,
        networks=[NETWORK_NAME],
        endpoint_spec=docker.types.EndpointSpec(ports={80:8000})
    )

    yield service
    service_id = service.id
    service.remove()
    removed = False
    while not removed:
        try:
            client.services.get(service_id)
        except docker.errors.NotFound:
            removed = True