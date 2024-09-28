from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

def parse_input(tables):
    """Parse the input markdown tables into structured data."""
    lab_data = []
    for table in tables:
        rows = table.strip().split("\n")[2:]  # Skip headers
        lab_info = []
        for row in rows:
            cells = row.split("|")[1:-1]  # Remove leading and trailing pipes
            lab_info.append({
                "lab": int(cells[0].strip()),
                "cell_counts": [int(i) for i in (cells[1].strip().split(" "))],
                "increment": cells[2].strip(),
                "condition": list(map(int, cells[3].strip().split()))
            })
        lab_data.append(lab_info)
    return lab_data

data =  

@app.route('/lab_work', methods=['POST'])
def lab_work():
    input_data = request.get_json()
    tables = input_data.get("tables")
    lab_data = parse_input(tables)
    result = simulate_labs(lab_data)
    return jsonify(result)