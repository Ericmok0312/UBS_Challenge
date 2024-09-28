import json
import logging
from flask import request, jsonify
# from routes import app

logger = logging.getLogger(__name__)

snapshots = {}

def walk_map(b_map, me_x, me_y, longest_fly, time, ans):
    if (me_x, me_y) in snapshots.keys():
        if time in snapshots[(me_x, me_y)]:
            return False
    if time == longest_fly:
        return True
    if time + 1 not in b_map[me_y][me_x].keys():
        flag = True
        for val in b_map[me_y][me_x].keys():
            if val > time:
                flag = False
                break
        if flag:
            return True
    if me_x - 1 >= 0 and time + 1 not in b_map[me_y][me_x - 1].keys() and ((time in b_map[me_y][me_x - 1].keys() and "r" not in b_map[me_y][me_x - 1][time]) or time not in b_map[me_y][me_x - 1].keys()):
        ans.append("l")
        if walk_map(b_map, me_x - 1, me_y, longest_fly, time + 1, ans):
            return True
        else:
            ans = ans[0:time]
    if me_x + 1 < len(b_map[me_y]) and time + 1 not in b_map[me_y][me_x + 1].keys() and ((time in b_map[me_y][me_x + 1].keys() and "l" not in b_map[me_y][me_x + 1][time]) or time not in b_map[me_y][me_x + 1].keys()):
        ans.append("r")
        if walk_map(b_map, me_x + 1, me_y, longest_fly, time + 1, ans):
            return True
        else:
            ans = ans[0:time]
    if me_y - 1 >= 0 and time + 1 not in b_map[me_y - 1][me_x].keys() and ((time in b_map[me_y - 1][me_x].keys() and "d" not in b_map[me_y - 1][me_x][time]) or time not in b_map[me_y - 1][me_x].keys()):
        ans.append("u")
        if walk_map(b_map, me_x, me_y - 1, longest_fly, time + 1, ans):
            return True
        else:
            ans = ans[0:time]
    if me_y + 1 < len(b_map) and time + 1 not in b_map[me_y + 1][me_x].keys() and ((time in b_map[me_y + 1][me_x].keys() and "u" not in b_map[me_y + 1][me_x][time]) or time not in b_map[me_y + 1][me_x].keys()):
        ans.append("d")
        if walk_map(b_map, me_x, me_y + 1, longest_fly, time + 1, ans):
            return True
        else:
            ans = ans[0:time]  
    if (me_x, me_y) in snapshots.keys():
        snapshots[(me_x, me_y)].append(time) 
    else:
        snapshots[(me_x, me_y)] = [time]  
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
    while i in range(i, len(data) - 1):
        row = row + 1
        i = i + col + 1
    b_map = []
    for y in range(row):
        temp = []
        for x in range(col):
            temp.append({}) 
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
                if fly not in b_map[y+fly][x].keys():
                    b_map[y+fly][x][fly] = [val]
                else:
                    b_map[y+fly][x][fly].append(val)
                fly = fly + 1
                if fly > longest_fly:
                    longest_fly = fly
        if val == 'u':
            while fly <= y:
                if fly not in b_map[y-fly][x].keys():
                    b_map[y-fly][x][fly] = [val]
                else:
                    b_map[y-fly][x][fly].append(val)
                fly = fly + 1
                if fly > longest_fly:
                    longest_fly = fly
        if val == 'r':
            while fly < col - x:
                if fly not in b_map[y][x+fly].keys():
                    b_map[y][x+fly][fly] = [val]
                else:
                    b_map[y][x+fly][fly].append(val)
                fly = fly + 1
                if fly > longest_fly:
                    longest_fly = fly
        if val == 'l':
            while fly <= x:
                if fly not in b_map[y][x-fly].keys():
                    b_map[y][x-fly][fly] = [val]
                else:
                    b_map[y][x-fly][fly].append(val)
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
    return walk_map(b_map, me_x, me_y, longest_fly, 0, ans), ans

data = "............\n...l........\n..l.........\n*l..........\n............\n............\n............\n............\n............\n............\n............\n............\nuuuuuuuu.uuu\nuuuuuuuu.uuu\nuuuuuuuu.uuu\nuuuuuuuu.uuu\nuuuuuuuu.uuu\nuuuuuuuu.uuu\nuuuuuuuu.uuu\nuuuuuuuu.uuu\nuuuuuuu.uuuu\nuuuuuu.uuuuu\nuuuuu.uuuuuu\nuuuu.uuuuuuu\nuuu.uuuuuuuu\nuu.uuuuuuuuu\nu.uuuuuuuuuu\n.uuuuuuuuuuu\n"

solved, ans = solve(data)
print(solved)
if solved:
    print({"instructions": ans})
else:
    print({"instructions": None})


# @app.route('/dodge', methods=['POST'])
def bullet():
    data = request.get_data(as_text = True)
    print(data)
    print("1")
    solved, ans = solve(data)
    print("2")
    if solved:
        print({"instructions": ans})
    else:
        print('{"instructions": null}')
    if solved:
        return json.dumps({"instructions": ans})
    else:
        return '{"instructions": null}'
