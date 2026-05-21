import pygame
from src.map import get_pos_lefttop
from src.config import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
    
    def render(self, game_state):
        self.screen.fill((75, 0, 130)) # indigo blue
        self.draw_map(game_state['map'])
        self.draw_path(game_state['path'])
        self.draw_towers(game_state['towers'])
        self.draw_enemies(game_state['enemies'])
        self.draw_stat(game_state['stat'])
        
    def draw_map(self, game_map):
        for i in range(ROWS):
            for j in range(COLS):
                if game_map[i][j] == 0:
                    pygame.draw.rect(self.screen, 'lightgreen', (*get_pos_lefttop(j, i), TILE_SIZE, TILE_SIZE))
                if game_map[i][j] == 1:
                    pygame.draw.rect(self.screen, 'brown', (*get_pos_lefttop(j, i), TILE_SIZE, TILE_SIZE))
                elif game_map[i][j] == 2:
                    pygame.draw.rect(self.screen, 'red', (*get_pos_lefttop(j, i), TILE_SIZE, TILE_SIZE))
                elif game_map[i][j] == 3:
                    pygame.draw.rect(self.screen, 'green', (*get_pos_lefttop(j, i), TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(self.screen, 'black', (*get_pos_lefttop(j, i), TILE_SIZE, TILE_SIZE), 1)

    def draw_towers(self, towers):
        for tower in towers:
            tower.draw(self.screen)

    def draw_enemies(self, enemies):
        for enemy in enemies:
            enemy.draw(self.screen)

    def draw_stat(self, stat):
        pygame.draw.rect(self.screen, 'black', (MARGIN, MARGIN*2+MAP_HEIGHT, STAT_WIDTH, STAT_HEIGHT))
        font = pygame.font.SysFont("malgungothic", 24)
        stat_text = font.render(f"골드: {stat['gold']}  HP: {stat['hp']}  웨이브: {stat['wave']}/{stat['max_wave']}", True, 'white')
        self.screen.blit(stat_text, (MARGIN*2, MARGIN*5.5+MAP_HEIGHT+STAT_HEIGHT/4))

    def draw_path(self, path):
        for i in range(len(path) - 1):
            start_pos = get_pos_lefttop(path[i][0], path[i][1])
            end_pos = get_pos_lefttop(path[i+1][0], path[i+1][1])
            pygame.draw.line(self.screen, 'white', (start_pos[0] + TILE_SIZE//2, start_pos[1] + TILE_SIZE//2), (end_pos[0] + TILE_SIZE//2, end_pos[1] + TILE_SIZE//2), 3)

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
