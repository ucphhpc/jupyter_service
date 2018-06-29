import argparse
import socket
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--hub-url', dest='hub_url',
                    default='http://127.0.0.1:8888')
parser.add_argument('--mount-url', dest='mount_url',
                    default='/hub/mount')
parser.add_argument('--auth-url', dest='auth_url',
                    default='/hub/login')
parser.add_argument('--spawn-url', dest='spawn_url',
                    default='/hub/spawn')
parser.add_argument('--docker-image', dest='docker_image',
                    default='jupyterhub/singleuser:0.8.1')


def main(args):
    request_user = 'mountuser'
    home = "/opt/{}".format(request_user)
    ssh_dir = "{}/.ssh".format(home)

    f_path = "{}/id_rsa".format(ssh_dir)

    with open(f_path, 'r') as file:
        private_key = "".join(file.readlines())

    # volume
    ssh_host_target = socket.gethostname()

    # Auth requests
    user_cert = '/C=DK/ST=NA/L=NA/O=NBI/OU=NA/CN=Name' \
                '/emailAddress=mail@sdfsf.com'

    mount_dict = {'HOST': 'DUMMY', 'USERNAME': request_user,
                  'PATH': ''.join(['@', ssh_host_target, ':']),
                  'PRIVATEKEY': private_key}

    auth_header = {'Remote-User': user_cert}

    mount_header = {'Remote-User': user_cert,
                    'Mount': str(mount_dict)}

    with requests.Session() as session:
        try:
            session.get(args.hub_url)
        except (requests.ConnectionError, requests.exceptions.InvalidSchema):
            print("{} can't be reached".format(args.hub_url))
            exit(-1)

        # Auth
        session.get(args.hub_url + args.auth_url, headers=auth_header)
        # Mount
        session.post(args.hub_url + args.mount_url, headers=mount_header)
        payload = {
            'dockerimage': args.docker_image
        }

        # Spawn
        session.post(args.hub_url + args.spawn_url, payload=payload, headers=auth_header)


if __name__ == '__main__':
    main(parser.parse_args())
