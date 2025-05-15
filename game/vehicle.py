# -*- coding: utf-8 -*-
"""
Created on Thu May 15 12:01:57 2025

@author: TRMA
"""

class Vehicle:
    def __init__(self, id, x, y, length, orientation, color):
        self.id = id
        self.x = x
        self.y = y
        self.length = length
        self.orientation = orientation  # 'H' or 'V'
        self.color = color

    def cells_occupied(self):
        return [
            (self.x + i, self.y) if self.orientation == 'H'
            else (self.x, self.y + i)
            for i in range(self.length)
        ]

    def move(self, dx, dy):
        if self.orientation == 'H':
            self.x += dx
        else:
            self.y += dy

    def copy(self):
        return Vehicle(
            id=self.id,
            x=self.x,
            y=self.y,
            length=self.length,
            orientation=self.orientation,
            color=self.color
        )
