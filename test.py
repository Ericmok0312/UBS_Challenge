from collections import defaultdict,deque
def solve(data):
    dependencies = data['prerequisites']
    durations = data['time']
    tasks = list(range(1, len(data)+1))

        # Step 1: Build the graph and in-degrees
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    for u, v in dependencies:
        graph[u].append(v)
        in_degree[v] += 1

    # Step 2: Topological Sort
    queue = deque([task for task in tasks if in_degree[task] == 0])
    topological_order = []
    
    while queue:
        node = queue.popleft()
        topological_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Step 3: Calculate earliest start and finish times
    earliest_start = {task: 0 for task in tasks}
    earliest_finish = {task: 0 for task in tasks}
    
    for node in topological_order:
        earliest_finish[node] = earliest_start[node] + durations[node - 1]
        for neighbor in graph[node]:
            earliest_start[neighbor] = max(earliest_start.get(neighbor,0), earliest_finish.get(node,0))

    # Step 4: Calculate latest start and finish times
    latest_finish = {task: float('inf') for task in tasks}
    latest_start = {task: float('inf') for task in tasks}
    
    for task in reversed(topological_order):
        if not graph[task]:  # If no successors
            latest_finish[task] = earliest_finish[task]
            latest_start[task] = latest_finish[task] - durations[task - 1]
        for neighbor in graph:
            if task in graph[neighbor]:  # If task is a predecessor
                latest_finish[task] = min(latest_finish[task], latest_start[neighbor])
                latest_start[task] = latest_finish[task] - durations[task - 1]

    # Step 5: Identify the critical path
    critical_path = []
    for task in tasks:
        if earliest_start[task] == latest_start[task]:
            critical_path.append(task)

    return critical_path




data = {
        "time": [1, 2, 3, 4, 5],
        "prerequisites": [(1,2),(3,4),(2,5),(4,5)]
    }
print(solve(data))
#print(solve(data))
