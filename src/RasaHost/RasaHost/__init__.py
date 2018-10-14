"""
The flask application package.
"""

from os import environ
HOST = environ.get('SERVER_HOST', 'localhost')
try:
    PORT = int(environ.get('SERVER_PORT', '5555'))
except ValueError:
    PORT = 5555

from flask import Flask
app = Flask(__name__)

from flask_socketio import SocketIO
socketio = SocketIO(app)

from RasaHost.services import LoggingService
LoggingService().initialize()

import RasaHost.controllers

def run():
    socketio.run(app,HOST, PORT)

