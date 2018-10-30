"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json

from RasaHost import host
app = host.flask
from RasaHost.services import *

@app.route('/nlu')
def nlu_list():
    return render_template(
        'intents/intents.html',
        title='Intents',
    )

@app.route('/api/nlu', methods=['GET'])
def api_nlu_list():
    q = request.args.get('q')
    intents = NluService().find_all(q)
    return jsonify(intents)

@app.route('/api/nlu/item/<name>', methods=['GET'])
def api_nlu_get(name):
    intent = NluService().get_by_name(name)
    return jsonify(intent)

@app.route('/api/nlu/item/<name>', methods=['POST'])
def api_nlu_post(name):
    updated_intent = request.json
    if name.lower() != updated_intent['name'].lower():
        existing_intned = NluService().get_by_name(updated_intent['name'].lower())
        if existing_intned:
            return jsonify({'error': 'Intent with the name already exits.'})
    
    NluService().update(name, updated_intent)
    return jsonify({'result': updated_intent})

@app.route('/api/nlu/item/<name>', methods=['PUT'])
def api_nlu_put(name):
    existing_intned = NluService().get_by_name(name)
    if existing_intned:
        return jsonify({'error': 'Intent with the name already exits.'})

    new_intent = request.json
    NluService().update(name, new_intent)
    return jsonify({'result': new_intent})

@app.route('/api/nlu/item/<name>', methods=['DELETE'])
def api_nlu_delete(name):
    NluService().delete(name)
    return jsonify({'result': 'ok'})

@app.route('/api/nlu/addIntentToDomain', methods=['POST'])
def api_nlu_add_intent_to_domain():
    intent = request.json['name']
    domainModel = DomainService().get_model()
    domainModel.add_intent(intent)
    DomainService().save_model(domainModel)
    return jsonify({'result': 'ok'})

@app.route('/api/nlu/addStoryWithUtter', methods=['POST'])
def api_nlu_add_intent_to_domain():
    intent = request.json['name']
    return jsonify({'result': 'ok'})

@app.route('/api/nlu/analyze', methods=['GET'])
def api_nlu_analyze():
    return jsonify(AnalyzeService().analyze())

