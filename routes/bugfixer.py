from collections import defaultdict, deque


import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


def min_hours(data):
    # Initialize result list
    result = []
    
    # Iterate over each test case
    for item in data:
        time = item['time']
        prerequisites = item['prerequisites']
        n = len(time)
        
        # Create adjacency list
        graph = defaultdict(list)
        in_degree = [0] * n
        
        # Build the graph
        for a, b in prerequisites:
            graph[a - 1].append(b - 1)
            in_degree[b - 1] += 1
        
        # Initialize dp array
        dp = [0] * n
        
        # Initialize queue with nodes having in-degree 0
        queue = deque([i for i in range(n) if in_degree[i] == 0])
        
        # Perform topological sorting with dynamic programming
        while queue:
            node = queue.popleft()
            dp[node] = max(dp[node], time[node])
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                dp[neighbor] = max(dp[neighbor], dp[node] + time[neighbor])
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # The minimum hours needed is the maximum hours in the dp array
        result.append(max(dp))
    
    return result



@app.route('/bugfixer/p1', methods=['POST'])
def bugfixerp1():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    result = min_hours(data)

    logging.info("My result :{}".format(result))
    return json.dumps(result)






