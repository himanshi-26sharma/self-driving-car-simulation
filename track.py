import pygame
import math
import random

class Track:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inner_boundary = []
        self.outer_boundary = []
        self.checkpoints = []
        self.start_pos = (0, 0)
        self.start_angle = 0
    
    def create_track(self):
        # Create a simple oval track
        center_x, center_y = self.width // 2, self.height // 2
        radius_x, radius_y = 300, 200
        
        # Inner boundary
        self.inner_boundary = []
        for i in range(0, 360, 10):
            angle = math.radians(i)
            x = center_x + (radius_x - 50) * math.cos(angle)
            y = center_y + (radius_y - 50) * math.sin(angle)
            self.inner_boundary.append((x, y))
        
        # Outer boundary
        self.outer_boundary = []
        for i in range(0, 360, 10):
            angle = math.radians(i)
            x = center_x + (radius_x + 50) * math.cos(angle)
            y = center_y + (radius_y + 50) * math.sin(angle)
            self.outer_boundary.append((x, y))
        
        # Start position and angle
        self.start_pos = (center_x + radius_x, center_y)
        self.start_angle = math.pi  # Pointing left
        
        # Create checkpoints (every 90 degrees)
        self.checkpoints = []
        for i in range(0, 360, 90):
            angle = math.radians(i)
            x = center_x + radius_x * math.cos(angle)
            y = center_y + radius_y * math.sin(angle)
            self.checkpoints.append((x, y))
    
    def is_on_track(self, x, y):
        # Simple check if point is between inner and outer boundaries
        center_x, center_y = self.width // 2, self.height // 2
        radius_x, radius_y = 300, 200
        
        # Calculate normalized distance from center
        dx = (x - center_x) / radius_x
        dy = (y - center_y) / radius_y
        distance_squared = dx*dx + dy*dy
        
        inner_radius = 0.7  # (radius - 50)/radius
        outer_radius = 1.2  # (radius + 50)/radius
        
        return inner_radius**2 <= distance_squared <= outer_radius**2
    
    def draw(self, screen):
        # Draw inner boundary
        if len(self.inner_boundary) > 1:
            pygame.draw.lines(screen, (255, 255, 255), True, self.inner_boundary, 2)
        
        # Draw outer boundary
        if len(self.outer_boundary) > 1:
            pygame.draw.lines(screen, (255, 255, 255), True, self.outer_boundary, 2)
        
        # Draw checkpoints
        for checkpoint in self.checkpoints:
            pygame.draw.circle(screen, (0, 255, 0), (int(checkpoint[0]), int(checkpoint[1])), 5)
        
        # Draw start position
        pygame.draw.circle(screen, (255, 0, 0), (int(self.start_pos[0]), int(self.start_pos[1])), 5)