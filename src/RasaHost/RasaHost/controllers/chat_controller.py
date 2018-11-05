"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json

from RasaHost import host
app = host.flask
from RasaHost.services import *

@app.route('/chat')
def chat():
    return render_template(
        'chat/index.html',
        title='Chat',
    )