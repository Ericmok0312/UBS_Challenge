from flask import Flask, request, jsonify
import heapq
import json

from routes import app

# Sample travel times between stations
travel_times = {
    "SS-TP": 20, "SS-YL": 20, "YL-TP": 40, "YL-TM": 10,
    "YL-TW": 20, "TM-TW": 20, "TM-L": 20, "L-TW": 30,
    "TP-TW": 30, "TP-ST": 10, "TW-ST": 20, "TW-KC": 10,
    "KC-ST": 20, "KC-SSP": 10, "SSP-ST": 20, "SSP-KLC": 10,
    "SSP-MK": 10, "KLC-MK": 10, "KLC-WTS": 10, "KLC-ST": 20,
    "KLC-KT": 10, "WTS-ST": 20, "WTS-SK": 30, "WTS-KT": 10,
    "KT-SK": 30, "KT-NP": 20, "SK-ST": 20, "MK-C": 10,
    "MK-WC": 20, "C-S": 30, "C-WC": 10, "WC-S": 20, "WC-NP": 10,
    "NP-S": 20
}

# Function to find shortest path using Dijkstra's algorithm
def dijkstra(source, destination):
    # This would compute the shortest path between two stations based on travel times
    # Implementing Dijkstra’s algorithm to find shortest travel time path
    # For simplicity, assume `travel_times` as an adjacency list for now
    # In practice, this function will return the shortest path and distance
    return ['SS', 'TP', 'YL'], 50  # Sample path and travel time

# Function to calculate the optimal path and customers
def calculate_optimal_route(taxi_info, station_info, start_time, end_time):
    path = []
    customers = []
    profit = 0

    current_station = taxi_info[0]['taxiLocation']
    path.append(current_station)

    while start_time < end_time:
        station = next((s for s in station_info if s['taxiStation'] == current_station), None)
        if station and station['customers']:
            customer = max(station['customers'], key=lambda c: c['fee'])
            customers.append(customer['customerId'])
            profit += customer['fee']
            current_station = customer['destination']
            path.append(current_station)
        else:
            customers.append(-1)
            break  # Exit loop if no more customers or paths

        # Update start time by adding travel time
        travel_path, travel_time = dijkstra(current_station, customer['destination'])
        start_time += travel_time

    return path, customers, profit

@app.route('/taxi-driver', methods=['POST'])
def taxi_driver():
    data = request.json
    challenge_input = data['challengeInput']
    
    start_time = int(challenge_input['startTime'].replace(':', ''))
    end_time = int(challenge_input['endTime'].replace(':', ''))
    taxi_info = challenge_input['taxiInfo']
    station_info = challenge_input['taxiStationInfo']
    
    # Calculate the optimal route
    path, customers, profit = calculate_optimal_route(taxi_info, station_info, start_time, end_time)
    
    # Return the result
    result = {
        'path': path,
        'customers': customers,
        'profit': profit
    }

    return jsonify(result)

