"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json
import zlib
import base64

from RasaHost import host
app = host.flask
from RasaHost.services import *

@app.route('/models/MemoizationPolicy')
def models_memoization_policy():
    MemoizationPolicyService(host.memoization_policy_path).decode()
    return render_template(
        'models/memoization_policy.html',
        title='MemoizationPolicy',
    )

@app.route('/api/models/MemoizationPolicy/lookups/decode', methods=['POST'])
def api_models_memoization_policy_lookups_decode():
    MemoizationPolicyService(host.memoization_policy_path).decode()
    return jsonify({"result":"ok"})


@app.route('/api/models/MemoizationPolicy/lookups', methods=['GET'])
def api_models_memoization_policy_lookups():
    query = request.args.get('q')
    last_index = int(request.args.get('i', 0))
    result = MemoizationPolicyService(host.memoization_policy_path).find(query, last_index)
    return jsonify({"result": result})
