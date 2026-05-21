import pygame
from src.map import *
from src.config import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
    
    def render(self, game_state):
        self.screen.fill((75, 0, 130)) # indigo blue
        self.draw_map(game_state['map'])
        self.draw_towers(game_state['towers'])
        self.draw_enemies(game_state['enemies'])
        self.draw_stat(game_state['stat'])
        
    def draw_map(self, game_map):
        for i in range(ROWS):
            for j in range(COLS):
                if game_map[i][j] == 0:
                    pygame.draw.rect(self.screen, 'lightgreen', (*get_pos(i, j), TILE_SIZE, TILE_SIZE))
                if game_map[i][j] == 1:
                    pygame.draw.rect(self.screen, 'brown', (*get_pos(i, j), TILE_SIZE, TILE_SIZE))
                elif game_map[i][j] == 2:
                    pygame.draw.rect(self.screen, 'red', (*get_pos(i, j), TILE_SIZE, TILE_SIZE))
                elif game_map[i][j] == 3:
                    pygame.draw.rect(self.screen, 'green', (*get_pos(i, j), TILE_SIZE, TILE_SIZE))
    
    def draw_towers(self, towers):
        for tower in towers:
            tower.draw(self.screen)

    def draw_enemies(self, enemies):
        for enemy in enemies:
            enemy.draw(self.screen)

    def draw_stat(self, stat):
        pygame.draw.rect(self.screen, 'black', (MARGIN, MARGIN*2+MAP_HEIGHT, STAT_WIDTH, STAT_HEIGHT))
        # font = pygame.font.SysFont("malgungothic", 24)
        # stat_text = font.render(f"골드: {stat['gold']}\nHP: {stat['hp']}\n웨이브: {stat['wave']}/{stat['max_wave']}", True, 'white')
        # self.screen.blit(stat_text, (MARGIN*2, MARGIN*2+MAP_HEIGHT+STAT_HEIGHT/4))

"""
{
    "map":
    "towers":
    "enemies":
    "stat": {
        "gold":
        "hp":
        "wave":
        "max_wave":
    }
}
"""
