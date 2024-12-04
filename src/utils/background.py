import pygame 
import random

def draw_gradient(screen, start_color, end_color):
    for y in range(screen.get_height()):
        ratio = y / screen.get_height()
        color = [
            start_color[i] + (end_color[i] - start_color[i]) * ratio
            for i in range(3)
        ]
        pygame.draw.line(screen, color, (0, y), (screen.get_width(), y))

particles = [{"pos": [random.randint(0, 800), random.randint(0, 600)], "vel": [1, -1]} for _ in range(50)]

def update_particles(screen):
    for p in particles:
        p["pos"][0] += p["vel"][0]
        p["pos"][1] += p["vel"][1]
        pygame.draw.circle(screen, (173, 216, 230), p["pos"], 3)
        if p["pos"][0] < 0 or p["pos"][0] > screen.get_width():
            p["vel"][0] *= -1
        if p["pos"][1] < 0 or p["pos"][1] > screen.get_height():
            p["vel"][1] *= -1