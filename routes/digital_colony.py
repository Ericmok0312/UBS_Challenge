import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


import numpy as np

def solve_optimized(data):
    generations = data["generations"]
    colony_str = data["colony"]
    colony = np.array([int(c) for c in colony_str])  # Use NumPy array
    n = len(colony)
    result = np.zeros((10, 10), dtype=int)  # Pre-compute weights

    for i in range(10):
        for j in range(10):
            result[i, j] = (10 + i - j) % 10

    for gen in range(generations + 1):
        weight = np.sum(colony)  # Efficient sum using NumPy

        if gen < generations:
            next_colony = []
            for i in range(n - 1):
                next_colony.append(colony[i])
                next_colony.append(result[colony[i], colony[i+1]] + weight)  #Efficient lookup
            next_colony.append(colony[-1])
            colony = np.array(next_colony)
            n = len(colony)

    return str(weight)


@app.route('/digital-colony', methods=['POST'])
def digital_colony():
    data = request.get_json()
    ans = []
    for i in len(data):
        ans.append(data[i])
    return json.dumps(ans)
