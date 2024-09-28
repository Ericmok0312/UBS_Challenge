from flask import Flask, request, jsonify
import json
import re
import numpy as np

app = Flask(__name__)
# from routes import app

def parse_input(table):
    """Parse the input markdown tables into structured data."""
    rows = table.split("\n")[2:]  # Skip headers
    lab_info = []
    for row in rows:
        cells = row.split("|")[1:-1]  # Remove leading and trailing pipes
        lab_info.append({
            "lab": int(cells[0].strip()),
            "cell_counts": np.array([int(i) for i in (cells[1].strip().split(" "))]),
            "increment": cells[2].strip(),
            "condition": list(map(int, cells[3].strip().split()))
        })
    return lab_info


def simulate_labs(lab_data):
    for data in lab_data:
        data['cell_counts'] *= 2
        mask = data['cell_counts'] % data['condition'][0] != 0
        np.append(lab_data[data['condition'][mask]["cell_counts"]], data['cell_counts'])
        print(data)
        break
        

data =  "|Lab | Cell counts             | Increment     | Condition |\n|----|-------------------------|---------------|-----------|\n|0   | 98 89 52                | count * 2     | 5  6 1    |\n|1   | 57 95 80 92 57 78       | count * 13    | 2  2 6    |\n|2   | 82 74 97 75 51 92 83    | count + 5     | 19 7 5    |\n|3   | 97 88 51 68 68 76       | count + 6     | 7  0 4    |\n|4   | 63                      | count + 1     | 17 0 1    |\n|5   | 94 91 51 63             | count + 4     | 13 4 3    |\n|6   | 61 54 94 71 74 68 98 83 | count + 2     | 3  2 7    |\n|7   | 90 56                   | count * count | 11 3 5    |"
lab_data = parse_input(data)
print(lab_data)
print(simulate_labs(lab_data))

# @app.route('/lab_work', methods=['POST'])
def lab_work():
    data = request.get_data(as_text = True)
    lab_data = parse_input(data)
    result = simulate_labs(lab_data)
    return jsonify(result)