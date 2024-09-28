from flask import Flask, request, jsonify
from typing import List, Dict, Any

from routes import app

# Directions mapping
DIRECTIONS = {
    "NORTH": (0, -1),
    "SOUTH": (0, 1),
    "EAST": (1, 0),
    "WEST": (-1, 0)
}

# Vehicle class
class Vehicle:
    def __init__(self, plateNumber: str, length: int, width: int, parkingFare: int):
        self.plateNumber = plateNumber
        self.length = length
        self.width = width
        self.parkingFare = parkingFare

# Function to check if parking is valid
def is_parking_valid(parking_lot: List[List[str]], vehicle: Vehicle, x: int, y: int, direction: str) -> bool:
    # Check if the vehicle fits in the parking space
    dx, dy = DIRECTIONS[direction]
    for i in range(vehicle.length):
        for j in range(vehicle.width):
            if parking_lot[y + i * dy][x + j * dx] not in (" ", "I", "O"):
                return False
    return True

# Function to calculate total fare
def calculate_total_fare(vehicles: List[Vehicle], actions: List[Dict[str, Any]]) -> int:
    total_fare = 0
    for action in actions:
        vehicle = next((v for v in vehicles if v.plateNumber == action["plateNumber"]), None)
        if action["action"] == "exit" and vehicle:
            total_fare += vehicle.parkingFare
    return total_fare

# Endpoint for parking lot management
@app.route('/parkinglot', methods=['POST'])
def parking_lot():
    data = request.json
    results = []

    for case in data:
        min_total_fare = case["minimumTotalFare"]
        vehicles = [Vehicle(**v) for v in case["vehicles"]]
        actions = case["actions"]
        parking_lot = case["parkingLot"]

        # Prepare results for actions
        action_results = []
        total_fare = 0

        for action in actions:
            vehicle = next((v for v in vehicles if v.plateNumber == action["plateNumber"]), None)
            if action["action"] == "park":
                # Find parking position
                parked = False
                for y in range(len(parking_lot)):
                    for x in range(len(parking_lot[0])):
                        if is_parking_valid(parking_lot, vehicle, x, y, "EAST"):
                            parking_lot[y][x] = "V"  # Mark parking space
                            action_results.append({
                                "plateNumber": vehicle.plateNumber,
                                "action": "park",
                                "execute": True,
                                "position": {"x": x, "y": y, "direction": "EAST"}
                            })
                            parked = True
                            break
                    if parked:
                        break
                if not parked:
                    action_results.append({
                        "plateNumber": vehicle.plateNumber,
                        "action": "park",
                        "execute": False,
                        "position": None
                    })

            elif action["action"] == "exit":
                # Here we could implement exit logic
                # For simplicity, we assume the exit is successful for valid parking
                total_fare += vehicle.parkingFare
                action_results.append({
                    "plateNumber": vehicle.plateNumber,
                    "action": "exit",
                    "execute": True,
                    "position": {"x": 4, "y": 4, "direction": "EAST"}  # Example exit position
                })

        # Check if total fare meets the minimum requirement
        if total_fare >= min_total_fare:
            results.append({"actions": action_results})
        else:
            results.append({"actions": action_results, "error": "Minimum total fare not met."})

    return jsonify(results)

