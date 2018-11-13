"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json
import os;

from RasaHost import host
app = host.flask
from RasaHost.services import *

@app.route('/stories')
def stories_list():
    return render_template(
        'stories/index.html',
        title='Stories',
    )

@app.route('/api/stories', methods=['GET'])
def api_stories_list():
    q = request.args.get('q')
    stories = StoriesService().find_all(q)
    return jsonify(stories)

@app.route('/api/stories/file/<path>', methods=['GET'])
def api_stories_get(path):
    story = StoriesService().get_by_path(path)
    return jsonify(story)

@app.route('/api/stories/file/<path>', methods=['POST'])
def api_stories_post(path):
    if not request.json["name"]:
        return jsonify({'error': 'Name is required'})
    
    newPath = os.path.join(os.path.dirname(path), request.json['name']  + ".md")
    if path.lower() != newPath.lower() and os.path.exists(newPath):
        return jsonify({'error': 'File with the name already exists'})

    updated_file = StoriesService().update(path, request.json)
    return jsonify({'result': updated_file})

@app.route('/api/stories/file/', methods=['PUT'])
def api_stories_put():
    if not request.json["name"]:
        return jsonify({'error': 'Name is required'})

    if NluService().get_by_name(request.json["name"]):
        return jsonify({'error': 'File with the name already exits.'})

    created_file = StoriesService().create(request.json)
    return jsonify({'result': created_file})

@app.route('/api/stories/file/<path>', methods=['DELETE'])
def api_stories_delete(path):
    NluService().delete(path)
    return jsonify({'result': 'ok'})

@app.route('/api/stories/intentWithUtter', methods=['PUT'])
def api_nlu_add_intent_with_utter_to_domain():
    intent = request.json['name']
    utter = "utter_" + intent
    StoriesService().add_story(intent, utter)
    DomainService().add_utter(utter)
    DomainService().add_action(utter)
    return jsonify({'result': 'ok'})

@app.route('/api/stories/intentWithAction', methods=['PUT'])
def api_nlu_add_intent_with_action_to_domain():
    intent = request.json['name']
    action = "action_" + intent
    StoriesService().add_story(intent, action)
    DomainService().add_action(action)
    return jsonify({'result': 'ok'})