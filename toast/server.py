import gunicorn.app.base

from .webhook import app
from .config import config

# https://docs.gunicorn.org/en/stable/custom.html

class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def main():
    options = {
        'bind': f'0.0.0.0:{config["toast"]["port"]}'
    }
    StandaloneApplication(app, options=options).run()

if __name__ == "__main__": main()