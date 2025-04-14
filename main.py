import pygame
import sys
import math
import numpy as np
import neat
import os
import random
from car import Car
from track import Track

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self-Driving Car Simulation with NEAT")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
def eval_genomes(genomes, config):
    
    # Initialize pygame font
    generation_font = pygame.font.SysFont("Arial", 30)
    stats_font = pygame.font.SysFont("Arial", 20)
    
    
    # Create track
    track = Track(WIDTH, HEIGHT)
    track.create_track()
    
    # Create cars
    cars = []
    nets = []
    ge = []
    
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car(track.start_pos[0], track.start_pos[1], track.start_angle))
        ge.append(genome)
    
    # Simulation loop
    running = True
    while running and len(cars) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
        # Update cars and get neural network outputs
        for i, car in enumerate(cars):
            if not car.alive:
                continue
                
            # Get sensor data and process through neural network
            sensor_data = car.get_sensor_data(track)
            output = nets[i].activate(sensor_data)
            car.steer(output[0] * 2 - 1)  # Convert to [-1,1] range
            car.accelerate(output[1] * 2 - 1)
            car.update(track)
            
            # Update fitness
            ge[i].fitness = car.fitness
            
            # Check if car is out of bounds
            if not track.is_on_track(car.x, car.y) or car.speed < 0.1:
                car.alive = False
                ge[i].fitness -= 10
        
        # Remove dead cars and their networks
        cars = [car for car in cars if car.alive]
        nets = [net for i, net in enumerate(nets) if i < len(cars) and cars[i].alive]
        ge = [g for i, g in enumerate(ge) if i < len(cars) and cars[i].alive]
        
        # Draw everything
        screen.fill(BLACK)
        track.draw(screen)
        
        # Display generation info
        text = generation_font.render(f"Cars Alive: {len(cars)}", True, WHITE)
        screen.blit(text, (10, 10))
        
        for car in cars:
            car.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
        
        # Display generation info
        draw_text(f"Cars Alive: {len(cars)}", generation_font, WHITE, screen, 10, 10)
        
        pygame.display.flip()
        clock.tick(FPS)

def run(config_path):
    # Load NEAT config
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    
    # Create population
    p = neat.Population(config)
    
    # Add reporters
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    # Run NEAT
    winner = p.run(eval_genomes, 50)  # Run for 50 generations
    
    # Save winner
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)