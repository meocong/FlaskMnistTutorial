import gunicorn
import gunicorn.app.base
from server import app

class GunicornServer(gunicorn.app.base.BaseApplication):
    def __init__(self, app, **kwargs):
        self.application = app
        self.options = kwargs
        super(GunicornServer, self).__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    gunicorn_server = GunicornServer(app, bind="localhost:8080", workers=1, threads=1, timeout=20, graceful_timeout=5, max_requests_jitter=40, max_requests=40, keepalive=10, worker_class='gevent', worker_connections=1000, preload=True)
    gunicorn_server.run()
    
