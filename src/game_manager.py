import pygame
from map import *
from enemy import *
from renderer import *
renderer = Renderer(pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)))

clock = pygame.time.Clock()
running = True

tower_list = []
enemy_list = []

class Game:
    def __init__(self):
        pass

    def play(self):
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            game_state = {
                "map":game_map,
                "towers":tower_list,
                "enemies":enemy_list,
                "stat": {
                    "gold" : 0,
                    "hp" : 100,
                    "wave" : 1,
                    "max_wave" : 5 
                }
            }
    
            renderer.render(game_state)

            pygame.display.flip()

        