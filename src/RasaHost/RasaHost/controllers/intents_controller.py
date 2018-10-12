"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json

from RasaHost import app
from RasaHost.dialogues import *

@app.route('/intents')
def intents_list():
    return render_template(
        'intents/intents.html',
        title='Intents',
    )

@app.route('/intents/create')
def intents_create():
    return render_template(
        'intents/intent.html',
        title='Intent',
        model={'name': '', 'text': ''},
        model_json=json.dumps({'name': '', 'text': ''})
    )

@app.route('/intents/edit/<name>', methods=['GET'])
def intents_edit(name):
    intent = IntentsService().get_by_name(name)
    return render_template(
        'intents/intent.html',
        title='Intent',
        model=intent,
        model_json=json.dumps(intent)
    )

@app.route('/api/intents', methods=['GET'])
def api_intents_list():
    q = request.args.get('q')
    intents = IntentsService().find_all(q)
    return jsonify(intents)

@app.route('/api/intents/<name>', methods=['GET'])
def api_intents_get(name):
    intent = IntentsService().get_by_name(name)
    return jsonify(intent)

@app.route('/api/intents/<name>', methods=['POST'])
def api_intents_post(name):
    updated_intent = request.json
    if name.lower() != updated_intent['name'].lower():
        existing_intned = IntentsService().get_by_name(name)
        if existing_intned:
            return jsonify({'error': 'Intent with the name already exits.'})
    
    IntentsService().update(name, updated_intent)
    return jsonify({'result': updated_intent})

@app.route('/api/intents/<name>', methods=['PUT'])
def api_intents_put(name):
    existing_intned = IntentsService().get_by_name(name)
    if existing_intned:
        return jsonify({'error': 'Intent with the name already exits.'})

    new_intent = request.json
    IntentsService().update(name, new_intent)
    return jsonify({'result': new_intent})
