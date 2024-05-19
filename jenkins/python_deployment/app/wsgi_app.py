from gunicorn.app.base import BaseApplication
from app import app as flask_app

class FlaskGunicornApp(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application

if __name__ == "__main__":
    options = {
            'bind': '0.0.0.0:8989',  
            'workers': 1
    }

    FlaskGunicornApp(flask_app, options).run()
