#Extension of jupyterhub

FROM jupyterhub/jupyterhub:0.7.2

MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

RUN apt-get update && apt-get -y install python3-pip && \
    useradd -ms /bin/bash jovyan

RUN mkdir -p /home/jovyan/work

## Enable the container to add docker-volume-sshfs to the swarm host
## Temporary install docker-ce to install the sshfs volume plugin
## Important -> remove docker in same layer so it dosen't cache over to the next
RUN  apt-get update && apt-get install -y --no-install-recommends \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     software-properties-common && \
     curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add - && \
     add-apt-repository \
     "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
     $(lsb_release -cs) \
     stable" && \
     apt-get update && \
     apt-get install -y docker-ce && \
     git clone https://github.com/rasmunk/docker-volume-sshfs.git

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

COPY jupyterhub_config.py /srv/jupyterhub/
CMD jupyterhub --debug
