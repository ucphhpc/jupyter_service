FROM jupyterhub/jupyterhub:0.7.2

MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    libcurl4-openssl-dev \
    python-pycurl \
    ssh

# Juptyer and sshfs
RUN pip3 install \
    'notebook>=5.0,<=6.0'

RUN pip3 install jupyterhub-dummyauthenticator
# Install Swarm Spawner
RUN git clone https://github.com/cassinyio/SwarmSpawner && \
    cd SwarmSpawner && \
    pip3 install -r requirements/base.txt && \
    pip3 install -r requirements/tests.txt && \
    touch README.rst && \
    python3 setup.py install && \
    cd ..

ADD . /app
RUN cd /app && \
    pip3 install -r requirements.txt && \
    pip3 install -r tests/requirements.txt && \
    python3 setup.py install && \
    python3 setup.py test

# create a user, since we don't want to run as root
RUN useradd -m jovyan
ENV HOME=/home/jovyan
WORKDIR $HOME
# Run container as
USER jovyan

CMD ["jupyterhub-singleuser"]