# -*- coding: utf-8 -*-
"""
Created on Thu May 15 12:48:46 2025

@author: TRMA
"""

import random

from game.solver import solve
from game.board import Board

def generate_random_level():
    vehicles = []
    used_ids = set()

    # Place la voiture rouge
    red_vehicle = {
        "id": "red",
        "x": 1,
        "y": 2,
        "length": 2,
        "orientation": "H",
        "color": "red"
    }
    vehicles.append(red_vehicle)
    occupied = {(1, 2), (2, 2)}  # ✔️ Set contenant les 2 cellules occupées par la voiture rouge


    def generate_unique_id():
        i = 1
        while True:
            vid = f"v{i}"
            if vid not in used_ids:
                used_ids.add(vid)
                return vid
            i += 1

    def vehicle_cells(x, y, length, orientation):
        if orientation == 'H':
            return {(x + i, y) for i in range(length)}
        else:
            return {(x, y + i) for i in range(length)}

    num_vehicles = random.randint(1, 5)
    attempts = 0
    max_attempts = 50

    while len(vehicles) < num_vehicles + 1 and attempts < max_attempts:
        length = random.choice([2, 3])
        orientation = random.choice(['H', 'V'])
        if orientation == 'H':
            x = random.randint(0, 6 - length)
            y = random.randint(0, 5)
        else:
            x = random.randint(0, 5)
            y = random.randint(0, 6 - length)

        new_cells = vehicle_cells(x, y, length, orientation)
        if not new_cells & occupied:
            vehicle = {
                "id": generate_unique_id(),
                "x": x,
                "y": y,
                "length": length,
                "orientation": orientation,
                "color": "#{:06x}".format(random.randint(0, 0xFFFFFF))
            }
            vehicles.append(vehicle)
            occupied.update(new_cells)
        attempts += 1
    
    
    solution = solve(Board(vehicles))
    if not solution : 
        return generate_random_level()

    return vehicles
