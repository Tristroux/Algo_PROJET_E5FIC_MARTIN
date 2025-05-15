# -*- coding: utf-8 -*-
"""
Created on Thu May 15 12:38:17 2025

@author: TRMA
"""

from collections import deque
import copy

def board_to_key(board):
    
    return tuple((v.x, v.y) for v in board.vehicles.values())

def solve(initial_board):
    
    visited = set()
    queue = deque()
    queue.append((copy.deepcopy(initial_board), []))
    visited.add(board_to_key(initial_board))

    while queue:
        current_board, path = queue.popleft()

        # Victoire
        red = current_board.vehicles["red"]
        if red.orientation == 'H' and red.x + red.length == 6 and red.y == 2:
            return path

        for vid in current_board.vehicles.keys():
            for direction in ['left', 'right', 'up', 'down']:
                new_board = copy.deepcopy(current_board)
                if new_board.move_vehicle(vid, direction):
                    key = board_to_key(new_board)
                    if key not in visited:
                        visited.add(key)
                        queue.append((new_board, path + [(vid, direction)]))

    # Pas de solution trouvée
    return []
