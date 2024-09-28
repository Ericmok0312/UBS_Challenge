from fastapi import FastAPI
from flask import request
import logging
from routes import app
logger = logging.getLogger(__name__)

app = FastAPI()



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

@app.post('/wordle-game')
def solve_kazuma():
    data = request.get_json()
    monsters = data.get("monsters")
    ans = []
    for i in range(len(monsters)):
        ans.append({"efficiency": kazuma_solver(monsters, 0, false)})
    return ans