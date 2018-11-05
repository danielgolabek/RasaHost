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
        'nlu/index.html',
        title='Nlu',
    )

@app.route('/api/nlu', methods=['GET'])
def api_nlu_list():
    q = request.args.get('q')
    intents = NluService().find_all(q)
    return jsonify(intents)

@app.route('/api/nlu/file/<path>', methods=['GET'])
def api_nlu_get(name):
    intent = NluService().get_by_path(path)
    return jsonify(intent)

@app.route('/api/nlu/file/<path>', methods=['POST'])
def api_nlu_post(path):
    if not request.json["name"]:
        return jsonify({'error': 'Name is required'})

    #newPath = os.path.join(os.path.dirname(path), request.json["name"]  + ".md")
    #if newPath != path and NluService().get_by_path(newPath):
    #    return jsonify({'error': 'File with the name already exits.'})

    NluService().update(path, request.json)
    return jsonify({'result': request.json})

@app.route('/api/nlu/file/', methods=['PUT'])
def api_nlu_put():
    if not request.json["name"]:
        return jsonify({'error': 'Name is required'})

    if NluService().get_by_name(request.json["name"]):
        return jsonify({'error': 'File with the name already exits.'})

    NluService().create(request.json)
    return jsonify({'result': request.json})

@app.route('/api/nlu/file/<path>', methods=['DELETE'])
def api_nlu_delete(path):
    NluService().delete(path)
    return jsonify({'result': 'ok'})

@app.route('/api/nlu/analyze', methods=['GET'])
def api_nlu_analyze():
    return jsonify(AnalyzeService().analyze())

