#!/usr/bin/env bash

# Required when the 'auth_state' flag is enabled
# means that the 'hub/setup_jup_crypt_secret.sh script
# must be sources before the stack is deployed
# https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html
export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)

# https://jupyterhub.readthedocs.io/en/stable/getting-started/security-basics.html#generating-and-storing-as-an-environment-variable
# Used by the proxy and JupyterHub for authentication
export CONFIGPROXY_AUTH_TOKEN=$(openssl rand -hex 32)