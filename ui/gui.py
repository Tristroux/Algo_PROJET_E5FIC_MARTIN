# -*- coding: utf-8 -*-
"""
Created on Thu May 15 12:04:09 2025

@author: TRMA
"""
### Fichier: ui/gui.py

import pygame
from game.board import Board
from game.levels import LEVELS
from game.solver import solve
from game.level_generator import generate_random_level

CELL_SIZE = 100
GRID_WIDTH = 6 * CELL_SIZE
PANEL_WIDTH = 200
WIDTH, HEIGHT = GRID_WIDTH + PANEL_WIDTH, 6 * CELL_SIZE

import os

class GameUI:
    def __init__(self):        
        self.isGameRunning = True
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rush Hour")
        self.clock = pygame.time.Clock()

        # Chemin absolu relatif au script
        assets_path = os.path.join(os.path.dirname(__file__), 'assets')

        # Chargement des images
        self.img_background = pygame.image.load(os.path.join(assets_path, 'background.png')).convert()
        self.img_background = pygame.transform.scale(self.img_background, (WIDTH, HEIGHT))

        self.img_menu = pygame.image.load(os.path.join(assets_path, 'menu.jpg')).convert_alpha()
        self.img_menu = pygame.transform.scale(self.img_menu, (WIDTH, HEIGHT))
        self.img_car = pygame.image.load(os.path.join(assets_path, 'car1.png')).convert_alpha()
        self.img_truck = pygame.image.load(os.path.join(assets_path, 'truck.png')).convert_alpha()
        self.img_car2 = pygame.image.load(os.path.join(assets_path, 'car.png')).convert_alpha()
        self.img_car2 = pygame.transform.scale(self.img_car2, (CELL_SIZE * 2, CELL_SIZE))


        # Redimensionne les images une fois pour éviter le faire à chaque draw
        self.img_car = pygame.transform.scale(self.img_car, (CELL_SIZE * 2, CELL_SIZE))
        self.img_truck = pygame.transform.scale(self.img_truck, (CELL_SIZE * 3, CELL_SIZE))

        self.level_index = None
        self.board = None
        self.selected = None
        self.in_menu = True
        self.animating_solution = False
        self.solution_button_rect = None
        self.reset_button_rect = None
        self.menu_button_rect = None
        self.randomLevel = None


    def draw_grid(self):
        for x in range(0, GRID_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (GRID_WIDTH, y))

    def draw_vehicles(self):
        for vid, v in self.board.vehicles.items():
            x = v.x * CELL_SIZE
            y = v.y * CELL_SIZE
    
            # Détection du véhicule rouge gagnant
            is_red_car = vid == "red"
    
            if v.length == 2:
                if is_red_car:
                    img = pygame.transform.rotate(self.img_car2, 90) if v.orientation == 'V' else self.img_car2
                else:
                    img = pygame.transform.rotate(self.img_car, 90) if v.orientation == 'V' else self.img_car
            elif v.length == 3:
                img = pygame.transform.rotate(self.img_truck, 90) if v.orientation == 'V' else self.img_truck
            else:
                # Fallback rectangle
                w = CELL_SIZE * v.length if v.orientation == 'H' else CELL_SIZE
                h = CELL_SIZE if v.orientation == 'H' else CELL_SIZE * v.length
                pygame.draw.rect(self.screen, pygame.Color(v.color), (x, y, w, h))
                continue
    
            self.screen.blit(img, (x, y))


    def draw_side_panel(self):
        panel_x = GRID_WIDTH
        pygame.draw.rect(self.screen, (50, 50, 50), (panel_x, 0, PANEL_WIDTH, HEIGHT))
        button_font = pygame.font.SysFont(None, 30)

        # Bouton Solution
        self.solution_button_rect = pygame.Rect(panel_x + 20, 50, 160, 50)
        pygame.draw.rect(self.screen, (180, 80, 80), self.solution_button_rect)
        text = button_font.render("Solution", True, (255, 255, 255))
        self.screen.blit(text, (self.solution_button_rect.centerx - text.get_width() // 2, self.solution_button_rect.centery - text.get_height() // 2))

        # Bouton Reset
        self.reset_button_rect = pygame.Rect(panel_x + 20, 120, 160, 50)
        pygame.draw.rect(self.screen, (100, 100, 200), self.reset_button_rect)
        text = button_font.render("Recharger", True, (255, 255, 255))
        self.screen.blit(text, (self.reset_button_rect.centerx - text.get_width() // 2, self.reset_button_rect.centery - text.get_height() // 2))

        # Bouton Menu
        self.menu_button_rect = pygame.Rect(panel_x + 20, 190, 160, 50)
        pygame.draw.rect(self.screen, (100, 200, 100), self.menu_button_rect)
        text = button_font.render("Menu", True, (255, 255, 255))
        self.screen.blit(text, (self.menu_button_rect.centerx - text.get_width() // 2, self.menu_button_rect.centery - text.get_height() // 2))

    def draw_menu(self):
        self.screen.blit(self.img_menu, (0, 0))

        font = pygame.font.SysFont(None, 60)
        title = font.render("Choisir un niveau", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        button_font = pygame.font.SysFont(None, 30)
        for i in range(3):
            btn_text = button_font.render(f"Niveau {i+1}", True, (0, 0, 0))
            btn_rect = pygame.Rect(WIDTH // 2 - 100, 150 + i * 100, 200, 60)
            pygame.draw.rect(self.screen, (200, 200, 200), btn_rect)
            self.screen.blit(btn_text, (btn_rect.centerx - btn_text.get_width() // 2, btn_rect.centery - btn_text.get_height() // 2))
        
        btn_text = button_font.render(f"Niveau Aléatoire", True, (0, 0, 0))
        btn_rect = pygame.Rect(WIDTH // 2 - 100, 150 + 3 * 100, 200, 60)
        pygame.draw.rect(self.screen, (200, 200, 200), btn_rect)
        self.screen.blit(btn_text, (btn_rect.centerx - btn_text.get_width() // 2, btn_rect.centery - btn_text.get_height() // 2))

        pygame.display.flip()

    def check_menu_click(self, pos):
        self.selected = None
        # Boutons des niveaux 1 à 3
        for i in range(3):
            btn_rect = pygame.Rect(WIDTH // 2 - 100, 150 + i * 100, 200, 60)
            if btn_rect.collidepoint(pos):
                self.level_index = i
                self.board = Board(LEVELS[i])
                self.in_menu = False
                self.isGameRunning = True
                self.randomLevel = None
                return  # clic valide, on quitte
    
        # Bouton "niveau aléatoire"
        random_btn_rect = pygame.Rect(WIDTH // 2 - 100, 150 + 3 * 100, 200, 60)
        if random_btn_rect.collidepoint(pos):
            # Affichage du message temporaire
            font = pygame.font.SysFont(None, 40)
            text = font.render("Génération du niveau en cours...", True, (255, 255, 255))
            pygame.draw.rect(self.screen, (0, 0, 0), (WIDTH // 2 - 150, HEIGHT // 2 - 30, 300, 60))  # fond noir
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
    
            # Génération
            level_data = generate_random_level()
    
            # Fin de génération
            self.board = Board(level_data)
            self.in_menu = False
            self.isGameRunning = True
            self.randomLevel = Board(level_data)


    def get_clicked_vehicle(self, pos):
        for vid, v in self.board.vehicles.items():
            x = v.x * CELL_SIZE
            y = v.y * CELL_SIZE
            w = CELL_SIZE * v.length if v.orientation == 'H' else CELL_SIZE
            h = CELL_SIZE if v.orientation == 'H' else CELL_SIZE * v.length
            rect = pygame.Rect(x, y, w, h)
            if rect.collidepoint(pos):
                return vid
        return None

    def show_popup(self, message):
        popup = pygame.Surface((300, 150))
        popup.fill((20, 20, 20))
        pygame.draw.rect(popup, (255, 255, 255), popup.get_rect(), 2)
        font = pygame.font.SysFont(None, 40)
        text = font.render(message, True, (255, 255, 255))
        popup.blit(text, (popup.get_width() // 2 - text.get_width() // 2, popup.get_height() // 2 - text.get_height() // 2))
        self.screen.blit(popup, (WIDTH // 2 - 150, HEIGHT // 2 - 75))
        pygame.display.flip()
        pygame.time.delay(2000)

    def check_win(self):
        red = self.board.vehicles.get("red")
        return self.isGameRunning == True and red and red.orientation == 'H' and red.x + red.length == 6 and red.y == 2

    def show_solution(self):
        self.animating_solution = True
        solution = solve(self.board)
        if not solution :            
            self.isGameRunning = False
            self.show_popup("Unsolvable")
            self.in_menu = True
            
        for vehicle_id, direction in solution:
            if not self.board.move_vehicle(vehicle_id, direction):
                continue            
            self.screen.blit(self.img_background, (0, 0))
            self.draw_exit_marker()  
            self.draw_grid()
            self.draw_vehicles()
            self.draw_side_panel()
            pygame.display.flip()
            pygame.time.delay(300)
        self.animating_solution = False
        if self.check_win():
            self.isGameRunning = False
            self.show_popup("Gagné !")
            self.in_menu = True

    def draw_exit_marker(self):
        # Coordonnées de la sortie : à droite de la cellule (5, 2)
        exit_x = 6 * CELL_SIZE - 5  # un peu avant le bord
        exit_y = 2 * CELL_SIZE + 10  # légère marge en haut
        exit_height = CELL_SIZE - 20  # marge haut/bas pour esthétique
    
        pygame.draw.line(self.screen, (0, 255, 0), (exit_x, exit_y), (exit_x, exit_y + exit_height), width=8)


    def run(self):
        running = True
        while running:
            self.screen.blit(self.img_background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and not self.animating_solution:
                    if self.in_menu:
                        self.check_menu_click(event.pos)
                    else:
                        if self.solution_button_rect and self.solution_button_rect.collidepoint(event.pos):
                            self.show_solution()
                        elif self.reset_button_rect and self.reset_button_rect.collidepoint(event.pos):
                            if self.randomLevel == None :
                                self.board = Board(LEVELS[self.level_index])
                            else :
                                self.board = self.randomLevel.copy()
                            self.isGameRunning = True
                        elif self.menu_button_rect and self.menu_button_rect.collidepoint(event.pos):
                            self.in_menu = True
                        else:
                            self.selected = self.get_clicked_vehicle(event.pos)

                elif self.isGameRunning and event.type == pygame.KEYDOWN and self.selected and not self.in_menu and not self.animating_solution:
                    if event.key == pygame.K_LEFT:
                        self.board.move_vehicle(self.selected, 'left')
                    elif event.key == pygame.K_RIGHT:
                        self.board.move_vehicle(self.selected, 'right')
                    elif event.key == pygame.K_UP:
                        self.board.move_vehicle(self.selected, 'up')
                    elif event.key == pygame.K_DOWN:
                        self.board.move_vehicle(self.selected, 'down')

            if self.in_menu:
                self.draw_menu()
            else:
                self.draw_grid()
                self.draw_exit_marker()  
                self.draw_vehicles()
                self.draw_side_panel()
                if self.check_win() :
                     self.isGameRunning = False
                     self.show_popup("Gagné !")
                     self.in_menu = True
                pygame.display.flip()

           
            self.clock.tick(60)
        pygame.quit()
        
        
