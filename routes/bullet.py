import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def walk_map(b_map, me_x, me_y, longest_fly, time, ans, instruct_no):
    if time == longest_fly:
        return True
    if time + 1 not in b_map[me_y][me_x]:
        flag = False
        for val in b_map[me_y][me_x]:
            if val > time:
                flag = True
                break
        if not flag:
            return True
    if me_x - 1 >= 0 and time + 1 not in b_map[me_y][me_x - 1] and time not in b_map[me_y][me_x - 1]:
        ans.append("l")
        instruct_no += 1
        if walk_map(b_map, me_x - 1, me_y, longest_fly, time + 1, ans, instruct_no):
            return True
        else:
            ans = ans[0:instruct_no]
    if me_x + 1 < len(b_map[me_y]) and time + 1 not in b_map[me_y][me_x + 1] and time not in b_map[me_y][me_x + 1]:
        ans.append("r")
        instruct_no += 1
        if walk_map(b_map, me_x + 1, me_y, longest_fly, time + 1, ans, instruct_no):
            return True
        else:
            ans = ans[0:instruct_no]
    if me_y - 1 >= 0 and time + 1 not in b_map[me_y - 1][me_x] and time not in b_map[me_y - 1][me_x]:
        ans.append("u")
        instruct_no += 1
        if walk_map(b_map, me_x, me_y - 1, longest_fly, time + 1, ans, instruct_no):
            return True
        else:
            ans = ans[0:instruct_no]
    if me_y + 1 < len(b_map) and time + 1 not in b_map[me_y + 1][me_x] and time not in b_map[me_y + 1][me_x]:
        ans.append("d")
        instruct_no += 1
        if walk_map(b_map, me_x, me_y + 1, longest_fly, time + 1, ans, instruct_no):
            return True
        else:
            ans = ans[0:instruct_no]        
    return False

def solve(data):
    row = 0
    col = 0
    i = 0
    while data[i] != '\n':
        col = col + 1
        i = i + 1
    row = row + 1
    i = i + 1
    for i in range(i, len(data) - 1):
        row = row + 1
        i = i + col + 1
    b_map = []
    for y in range(row):
        temp = []
        for x in range(col):
            temp.append([]) 
        b_map.append(temp)
    x = 0
    y = 0
    longest_fly = 0
    for val in data:
        fly = 0
        if val == '\n':
            continue
        if val == 'd':
            while fly < row - y:
                b_map[y+fly][x].append(fly)
                fly = fly + 1
                if fly > longest_fly:
                    longest_fly = fly
        if val == 'u':
            while fly <= y:
                b_map[y-fly][x].append(fly)
                fly = fly + 1
                if fly > longest_fly:
                    longest_fly = fly
        if val == 'r':
            while fly < col - x:
                b_map[y][x+fly].append(fly)
                fly = fly + 1
                if fly > longest_fly:
                    longest_fly = fly
        if val == 'l':
            while fly <= x:
                b_map[y][x-fly].append(fly)
                fly = fly + 1
                if fly > longest_fly:
                    longest_fly = fly
        if val == '*':
            me_x = x
            me_y = y
        x = x + 1
        if x >= col:
            x = 0
            y = y + 1
    
    ans = []
    return walk_map(b_map, me_x, me_y, longest_fly, 0, ans, 0), ans

@app.route('/dodge', methods=['POST'])
def bullet():
    data = request.get_data(as_text = True)
    logging.info("data sent for evaluation {}".format(data))
    solved, ans = solve(data)
    if solved:
        json_response = json.dumps({"instructions": ans})
        return json_response, 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        json_response = json.dumps({"instructions": None})
        return json_response, 200, {'Content-Type': 'application/json; charset=utf-8'}