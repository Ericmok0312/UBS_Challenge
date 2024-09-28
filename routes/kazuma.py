from flask import request
import logging
from routes import app
import json

logger = logging.getLogger(__name__)

def kazuma_solver(monsters, efficiency, can_shoot):
    if (len(monsters)==0):
        return efficiency
    else:
        if(not(can_shoot)):
            res1 = kazuma_solver(monsters[1:], efficiency-monsters[0], not can_shoot) # spell
            res2 = kazuma_solver(monsters[1:], efficiency, can_shoot)
            res3 = -999
        elif(can_shoot):
            res1 = kazuma_solver(monsters[2:], efficiency+monsters[0], not can_shoot) #shoot 
            res2 = kazuma_solver(monsters[1:], efficiency-monsters[0], can_shoot)
            res3 = kazuma_solver(monsters[1:], efficiency, can_shoot)
    return max(res1, res2,res3)

@app.route('/efficient-hunter-kazuma', methods = ['POST'])
def solve_kazuma():
    data = request.get_json()

    ans = []
    for i in range(len(data)):
        ans.append({"efficiency": kazuma_solver(data[i].get("monsters"), 0, False)})
        json_response = json.dumps(ans)
    return json_response, 200, {'Content-Type': 'application/json; charset=utf-8'}