import pygame
import math
import numpy as np

class Car:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle  # in radians
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.rotation_speed = 0.03
        self.alive = True
        self.fitness = 0
        self.distance = 0
        self.time_alive = 0
        
        # Car dimensions
        self.width = 20
        self.length = 40
        
        # Sensor configuration
        self.sensor_length = 100
        self.sensor_angles = [-math.pi/2, -math.pi/4, 0, math.pi/4, math.pi/2]
        
    def get_vertices(self):
        # Calculate car vertices for drawing and collision detection
        half_width = self.width / 2
        half_length = self.length / 2
        
        vertices = [
            (-half_length, -half_width),
            (half_length, -half_width),
            (half_length, half_width),
            (-half_length, half_width)
        ]
        
        # Rotate and translate vertices
        rotated_vertices = []
        for x, y in vertices:
            # Rotate
            rx = x * math.cos(self.angle) - y * math.sin(self.angle)
            ry = x * math.sin(self.angle) + y * math.cos(self.angle)
            # Translate
            tx = rx + self.x
            ty = ry + self.y
            rotated_vertices.append((tx, ty))
            
        return rotated_vertices
    
    def get_sensor_data(self, track):
        sensor_data = []
        for angle in self.sensor_angles:
            sensor_angle = self.angle + angle
            sensor_end_x = self.x + math.cos(sensor_angle) * self.sensor_length
            sensor_end_y = self.y + math.sin(sensor_angle) * self.sensor_length
            
            # Check for intersection with track boundaries
            distance = self.sensor_length
            for i in range(len(track.inner_boundary)):
                x1, y1 = track.inner_boundary[i]
                x2, y2 = track.inner_boundary[(i + 1) % len(track.inner_boundary)]
                
                intersect = self.line_intersection(
                    (self.x, self.y), (sensor_end_x, sensor_end_y),
                    (x1, y1), (x2, y2))
                
                if intersect:
                    dist = math.sqrt((intersect[0] - self.x)**2 + (intersect[1] - self.y)**2)
                    if dist < distance:
                        distance = dist
            
            for i in range(len(track.outer_boundary)):
                x1, y1 = track.outer_boundary[i]
                x2, y2 = track.outer_boundary[(i + 1) % len(track.outer_boundary)]
                
                intersect = self.line_intersection(
                    (self.x, self.y), (sensor_end_x, sensor_end_y),
                    (x1, y1), (x2, y2))
                
                if intersect:
                    dist = math.sqrt((intersect[0] - self.x)**2 + (intersect[1] - self.y)**2)
                    if dist < distance:
                        distance = dist
            
            # Normalize distance to [0, 1]
            sensor_data.append(distance / self.sensor_length)
        
        return sensor_data
    
    def line_intersection(self, line1_start, line1_end, line2_start, line2_end):
        # Implementation of line segment intersection
        x1, y1 = line1_start
        x2, y2 = line1_end
        x3, y3 = line2_start
        x4, y4 = line2_end
        
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None
            
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        
        if 0 <= t <= 1 and 0 <= u <= 1:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
        else:
            return None
    
    def steer(self, direction):
        # direction should be between -1 (left) and 1 (right)
        self.angle += direction * self.rotation_speed
    
    def accelerate(self, amount):
        # amount should be between -1 (brake/reverse) and 1 (accelerate)
        self.speed += amount * self.acceleration
        self.speed = max(-self.max_speed/2, min(self.max_speed, self.speed))
    
    def update(self, track):
        if not self.alive:
            return
        
        # Update position
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Update fitness
        self.time_alive += 1
        self.distance += abs(self.speed)
        self.fitness = self.distance + self.time_alive * 0.1
    
    def draw(self, screen):
        if not self.alive:
            return
        
        # Draw car body
        vertices = self.get_vertices()
        pygame.draw.polygon(screen, (0, 100, 255), vertices)
        
        # Draw sensors
        for angle in self.sensor_angles:
            sensor_angle = self.angle + angle
            end_x = self.x + math.cos(sensor_angle) * self.sensor_length
            end_y = self.y + math.sin(sensor_angle) * self.sensor_length
            pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), (end_x, end_y), 1)