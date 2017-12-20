#Extension of jupyterhub

FROM jupyterhub/jupyterhub:0.7.2

MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

RUN apt-get update && apt-get -y install python3-pip && \
    useradd -ms /bin/bash jovyan

RUN mkdir -p /home/jovyan/work

## Remote user authenticator with support for MIG mount
RUN git clone https://github.com/rasmunk/jhub_remote_user_authenticator.git && \
    cd jhub_remote_user_authenticator && \
    pip install -r requirements.txt && \
    pip install .

# SwarmSpawner with support for sshfs mount
RUN git clone https://github.com/rasmunk/SwarmSpawner && \
    cd SwarmSpawner && \
    pip install -r requirements/base.txt && \
    pip install -r requirements/tests.txt && \
    touch README.rst && \
    python3 setup.py install

COPY jupyterhub_config.py /srv/jupyterhub/
CMD jupyterhub --debug
