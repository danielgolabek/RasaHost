"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json

from RasaHost import host
app = host.flask
from RasaHost.services import *

@app.route('/intents')
def intents_list():
    return render_template(
        'intents/intents.html',
        title='Intents',
    )

@app.route('/api/intents', methods=['GET'])
def api_intents_list():
    q = request.args.get('q')
    intents = IntentsService().find_all(q)
    return jsonify(intents)

@app.route('/api/intent/<name>', methods=['GET'])
def api_intents_get(name):
    intent = IntentsService().get_by_name(name)
    return jsonify(intent)

@app.route('/api/intent/<name>', methods=['POST'])
def api_intents_post(name):
    updated_intent = request.json
    if name.lower() != updated_intent['name'].lower():
        existing_intned = IntentsService().get_by_name(updated_intent['name'].lower())
        if existing_intned:
            return jsonify({'error': 'Intent with the name already exits.'})
    
    IntentsService().update(name, updated_intent)
    return jsonify({'result': updated_intent})

@app.route('/api/intent/<name>', methods=['PUT'])
def api_intents_put(name):
    existing_intned = IntentsService().get_by_name(name)
    if existing_intned:
        return jsonify({'error': 'Intent with the name already exits.'})

    new_intent = request.json
    IntentsService().update(name, new_intent)
    return jsonify({'result': new_intent})

@app.route('/api/intent/<name>', methods=['DELETE'])
def api_intents_delete(name):
    IntentsService().delete(name)
    return jsonify({'result': 'ok'})

intents_warnings = []
domain_model = DomainService().get_model()
intents_model = IntentsService().get_model()
for file in intents_model:
    for intent in file.intents:
        existe_in_domain = any([x for x in domain_model.intents if x.name == intent.name])
        if not existe_in_domain:
            intents_warnings.append("")
