===================
jupyter_service
===================

A jupyter notebook docker swarm setup that consists of a standard proxy nginx
and a customised jupyterhub service that spawns individual notebooks for
individual users.

- `NBI Jupyterhub <https://github.com/rasmunk/docker-nbi-jupyterhub.git>`_


------------
Architecture
------------

An overview of how the different components of the
jupyter_service interconnects can be seen below:

TODO: update architecture image

The stack is made of a 2 layered docker swarm stack, i.e. any external
request is received by the jupyterhub service which handles whether a user is allow to start a notebook.

This is defined by `Authenticators <https://jupyterhub.readthedocs.io/en/stable/
reference/authenticators.html>`_ where Jupyterhub allows for a custom
authenticator to be selected based on the local requirements.
Hence how a user should be authenticated before they are able to launch notebooks via the jupyterhub web interface.
The authenticator itself is selected by defining the ``authenticator_class`` variable as shown in
the example/basic_jupyterhub_config.py configuration file.

Beyond authentication, jupyterhub also allows for a custom `Spawner <https://jupyterhub.readthedocs.io/en/stable/reference/spawners.html>`_
scheme to be overloaded.
The default ``spawner_class`` in the example/basic_jupyterhub_config.py configuration file
is defined with the `jhub-swarmspawner <https://github.com/rasmunk/SwarmSpawner>`_ which enables the deployment of
jupyter notebooks on a `Docker Swarm Cluster <https://github.com/docker/swarmkit>`_
cluster whenever a user requests a new notebook.

-------------
Prerequisites
-------------

Before the jupyterhub service is able to launch separate notebook services,
jupyterhub needs access to the hosts docker daemon process. This access can
be gained in a number of ways, one of which is to mount the /var/run/docker
.sock file inside the jupyterhub service as a volume and then ensuring that
the user that executes the ``deploy`` command is part of the ``docker`` system
group. This is the default approach as defined in the docker-compose.yml file.

Another approach would be to expose the docker daemon remotely on port 2376
with TLS verification as explained @ `Docker Docs <https://docs.docker
.com/engine/reference/commandline/dockerd/#description>`_ under "Daemon
socket option".

In addition it requires that the jupyterhub service is deployed on a swarm manager node.
See `Create a swarm <https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm>`_.
Hence the restriction set in the docker-compose file that the jupyterhub service is restricted to a manager node.

By default the example/basic_docker-compose.yml stack also provides an `docker-image-updater <https://github.com/rasmunk/docker-image-updater>`_ service.
This service provides a continuously monitor whether new versions of the specified notebook image is available,
and if so pulls it to every swarm node and prunes previous versions when no other running notebook depends on that particular version.

---------------------
Launching the Service
---------------------

To run a basic stack, simply execute the following command inside the repo
directory::

    docker stack deploy --compose-file example/basic_docker-compose.yml jupyter-service


To verify that the stack is now deployed and the services are being spawned
do::

    docker stack ls
    docker services ls

The ``stack`` command should return that the jupyter-service stacks is running with 2 services, i.e. the jupyterhub and image-updater service.
Beyond that, the ``services`` call should return the 2 individual services are preparing/running.
