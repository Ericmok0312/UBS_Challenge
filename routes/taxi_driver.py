import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


def solve(data):
   


@app.route('/driver', methods=['POST'])
def digital_colony():
    data = request.get_json()
    ans = []
    for i in len(data):
        ans.append(data[i])
    return json.dumps(ans)
