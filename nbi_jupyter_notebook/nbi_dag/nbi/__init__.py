from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler


def _jupyter_server_extension_paths():
    return [{
        "module": "nbi"
    }]


class HelloWorldHandler(IPythonHandler):
    def get(self):
        self.log(self.settings['headers'])
        self.finish('Hello, world!')


def load_jupyter_server_extension(nbapp):
    nbapp.log.info("nbi enabled")
    web_app = nbapp.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/hello')
    web_app.add_handlers(host_pattern, [(route_pattern, HelloWorldHandler)])
