from fastapi import FastAPI
from flask import request
import logging
from routes import app
logger = logging.getLogger(__name__)

app = FastAPI()



result = []

def kazuma_solver(monsters):
    if len(monsters) == 1:
        result.append(0)
        return 0
    if len(monsters) == 2:
        if monsters[0] < monsters[1]:
            result.append(monsters[1] - monsters[0])
            return 2
        else:
            result.append(0)
            return 0
    cooldown = kazuma_solver(monsters[1:])
    if cooldown == 0 :
        if monsters[0] < monsters[1]:
            result.append(monsters[1] - monsters[0])
            return 2
        else:
            result.append(0)
            return cooldown - 1
    elif monsters[1] - monsters[0] > result[-1]:
        result[-1] = monsters[1] - monsters[0]
        return 2
    else:
        return cooldown - 1    

# monsters = [1, 6, 17, 11, 12, 14]
# kazuma_solver(monsters)
# efficiency = sum(result)
# print(efficiency)

@app.post('/wordle-game')
def solve_kazuma():
    data = request.get_json()
    monsters = data.get("monsters")
    kazuma_solver(monsters)
    efficiency = sum(result)
    return {"efficiency": efficiency}