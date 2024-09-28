import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


class Block:
    def __init__(self,x,y,width=1,length=1):
        self.top_left = [x,y]
        self.x = x
        self.y = y
        self.width = width
        self.length = length



def solve(data):



    mp = data["board"]
    move = data["moves"]
    location = {}

    for j in range(20):
        cur_y = int(j / 4) #row
        cur_x = int(j % 4) #column
        if(not(mp[j] == "@")):
            if not(mp[j] in location):
                location[mp[j]] = Block(cur_x, cur_y)
            else:
                location[mp[j]].width = max(location[mp[j]].width, cur_x - location[mp[j]].x + 1)
                location[mp[j]].length = max(location[mp[j]].length, cur_y-location[mp[j]].y + 1)



    
    for i in range(int(len(move)/2)):
        dir = move[2*i+1]
        if (dir == "N"):
            location[move[2*i]].y-=1
        elif(dir == "E"):
            location[move[2*i]].x+=1
        elif(dir == "S"):
            location[move[2*i]].y+=1
        else:
            location[move[2*i]].x-=1


    location_list = "@"*20

    for key,value in location.items():
        for i in range(int(value.length)):
            for j in range(int(value.width)):
                loc = int(value.x+j+(value.y+i)*4)
                location_list = location_list[:loc] + key + location_list[loc+1:]

    return location_list



@app.route('/klotski', methods=['POST'])
def klotski():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    print(data)


    ans = []
    for i in range(len(data)):
        ans.append(solve(data[i]))
    #ans holds result



    return json.dumps(ans)
