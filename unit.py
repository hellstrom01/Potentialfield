import math
import numpy as np
from typing import List

class OwnUnit: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 20
        self.unit_pos = (x,y) 
        self.position = np.array([x, y], dtype=np.int64)

    def move_unit(self, potential_map, boids_potential, enemy_units, radius=5):
        print(enemy_units, " in move unit ")
        print(self.get_unit_range(self))
        # Calculate combined force based on potential fields
        force = boids_potential.combined_force(self,enemy_units)
        print(self.position, " own pos")
        print(force, " the force")
        new_position = self.position + force  # Add force
        self.position = np.round(new_position).astype(np.int64) # Update position based on force vector
        if potential_map[int(round(self.position[0]))][int(round(self.position[1]))] == 1:                                            
            self.x, self.y = int(round(self.position[0])), int(round(self.position[1]))  # Update integer position

    def calculate_distance(self, x1, y1, x2, y2):
        """Calculate Euclidean distance between (x1, y1) and (x2, y2)."""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    def get_unit_range(self,unit):
        """Gets the attack range of a unit."""
        return unit.range

    def calcualate_attractive(self, own_unit, target_unit):
        """Calculate the attractive potential towards a target."""
        range_ = self.get_unit_range(self)
        direction = target_unit.position - own_unit.position
        distance = np.linalg.norm(direction)
        if distance == 0:
            return np.zeros(2)  # Avoid division by zero
        desired_distance = max(0, distance - range_)
        force_magnitude = min(1, desired_distance / 10)
        return (direction / distance) * force_magnitude

    def calculate_repulsive(self, own_unit, enemy_units, buffer=5.0):
        """Calculate the repulsive force from enemies."""
        total_force = np.zeros(2)
        for enemy in enemy_units:
            enemy_range = self.get_unit_range(enemy)
            direction = own_unit.position - enemy.position
            distance = np.linalg.norm(direction)
            buffer_distance = enemy_range + buffer
            if 0 < distance < buffer_distance:
                force = (buffer_distance - distance) / buffer_distance
                total_force += (direction / distance) * force
        return total_force

    def combined_force(self, unit, enemy_units):
        """Calculate the total combined force (attractive + repulsive)."""
        attractive_forces = np.sum([self.calcualate_attractive(unit, target) for target in enemy_units], axis=0)
        repulsive_force = self.calculate_repulsive(unit, enemy_units)
        total_force = attractive_forces + repulsive_force
        norm = np.linalg.norm(total_force)
        print(total_force)
        return total_force / norm if norm != 0 else total_force


class EnemyUnit:
      def __init__(self, x,y):
        self.x= x
        self.y = y
        self.position = np.array([x, y], dtype=np.int64)
        self.range = 10

