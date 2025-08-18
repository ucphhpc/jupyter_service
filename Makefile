SHELL:=/bin/bash
SERVICE_NAME=jupyter-service
NETWORK_NAME=$(SERVICE_NAME)_default
NETWORK_RANGE=10.50.0.0/16
NETWORK_EXISTS=$(shell docker network inspect $(NETWORK_NAME) > /dev/null 2>&1 && echo 0 || echo 1)
SSL_MOUNT_DIRECTORY_PATH=./ssl/certs/jupyterhub
USE_JUPYTERHUB_CONFIG_PATH=./example/non_ssl/basic_jupyterhub_config.py
USE_DOCKER_COMPOSE_PATH=./example/non_ssl/basic_docker-compose.yml
ARGS=

# NOTE: dynamic lookup with docker as default
DOCKER = $(shell which docker 2>/dev/null)
# if docker compose plugin is not available, try old docker-compose/podman-compose
ifeq (, $(shell ${DOCKER} help|grep compose))
	DOCKER_COMPOSE = $(shell which docker-compose 2>/dev/null)
else
	DOCKER_COMPOSE = ${DOCKER} compose
endif
$(echo ${DOCKER_COMPOSE} >/dev/null)

.PHONY: all
all: venv init

.PHONY: init
init:
ifeq ($(NETWORK_EXISTS), 1)
	@echo No default Docker Swarm network detected for the service: $(SERVICE_NAME)
	@echo Creating Docker Swarm network: $(NETWORK_NAME)
	./init/init-swarm-network.sh $(NETWORK_NAME) $(NETWORK_RANGE)
endif
ifeq (,$(wildcard ./hub/jupyterhub/jupyterhub_config.py))
	@echo No jupyterhub configuration file detected
	@echo Defaulting to the non-SSL version inside ${USE_JUPYTERHUB_CONFIG_PATH}
	@cp ${USE_JUPYTERHUB_CONFIG_PATH} hub/jupyterhub/jupyterhub_config.py
endif
ifeq (,$(wildcard ./docker-compose.yml))
# Geneate and pass secret environment variables to environment file
	@echo No docker-compose.yml file detected
	@echo Defaulting to the non-SSL version inside ${USE_DOCKER_COMPOSE_PATH}
	@ln -s ${USE_DOCKER_COMPOSE_PATH} docker-compose.yml
endif
ifeq (,$(wildcard ./defaults.env))
	@echo No defaults.env file detected
	@echo Generating a default environment setup
	./init/gen-default-environment.sh > defaults.env
	./init/gen-secrets.sh >> defaults.env
endif
ifeq (,$(wildcard ./.env))
# Geneate and pass secret environment variables to environment file
	@echo No .env file detected, linking to the default "defaults.env"
	ln -s defaults.env .env
endif
# Create the designated directory that should contains the
# SSL key and certificate if the JupyterHub is to use HTTPS/SSL connections
ifeq (,$(wildcard ${SSL_MOUNT_DIRECTORY_PATH}))
	@echo Creating missing path: ${SSL_MOUNT_DIRECTORY_PATH} for mounting host SSL files
	@mkdir -p ${SSL_MOUNT_DIRECTORY_PATH}
endif

.PHONY: clean
clean:
	@rm -fr docker-compose.yml
	@rm -fr hub/jupyterhub/jupyterhub_config.py
	@rm -fr .env

.PHONY:	distclean
distclean:
	@rm -fr venv
	@defaults.env

.PHONY: daemon
daemon:
	${DOCKER} stack deploy -c docker-compose.yml $(SERVICE_NAME) $(ARGS)

.PHONY: down
down:
	${DOCKER} stack rm $(SERVICE_NAME) $(ARGS)

.PHONY: install-dev
install-dev:
	$(VENV)/pip install -r requirements-dev.txt

.PHONY: uninstall-dev
uninstall-dev:
	$(VENV)/pip uninstall -y -r requirements-dev.txt

include Makefile.venv