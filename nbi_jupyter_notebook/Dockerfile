FROM python:3.6

MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    libcurl4-openssl-dev \
    python-pycurl \
    ssh

# Juptyer and sshfs
RUN pip3 install \
    jupyterhub==0.7.2 \
    'notebook>=5.0,<=6.0'

ADD . /app
RUN cd /app/nbi_data_access && \
    pip3 install -r requirements.txt && \
    pip3 install -r tests/requirements.txt && \
    python3 setup.py install && \
    python3 setup.py test

#
EXPOSE 8888

#ADD fix-permissions /usr/local/bin/fix-permissions
# create a user, since we don't want to run as root
RUN useradd -m jovyan
ENV HOME=/home/jovyan
WORKDIR $HOME

COPY jupyter_notebook_config.py /etc/jupyter/

# Run container as
USER jovyan
CMD ["jupyterhub-singleuser"]