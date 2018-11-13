"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json
from RasaHost import host
app = host.flask
from RasaHost.services import *
from RasaHost.database import *

@app.route("/conversations/<sender_id>/respond")
def rasa_respond(sender_id):
    if 'query' in request.args:
        message = request.args.get('query')
    elif 'q' in request.args:
        message = request.args.get('q')

    output = host.agent.handle_message(message, sender_id=sender_id)
    return jsonify(output)

@app.route("/conversations/<sender_id>/parse")
def rasa_parse(sender_id):
    if 'query' in request.args:
        message = request.args.get('query')
    elif 'q' in request.args:
        message = request.args.get('q')

    output = host.agent.start_message_handling(message, sender_id=sender_id)
    return jsonify(output)

@app.route("/actions", methods = ['GET', 'POST'])
def actions():
    action_call = request.json
    response = host.actionExecutor.run(action_call)
    return jsonify(response)