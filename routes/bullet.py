from flask import Flask, request, jsonify
from collections import deque
import copy

import json
import logging

from flask import request

from routes import app

# Directions mapping
DIRS = {
    'u': (-1, 0),
    'd': (1, 0),
    'l': (0, -1),
    'r': (0, 1)
}

# Prioritized move directions: prioritize 'd' then 'l'
MOVE_DIRS = ['d', 'l', 'u', 'r']

def parse_map(map_str):
    grid = [list(line) for line in map_str.strip().split('\n')]
    bullets = []
    player = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '*':
                player = (i, j)
            elif cell in DIRS:
                bullets.append({'pos': (i, j), 'dir': cell})
    return grid, player, bullets

def move_bullets(bullets, rows, cols):
    new_bullets = []
    for bullet in bullets:
        di, dj = DIRS[bullet['dir']]
        ni, nj = bullet['pos'][0] + di, bullet['pos'][1] + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            new_bullets.append({'pos': (ni, nj), 'dir': bullet['dir']})
    return new_bullets

def is_safe(pos, bullets_set):
    return pos not in bullets_set

def serialize_state(player_pos, bullets):
    bullets_sorted = sorted([tuple(b['pos']) for b in bullets])
    return (player_pos, tuple(bullets_sorted))

@app.route('/dodge', methods=['POST'])
def dodge():
    input_data = request.get_data(as_text=True)
    grid, player, bullets = parse_map(input_data)
    rows, cols = len(grid), len(grid[0])

    # BFS initialization
    queue = deque()
    visited = set()
    initial_state = (player, bullets, [])
    queue.append(initial_state)
    visited.add(serialize_state(player, bullets))

    # Define a maximum number of steps to prevent infinite search
    MAX_STEPS = 100

    while queue:
        current_player, current_bullets, instructions = queue.popleft()

        if len(instructions) > MAX_STEPS:
            break

        # Check if current position is safe
        bullets_set = set(b['pos'] for b in current_bullets)
        if not is_safe(current_player, bullets_set):
            continue

        # If no bullets left, return instructions
        if not current_bullets:
            return jsonify({"instructions": instructions})

        # Try all possible moves
        for move in MOVE_DIRS:
            di, dj = DIRS[move]
            ni, nj = current_player[0] + di, current_player[1] + dj

            # Check map boundaries
            if not (0 <= ni < rows and 0 <= nj < cols):
                continue

            # Check if the new position is safe (no bullet currently)
            if (ni, nj) in bullets_set:
                continue

            # Move bullets
            new_bullets = move_bullets(current_bullets, rows, cols)
            new_bullets_set = set(b['pos'] for b in new_bullets)

            # Check if the new player position would be safe after bullets move
            if (ni, nj) in new_bullets_set:
                continue

            # Serialize the new state
            new_state = ( (ni, nj), new_bullets, instructions + [move] )
            serialized = serialize_state((ni, nj), new_bullets)
            if serialized in visited:
                continue
            visited.add(serialized)

            queue.append(new_state)

    # If no safe path found
    return jsonify({"instructions": None})

