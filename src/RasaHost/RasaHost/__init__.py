"""
The flask application package.
"""

from os import environ
import os
from flask import Flask
from flask_socketio import SocketIO
from RasaHost.logging import enable

class RasaHost:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    nlu_path = os.path.join(current_dir, "data/intents/")
    stories_path = os.path.join(current_dir, "data/stories/")
    domain_path = os.path.join(current_dir, "data/domain.yml")
    host = environ.get('SERVER_HOST', 'localhost')
    port = 5555
    agent = None
    actionExecutor = None

    try:
        port = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        port = 5555

    def __init__(self):
        self.flask = Flask(__name__)
        #self.socketio = SocketIO(self.flask)

    def set_data_path(self, data_dir):
        self.nlu_path = os.path.join(data_dir, "nlu/")
        self.stories_path = os.path.join(data_dir, "stories/")
        self.domain_path = os.path.join(data_dir, "domain.yml")

    def enable_logging(self):
        enable()

    def run(self):
        import RasaHost.controllers
        from RasaHost.services import LoggingService
        self.enable_logging()
        #self.socketio.run(self.flask,self.host, self.port)
        self.flask.run(self.host, self.port)

host = RasaHost()
