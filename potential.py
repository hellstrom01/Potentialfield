import pygame 
import json
import os
from unit import OwnUnit, EnemyUnit
import math

class Potential:
    def __init__(self):
        self.map = [[]]

    def create_map(self):
        """initialize potentials in the map"""
        self.read_map_from_json()

        for y,row in enumerate(self.map):
            for x,tile in enumerate(row):
                if 55<x<70 and 55<y<60:
                    if tile == 1:
                            self.map[y][x] = 2
                    else:
                        self.map[y][x] = tile 
                else:
                    #adding potential for a walkable tile
                    if tile == 1:
                        self.map[y][x] =  tile 
                    else:
                        self.map[y][x] = tile

    def read_map_from_json(self, file_name="map.json", directory="map_directory") -> None:
            filepath = os.path.join(directory, file_name)
            try:
                with open(filepath, "r") as file:
                    self.map = json.load(file)

            except FileNotFoundError:
                print(f"Error: The file {file_name} was not found in the directory {directory}.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    
class Visualize:
        def __init__(self,potential):
            self.potential = potential
            self.map = self.potential.map
            self.own_units = []
            self.enemy_units = []
        def create_units(self):
            for y,row in enumerate(self.map):
                for x in range(len(row)):
                    if 55<x<70 and 55<y<60:
                        self.enemy_units.append(EnemyUnit(y,x))

                    elif 60<x<75 and 85 < y <95:
                        self.own_units.append(OwnUnit(x, y))
             
        def draw_map(self,cell_size = 5):
            pygame.init()
            self.create_units()
            map_width = len(self.map[0]) if self.map else 0
            map_height = len(self.map) if self.map else 0
            screen_width = map_width * cell_size
            screen_height = map_height * cell_size
            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("Potential Field Visualization")
            
            running = True
            while running:
                for unit in self.own_units:
                    unit.move_unit(self.map,unit,self.enemy_units)
                    self.map[unit.y][unit.x] =  3 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                # Draw the map
                screen.fill((0, 0, 0)) 
                walkable_color = (255,255,255)
                not_walkable_color = (0,0,0)
                enemy_unit_color = (250,0,0)
                own_unit_color = (0, 255, 0)
                for y,row in enumerate(self.map):
                    for x,tile in enumerate(row):
                        color = (0,0,0)
                        if tile == 0:
                                color = not_walkable_color
                        elif tile == 1:
                                color = walkable_color
                        elif tile == 2:
                                color = enemy_unit_color
                        elif tile == 3:
                                color = own_unit_color
                        pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
                pygame.display.flip()
            pygame.quit()