# -*- coding: utf-8 -*-
"""
Created on Thu May 15 12:03:43 2025

@author: TRMA
"""

from .vehicle import Vehicle

class Board:
    def __init__(self, level_data):
        self.initial_level = level_data
        self.vehicles = {v['id']: Vehicle(**v) for v in level_data}

    def occupied_cells(self):
        occ = set()
        for v in self.vehicles.values():
            occ.update(v.cells_occupied())
        return occ

    def can_move(self, vehicle_id, direction):
        v = self.vehicles[vehicle_id]
        dx, dy = (1, 0) if direction == 'right' else (-1, 0) if direction == 'left' else (0, 1) if direction == 'down' else (0, -1)
        if v.orientation == 'H' and dy != 0: return False
        if v.orientation == 'V' and dx != 0: return False

        next_cells = [
            (v.x + dx * v.length, v.y) if v.orientation == 'H' and dx > 0 else
            (v.x - 1, v.y) if v.orientation == 'H' and dx < 0 else
            (v.x, v.y + dy * v.length) if v.orientation == 'V' and dy > 0 else
            (v.x, v.y - 1) if v.orientation == 'V' and dy < 0 else None
        ]

        for cell in next_cells:
            if cell in self.occupied_cells():
                return False
            if not (0 <= cell[0] < 6 and 0 <= cell[1] < 6):
                return False
        return True

    def move_vehicle(self, vehicle_id, direction):
        if self.can_move(vehicle_id, direction):
            dx, dy = (1, 0) if direction == 'right' else (-1, 0) if direction == 'left' else (0, 1) if direction == 'down' else (0, -1)
            self.vehicles[vehicle_id].move(dx, dy)
            return True
        return False

    def is_victory(self):
        red = self.vehicles.get("red")
        return red and red.x + red.length - 1 == 5 and red.y == 2

    def reset(self):
        self.vehicles = {v['id']: Vehicle(**v) for v in self.initial_level}
        
        
    def export_level(self):
        level = []
        for v in self.vehicles.values():
            level.append({
                "id": v.id,
                "x": v.x,
                "y": v.y,
                "length": v.length,
                "orientation": v.orientation,
                "color": v.color
            })
        return level

    def add_vehicle(self, vehicle_data):
        new_vehicle = Vehicle(**vehicle_data)
        new_cells = set(new_vehicle.cells_occupied())
    
        # Vérifie qu'on reste dans la grille
        for x, y in new_cells:
            if not (0 <= x < 6 and 0 <= y < 6):
                return False
    
        # Vérifie les collisions
        if new_cells & self.occupied_cells():
            return False
    
        # Ajoute le véhicule
        self.vehicles[new_vehicle.id] = new_vehicle
        return True
    
    def copy(self):
        new_board = Board([])  # On initialise avec un niveau vide
        new_board.vehicles = {
            vid: v.copy() for vid, v in self.vehicles.items()
        }
        return new_board

  