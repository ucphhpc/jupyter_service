FROM jupyter/base-notebook:e1677043235c
MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

USER root

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    gcc \
    libxml2-dev \
    libxslt-dev \
    libcurl4-openssl-dev \
    libx32gcc-4.8-dev \
    libc6-dev-i386 \
    libgl1-mesa-glx \
    binutils \
    fonts-dejavu \
    tzdata \
    gfortran \
    emacs \
    pandoc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8888
USER jovyan

# Juptyer
RUN pip install \
    jupyterhub==0.7.2 \
    'notebook>=5.0,<=6.0' \
    jupyterlab==0.29.2

# Environement variables
ENV CONDA_DIR=/opt/conda
ENV BH_CONFIG=/home/jovyan/.local/lib/python2.7/site-packages/bohrium/config.ini
ENV PYTHON2_PATH=$CONDA_DIR/envs/python2
ENV PYTHON3_PATH=$CONDA_DIR/envs/python3
ENV NBI_DATA_ACCESS_VER=0.0.1

# Create python2/3 environement
RUN conda create -n python2 python=2 ipykernel \
    && conda create -n python3 python=3 ipykernel \
    && $PYTHON2_PATH/bin/python -m ipykernel install --user \
    && $PYTHON3_PATH/bin/python -m ipykernel install --user \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR

# Install bohrium/matplotlib/pandas/scikit-image for py2/py3
RUN $PYTHON2_PATH/bin/pip install --user bohrium==0.8.10.post78 \
    && $PYTHON2_PATH/bin/pip install \
    matplotlib==2.1.2 \
    pandas==0.22.0 \
    scikit-image==0.13.1 \
    && $PYTHON3_PATH/bin/pip install --user bohrium==0.8.10.post78 \
    && $PYTHON3_PATH/bin/pip install \
    matplotlib==2.1.2 \
    pandas==0.22.0 \
    scikit-image==0.13.1 \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR

# Create R environment
RUN conda create -n r \
    && conda install -qy -n r \
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
    'r-randomforest=4.6*' \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR \
    && /opt/conda/envs/r/bin/R -e 'IRkernel::installspec()'

USER root

RUN ln -s /usr/lib/x86_64-linux-gnu /usr/lib64
ADD . /app
RUN fix-permissions /app

USER jovyan

# Install ShareLinks data access lib for python3 and python2
RUN curl -SL https://github.com/rasmunk/nbi_data_access/archive/$NBI_DATA_ACCESS_VER.tar.gz \
    | tar xz \
    && mv nbi_data_access-$NBI_DATA_ACCESS_VER nbi_data_access \
    && cd nbi_data_access \
    && $PYTHON2_PATH/bin/pip install -r requirements.txt \
    && $PYTHON2_PATH/bin/pip install -r tests/requirements.txt \
    && $PYTHON2_PATH/bin/python setup.py install \
    && $PYTHON2_PATH/bin/pytest \
    && $PYTHON3_PATH/bin/pip install -r requirements.txt \
    && $PYTHON3_PATH/bin/pip install -r tests/requirements.txt \
    && $PYTHON3_PATH/bin/python setup.py install \
    && $PYTHON3_PATH/bin/pytest

COPY jupyter_notebook_config.py /etc/jupyter/
RUN /usr/local/bin/fix-permissions /etc/jupyter/

# Run container as
USER jovyan
