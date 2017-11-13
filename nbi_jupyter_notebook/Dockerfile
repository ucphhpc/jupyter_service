FROM jupyter/base-notebook:e1677043235c

MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

USER root
RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    libxml2-dev \
    libxslt-dev \
    libcurl4-openssl-dev \
    ssh \
    libx32gcc-4.8-dev \
    libc6-dev-i386 \
    libgl1-mesa-glx \
    binutils

EXPOSE 8888

# Environement variables
ENV BH_CONFIG /opt/conda/etc/bohrium/config.ini
ENV CONDA_DIR=/opt/conda

ADD . /app
RUN fix-permissions /app

USER jovyan

# Juptyer and sshfs
RUN pip install \
    jupyterhub==0.7.2 \
    'notebook>=5.0,<=6.0'

# Install bohrium
RUN conda install -qy gcc=4.8.2 && \
    conda install -qy -c bohrium bohrium && \
    conda install -qy matplotlib && \
    fix-permissions $CONDA_DIR

RUN ln -s /opt/conda/bin/gcc /opt/conda/bin/cc

USER root
RUN ln -s /usr/lib/x86_64-linux-gnu /usr/lib64

USER jovyan

# Install ShareLinks data access lib
RUN cd /app/nbi_data_access && \
    pip install -r requirements.txt && \
    pip install -r tests/requirements.txt && \
    python setup.py install && \
    python setup.py test

COPY jupyter_notebook_config.py /etc/jupyter/
RUN /usr/local/bin/fix-permissions /etc/jupyter/

# Run container as
USER jovyan