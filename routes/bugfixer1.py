import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


def solve(data):
    prerequisites = data['prerequisites']
    times = data['times']
    n = len(data)

    graph = defaultdict(list)
    in_degree = defaultdict(int)
    all_nodes = set(range(1, n + 1)) # Node numbers are 1-based

    for u, v in prerequisites:
        graph[u + 1].append(v + 1)  # Adjust for 1-based indexing
        in_degree[v + 1] += 1
        

    # 2. Topological Sort (Kahn's Algorithm):
    queue = [node for node in all_nodes if in_degree[node] == 0]
    topological_order = []
    while queue:
        node = queue.pop(0)
        topological_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Cycle detection:
    if len(topological_order) != n:
        return -1

    # 3. Critical Path Analysis (with durations):
    completion_times = {}
    for node in topological_order:
        max_predecessor_time = 0
        for predecessor in graph[node]:
            max_predecessor_time = max(max_predecessor_time, completion_times[predecessor])
        completion_times[node] = max_predecessor_time + times[node - 1] #times list is 0-based

    return max(completion_times.values())


    
    
    


@app.route('/driver', methods=['POST'])
def digital_colony():
    data = request.get_json()
    ans = []
    for i in len(data):
        ans.append(solve(data[i]))
    return json.dumps(ans)
