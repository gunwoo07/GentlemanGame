import pygame
from src.map import get_pos_lefttop, get_pos
from src.tower import Archer, Cannon, Frost
from src.config import *

class TowerButton:
    WIDTH = 120
    HEIGHT = 80

    def __init__(self, tower, bx, by):
        self.tower = tower
        self.bx = bx
        self.by = by
        self.rect = pygame.Rect(bx, by, self.WIDTH, self.HEIGHT)

    def draw(self, screen, font):
        # [버튼 배경 및 테두리]
        pygame.draw.rect(screen, (60, 60, 60), self.rect)
        pygame.draw.rect(screen, 'white', self.rect, 1)

        # [타워 아이콘 - 왼쪽 배치]
        pygame.draw.circle(screen, self.tower.color, (self.bx + 30, self.by + 40), 20)

        # [텍스트 정보 - 오른쪽 배치]
        name_text = font.render(self.tower.type_name, True, 'white')
        cost_text = font.render(f"{self.tower.cost}G", True, 'yellow')

        screen.blit(name_text, (self.bx + 60, self.by + 25))
        screen.blit(cost_text, (self.bx + 60, self.by + 45))


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("malgungothic", 20)
        self.title_font = pygame.font.SysFont("malgungothic", 16)
        
        # 버튼 시작 위치 및 간격 계산
        start_x = MARGIN * 2
        btn_y = MARGIN * 2 + MAP_HEIGHT + 15
        btn_margin = 15
        
        self.btn_list = [
            TowerButton(Archer, start_x + (TowerButton.WIDTH + btn_margin) * 0, btn_y),
            TowerButton(Cannon, start_x + (TowerButton.WIDTH + btn_margin) * 1, btn_y),
            TowerButton(Frost, start_x + (TowerButton.WIDTH + btn_margin) * 2, btn_y)
        ]

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
        # 1. 하단 스탯 창 배경 (검은색 상자)
        stat_rect = (MARGIN, MARGIN*2 + MAP_HEIGHT, STAT_WIDTH, STAT_HEIGHT)
        pygame.draw.rect(self.screen, 'black', stat_rect)
        
        # 2. 버튼 그리기
        for btn in self.btn_list:
            btn.draw(self.screen, self.title_font)
            
        # 3. 하단 게임 정보 (버튼들 바로 아래에 한 줄로 표시)
        start_x = MARGIN * 2
        btn_y = MARGIN * 2 + MAP_HEIGHT + 15
        info_y = btn_y + TowerButton.HEIGHT + 20
        status_info = f"골드: {stat['gold']}   HP: {stat['hp']}   웨이브: {stat['wave']}/{stat['max_wave']}"
        stat_text = self.font.render(status_info, True, 'white')
        
        self.screen.blit(stat_text, (start_x, info_y))

    def draw_path(self, path):
        for i in range(len(path) - 1):
            start_pos = get_pos(path[i][0], path[i][1])
            end_pos = get_pos(path[i+1][0], path[i+1][1])
            pygame.draw.line(self.screen, 'white', (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]), 3)

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
