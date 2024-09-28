from flask import Flask, request, jsonify
import itertools

from routes import app

# Define the subway map as subway lines with their ordered stations
# and travel time between adjacent stations for each line
SUBWAY_LINES = {
    "Tokyo Metro Ginza Line": ["Asakusa", "Tawaramachi", "Inaricho", "Omotesando", "Ichigaya", "Oji", "Nakano"],
    "Line2": ["Yoyogi-uehara", "Meiji-jingumae", "Oji", "Takebashi", "Tameike-sanno", "Shimbashi", "Minami-asagaya"],
    # Adding 'Line3' with 'Tokyo' station and connections for demonstration
    "Line3": ["Tokyo", "Shinjuku", "Shibuya", "Yoyogi-uehara"]
}

# Travel time between adjacent stations for each line in minutes
TRAVEL_TIME_PER_LINE = {
    "Tokyo Metro Ginza Line": 2,
    "Line2": 3,
    "Line3": 4  # Hypothetical travel time
}

# Function to build adjacency list from subway lines
def build_graph(subway_lines, travel_time_per_line):
    graph = {}
    for line, stations in subway_lines.items():
        time = travel_time_per_line[line]
        for i in range(len(stations)):
            if stations[i] not in graph:
                graph[stations[i]] = []
            if i > 0:
                prev_station = stations[i-1]
                graph[stations[i]].append((prev_station, time))
            if i < len(stations) -1:
                next_station = stations[i+1]
                graph[stations[i]].append((next_station, time))
    return graph

# Function to compute all-pairs shortest paths using Floyd-Warshall
def floyd_warshall(stations, graph):
    INF = float('inf')
    dist = {s: {t: INF for t in stations} for s in stations}
    for s in stations:
        dist[s][s] = 0
    for s in graph:
        for neighbor, time in graph[s]:
            dist[s][neighbor] = min(dist[s][neighbor], time)
    for k in stations:
        for i in stations:
            for j in stations:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

# Function to find the optimal path using backtracking
def find_optimal_path(start, locations, dist, time_limit):
    best = {
        'satisfaction': -1,
        'path': []
    }

    def backtrack(current, path, total_time, total_satisfaction, visited):
        # Try to return to start
        travel_back = dist[current].get(start, float('inf'))
        if travel_back != float('inf') and total_time + travel_back <= time_limit:
            candidate_path = path + [start]
            if total_satisfaction > best['satisfaction']:
                best['satisfaction'] = total_satisfaction
                best['path'] = candidate_path
        # Explore further stations
        for station in locations:
            if station not in visited and station != start:
                travel_time = dist[current].get(station, float('inf'))
                if travel_time == float('inf'):
                    continue
                min_time = locations[station][1]
                new_total_time = total_time + travel_time + min_time
                # Time to return to start after visiting this station
                travel_back_from_station = dist[station].get(start, float('inf'))
                if new_total_time + travel_back_from_station > time_limit:
                    continue
                # Update satisfaction
                new_total_satisfaction = total_satisfaction + locations[station][0]
                # Mark as visited
                visited.add(station)
                # Recurse
                backtrack(station, path + [station], new_total_time, new_total_satisfaction, visited)
                # Unmark
                visited.remove(station)

    # Initialize
    initial_time = locations[start][1]  # Should be 0 as per problem
    backtrack(start, [start], initial_time, 0, set([start]))
    return best

# Build the subway graph once at startup
SUBWAY_GRAPH = build_graph(SUBWAY_LINES, TRAVEL_TIME_PER_LINE)
ALL_STATIONS = list(SUBWAY_GRAPH.keys())
# Compute all-pairs shortest paths
ALL_PAIRS_DIST = floyd_warshall(ALL_STATIONS, SUBWAY_GRAPH)

@app.route('/tourist', methods=['POST'])
def tourist():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    # Extract input
    locations = data.get("locations")
    starting_point = data.get("startingPoint")
    time_limit = data.get("timeLimit")
    if locations is None or starting_point is None or time_limit is None:
        return jsonify({"error": "Missing required fields"}), 400
    if starting_point not in locations:
        return jsonify({"error": "Starting point not in locations"}), 400
    # Ensure starting point has [0,0] as per problem
    if locations[starting_point] != [0, 0]:
        locations[starting_point] = [0, 0]
    # Validate that all stations in locations exist in the subway map
    missing_stations = [station for station in locations if station not in SUBWAY_GRAPH]
    if missing_stations:
        return jsonify({
            "error": f"The following stations are missing from the subway map: {', '.join(missing_stations)}"
        }), 400
    # Compute the optimal path
    optimal = find_optimal_path(starting_point, locations, ALL_PAIRS_DIST, time_limit)
    if optimal['satisfaction'] == -1:
        # Only possible path is start and end without visiting any station
        return jsonify({"path": [starting_point, starting_point], "satisfaction": 0})
    return jsonify({
        "path": optimal['path'],
        "satisfaction": optimal['satisfaction']
    })
