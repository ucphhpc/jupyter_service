from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import os

def _jupyter_server_extension_paths():
    return [{
        "module": "nbi"
    }]


class HelloWorldHandler(IPythonHandler):
    def get(self):
        print("Hello")
        mount = self.request.headers.get('Mount')
        if mount is not None:
            print(mount)
        self.redirect('/tree')


def load_jupyter_server_extension(nbapp):
    nbapp.log.info("nbi enabled")
    web_app = nbapp.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/')
    web_app.add_handlers(host_pattern, [(route_pattern, HelloWorldHandler)])
