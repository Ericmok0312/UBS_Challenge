import json
import logging

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)


@app.route('/coolcodehack', methods=['POST'])
def hack():
    username = "franklin"
    password = "Ubs1234!"
    return jsonify({
        "username": username,
        "password": password
    })