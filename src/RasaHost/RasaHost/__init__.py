"""
The flask application package.
"""

from os import environ
import os
import sys
import traceback
import logging
from flask import Flask
from flask_socketio import SocketIO

logger = logging.getLogger(__name__)

class RasaHost:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    nlu_path = os.path.join(current_dir, "data/nlu/")
    stories_path = os.path.join(current_dir, "data/stories/")
    domain_path = os.path.join(current_dir, "data/domain.yml")
    memoization_policy_path = os.path.join(current_dir, "models/current/dialogue/policy_1_MemoizationPolicy")
    host = environ.get('SERVER_HOST', '0.0.0.0')
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

    def handle_message(self, *args, **kwargs):
        from RasaHost.services import ConversationsService
        return ConversationsService().handle_message(*args, **kwargs)

    def set_data_path(self, data_dir):
        self.nlu_path = os.path.join(data_dir, "nlu/")
        self.stories_path = os.path.join(data_dir, "stories/")
        self.domain_path = os.path.join(data_dir, "domain.yml")

    def enable_logging(self):
        from RasaHost.logging import enable
        enable()

    def register_channels(self):
        try:
            if self.channels:
                logger.debug("Registering channels")
                import rasa_core
                rasa_core.channels.channel.register(self.channels,
                                                    self.flask,
                                                    self.handle_message,
                                                    route="/webhooks/")
        except:
            e = "\n". join(traceback.format_exception(*sys.exc_info()))
            logger.error(e)

    def run(self):
        import RasaHost.controllers
        self.enable_logging()
        self.register_channels()
        #self.socketio.run(self.flask,self.host, self.port)
        self.flask.run(self.host, self.port)

host = RasaHost()
