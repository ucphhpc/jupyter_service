FROM jupyter/base-notebook:e1677043235c

MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

USER root

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    libxml2-dev \
    libxslt-dev \
    libcurl4-openssl-dev \
    ssh
 #   software-properties-common \
 #   python-software-properties

# Install bohrium
#RUN add-apt-repository ppa:bohrium/nightly && \
#    apt-get update && \
#    apt-get install -yq --no-install-recommends \
#    bohrium \
#    bohrium3

EXPOSE 8888
RUN echo root:password | chpasswd

# Juptyer and sshfs
RUN pip install \
    jupyterhub==0.7.2 \
    'notebook>=5.0,<=6.0'

# Install ShareLinks data access lib
ADD . /app
RUN cd /app/nbi_data_access && \
    pip install -r requirements.txt && \
    pip install -r tests/requirements.txt && \
    python setup.py install && \
    python setup.py test

COPY jupyter_notebook_config.py /etc/jupyter/
RUN /usr/local/bin/fix-permissions /etc/jupyter/

# Run container as
USER jovyan