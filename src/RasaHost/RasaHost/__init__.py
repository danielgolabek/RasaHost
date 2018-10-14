"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import RasaHost.controllers

from RasaHost.services import LoggingService
LoggingService().initialize()
