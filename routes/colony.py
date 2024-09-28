import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


def solve(data):
    generation = data["generations"]
    colony = data["colony"]
#     n = len(colony)
#     dif = int(colony[0]) - int(colony[-1])
#     weight = 0
#     for i in colony:
#         weight += int(i)
#     for i in range (generation):
#         weight = weight + ((n - 1) * weight + dif) - 10 * n
#         n = 2 * n - 1
#     return weight
    
# print(solve({ "generations": 2, "colony": "914" }))
    
    result = dict()
    for gen in range(generation+1):
        weight = 0
        for i in range(len(colony)-1):
            left = colony[i]
            right = colony[i+1]
            if not (left, right) in result:
                result[(left,right)]  =  int((10+int(left)-int(right))%10)

        for i in range(len(colony)):
            weight+=int(colony[i])

        if(gen < generation):
            next_colon = ""
            for i in range(len(colony)-1):
                next_colon += colony[i]
                next_colon += str(result[(colony[i], colony[i+1])]+weight)[-1]
            
            next_colon += colony[-1]
            colony = next_colon
    return str(weight)


@app.route('/digital-colony', methods=['POST'])
def digital_colony():
    data = request.get_json()
    ans = []
    for i in range(len(data)):
        ans.append(solve(data[i]))
    return json.dumps(ans)