import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)



def solve(data):
    tb = [[0]*len(data)]*3
    tb[0][0] = -data[0] #spell
    tb[1][0] = 0
    tb[2][0] = 0
    spelled = False

    for i in range(len(data)):
        



@app.route('/efficient-hunter-kazuma', methods=['POST'])
def evaluate():
    data = request.get_json()

