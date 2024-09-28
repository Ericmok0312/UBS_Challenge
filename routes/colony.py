import json
import logging

from flask import request, jsonify

from routes import app

from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Precompute signature for all possible (a, b) pairs
signature = [[0 for _ in range(10)] for _ in range(10)]
for a in range(10):
    for b in range(10):
        if a > b:
            signature[a][b] = a - b
        elif a < b:
            signature[a][b] = 10 - (b - a)
        else:
            signature[a][b] = 0

@dataclass
class ColonyRequestItem:
    generations: int
    colony: str

def parse_request(data):
    if not isinstance(data, list):
        raise ValueError("Input data must be a JSON array.")
    if len(data) != 2:
        raise ValueError("Input array must contain exactly 2 items.")
    items = []
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {idx} is not a JSON object.")
        if 'generations' not in item or 'colony' not in item:
            raise ValueError(f"Item at index {idx} must contain 'generations' and 'colony' fields.")
        generations = item['generations']
        colony = item['colony']
        if not isinstance(generations, int) or generations < 0:
            raise ValueError(f"'generations' in item at index {idx} must be a non-negative integer.")
        if not isinstance(colony, str) or not colony.isdigit() or not (1 <= len(colony) <= 10):
            raise ValueError(f"'colony' in item at index {idx} must be a string of digits (length 1 to 10).")
        items.append(ColonyRequestItem(generations=generations, colony=colony))
    return items

@app.route('/digital-colony', methods=['POST'])
def digital_colony():
    try:
        data = request.get_json()
        items = parse_request(data)
    except (ValueError, json.JSONDecodeError) as e:
        return jsonify({"error": str(e)}), 400

    responses = []
    for item in items:
        generations = item.generations
        colony_str = item.colony

        # Initialize pair counts
        counts = [[0 for _ in range(10)] for _ in range(10)]
        for i in range(len(colony_str) - 1):
            a = int(colony_str[i])
            b = int(colony_str[i + 1])
            counts[a][b] += 1

        # Initialize weight W
        sum_a = 0
        for a in range(10):
            for b in range(10):
                sum_a += counts[a][b] * a
        last_digit = int(colony_str[-1]) if colony_str else 0
        W = sum_a + last_digit

        # Simulate generations
        for _ in range(generations):
            W_mod = W % 10
            sum_new_digits = 0
            # Calculate sum_new_digits
            for a in range(10):
                for b in range(10):
                    c = counts[a][b]
                    if c > 0:
                        s = signature[a][b]
                        new_digit = (W_mod + s) % 10
                        sum_new_digits += c * new_digit
            W += sum_new_digits

            # Update counts
            new_counts = [[0 for _ in range(10)] for _ in range(10)]
            for a in range(10):
                for b in range(10):
                    c = counts[a][b]
                    if c > 0:
                        s = signature[a][b]
                        new_digit = (W_mod + s) % 10
                        new_counts[a][new_digit] += c
                        new_counts[new_digit][b] += c
            counts = new_counts

        responses.append(str(W))

    return jsonify(responses), 200
