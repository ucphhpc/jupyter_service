#Extension of jupyterhub

FROM jupyterhub/jupyterhub:0.7.2

MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

RUN apt-get update && apt-get -y install python3-pip
# Temporary add these usful tools while developing
RUN apt-get -y install vim less net-tools
RUN useradd -ms /bin/bash jovyan
RUN mkdir -p /home/jovyan/work

RUN pip install jupyterhub-dummyauthenticator

RUN git clone https://github.com/cassinyio/SwarmSpawner && \
    cd SwarmSpawner && \
    pip install -r requirements/base.txt && \
    pip install -r requirements/tests.txt && \
    touch README.rst && \
    python3 setup.py install && \
    cd ..

## Remote user authenticator
RUN git clone https://github.com/cwaldbieser/jhub_remote_user_authenticator.git && \
    cd jhub_remote_user_authenticator && \
    pip install .

## Mount home volume plugin
RUN git clone https://github.com/rasmunk/docker-volume-sshfs.git && \
    cd docker-volume-sshfs && \
    make && \
    make enable

COPY jupyterhub_config.py /srv/jupyterhub/
CMD jupyterhub --debug
