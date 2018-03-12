import docker
import requests

jhub_url = "http://127.0.0.1:8000"


def test_swarm(hu):
    """Test that the jupyterhub and nginx services are launched correctly
    and that the hub spawns a notebook image upon a authenticated spawn
    request """
    client = docker.from_env()
    services_before_spawn = client.services.list()

    user_cert = '/C=DK/ST=NA/L=NA/O=NBI/OU=NA/CN=Rasmus ' \
                'Munk/emailAddress=rasmus.munk@nbi.ku.dk'
    # Auth header
    auth_header = {'Remote-User': user_cert}

    with requests.Session as s:
        login_resp = s.get(
            jhub_url + "/hub/login", headers=auth_header
        )
        assert login_resp.status_code == 200

        spawn_form_resp = s.get(jhub_url + "/hub/spawn")
        assert spawn_form_resp.status_code == 200
        assert 'Select a notebook image' in spawn_form_resp.text
        payload = {
            'dockerimage': 'nielsbohr/base-notebook'
        }
        spawn_resp = s.post(jhub_url + "/hub/spawn", data=payload)
        assert spawn_resp.status_code == 200

        attempts = 0
        spawned_services = set()
        while not len(spawned_services) > 0 and attempts < 15:
            services_after_spawn = client.services.list()
            spawned_services = (set(services_after_spawn)
                                - set(services_before_spawn))
            attempts += 1
