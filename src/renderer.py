import pygame
import map

class Renderer:
    def __init__(self, screen):
        self.screen = screen
    
    def render(self, game_state):
        self.screen.fill((75, 0, 130)) # indigo blue
        self.draw_map(game_state.map)
    
    def draw_map(self, game_map):
        for i in range(map.ROWS):
            for j in range(map.COLS):
                if game_map[i][j] == 0:
                    pygame.draw.rect(self.screen, 'lightgreen', (*map.get_pos(i, j), map.TILE_SIZE, map.TILE_SIZE))
                if game_map[i][j] == 1:
                    pygame.draw.rect(self.screen, 'brown', (*map.get_pos(i, j), map.TILE_SIZE, map.TILE_SIZE))
                elif game_map[i][j] == 2:
                    pygame.draw.rect(self.screen, 'red', (*map.get_pos(i, j), map.TILE_SIZE, map.TILE_SIZE))
                elif game_map[i][j] == 3:
                    pygame.draw.rect(self.screen, 'green', (*map.get_pos(i, j), map.TILE_SIZE, map.TILE_SIZE))