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
    binutils \
    fonts-dejavu \
    tzdata \
    gfortran \
    emacs \
    pandoc \
    curl && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8888

# Environement variables
ENV BH_CONFIG /opt/conda/etc/bohrium/config.ini
ENV CONDA_DIR=/opt/conda

USER jovyan

# Juptyer
RUN pip install \
    jupyterhub==0.7.2 \
    'notebook>=5.0,<=6.0' \
    jupyterlab==0.29.2

# Create python2 environement
RUN conda create -n python2 python=2 ipykernel && \
    /opt/conda/envs/python2/bin/python -m ipykernel install --user && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR

# Install bohrium/matplotlib into python3 and python2 environment
RUN conda install -qy gcc=4.8.2 && \
    conda install -qy -c bohrium bohrium && \
    conda install -qy matplotlib && \
    conda install -qy -n python2 -c bohrium bohrium && \
    conda install -qy -n python2 matplotlib && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR

RUN ln -s /opt/conda/bin/gcc /opt/conda/bin/cc

# Create R environment
RUN conda create -n r && \
    conda install -qy -n r \
    'r-base=3.3.2' \
    'r-irkernel=0.7*' \
    'r-plyr=1.8*' \
    'r-devtools=1.12*' \
    'r-tidyverse=1.0*' \
    'r-shiny=0.14*' \
    'r-rmarkdown=1.2*' \
    'r-forecast=7.3*' \
    'r-rsqlite=1.1*' \
    'r-reshape2=1.4*' \
    'r-nycflights13=0.2*' \
    'r-caret=6.0*' \
    'r-rcurl=1.95*' \
    'r-crayon=1.3*' \
    'r-randomforest=4.6*' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR && \
    /opt/conda/envs/r/bin/R -e 'IRkernel::installspec()'

USER root
RUN ln -s /usr/lib/x86_64-linux-gnu /usr/lib64
ADD . /app
RUN fix-permissions /app

USER jovyan

# Install ShareLinks data access lib for python3 and python2
RUN cd /app/nbi_data_access && \
    pip install -r requirements.txt && \
    pip install -r tests/requirements.txt && \
    python setup.py install && \
    python setup.py test && \
    /opt/conda/envs/python2/bin/pip install -r requirements.txt && \
    /opt/conda/envs/python2/bin/pip install -r tests/requirements.txt && \
    /opt/conda/envs/python2/bin/python setup.py install && \
    /opt/conda/envs/python2/bin/python setup.py test

COPY jupyter_notebook_config.py /etc/jupyter/
RUN /usr/local/bin/fix-permissions /etc/jupyter/

# Run container as
USER jovyan