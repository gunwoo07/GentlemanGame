import pygame
from src.core.config import *
from src.core.map import find_grid_pos, get_pos_lefttop, get_pos
from src.entities.tower import Archer, Cannon, Frost
from src.ui.components.button import (
    TowerButton,
    LevelupButton,
    SellButton
)
from src.ui.screens.title_screen import TitleScreen
from src.ui.screens.ranking_screen import RankingScreen
from src.ui.screens.result_screen import ResultScreen

from copy import deepcopy
from src.core.map import find_shortest_path


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont("malgungothic", 20)
        self.font = pygame.font.SysFont("malgungothic", 16)
        self.small_font = pygame.font.SysFont("malgungothic", 12)
        self.title_screen = TitleScreen(self.screen)
        self.ranking_screen = RankingScreen(self.screen)
        self.BACKGROUND_COLOR = (75, 0, 130)
        self.current_bgm = None
        
        self.selected_tower_btn = None
        self.selected_tower = None
        # 버튼 시작 위치 및 간격 계산
        start_x = MARGIN * 2
        btn_y = MARGIN * 2 + MAP_HEIGHT + 15
        btn_margin = 15
        
        self.tower_btns = {
            "archer": TowerButton(Archer, start_x + (TowerButton.WIDTH + btn_margin) * 0, btn_y),
            "cannon": TowerButton(Cannon, start_x + (TowerButton.WIDTH + btn_margin) * 1, btn_y),
            "frost": TowerButton(Frost, start_x + (TowerButton.WIDTH + btn_margin) * 2, btn_y)
        }
        self.levelup_btn = LevelupButton(None, 0, 0)  # 초기화는 나중에 tower가 선택될 때 이루어짐
        self.sell_btn = SellButton(0, 0)
    
    def check_is_tower_selected(self, towers):
        self.selected_tower = None
        for tower in towers:
            if tower.is_selected:
                self.selected_tower = tower
                break
    
    def show_title(self, bgm):
        self.play_bgm(bgm)
        return self.title_screen.run()
    
    def show_ranking(self, bgm):
        self.play_bgm(bgm)
        return self.ranking_screen.run()
    
    def show_result(self, is_win, score, wave_index, bgm):
        self.play_bgm(bgm)
        result_screen = ResultScreen(self.screen, is_win, score, wave_index+1)
        return result_screen.run()
    
    def render(self, game_state):
        # 선택된 타워가 있는지 확인
        self.check_is_tower_selected(game_state['towers'])
        
        self.draw_map(game_state['game_map'])
        self.draw_tower_preview(game_state['game_map'])
        self.draw_path(game_state['path'])
        self.draw_towers(game_state['towers'])
        self.draw_enemies(game_state['enemies'])
        self.draw_bullets(game_state['bullets'])
        self.draw_skills(game_state['skills'])
        # self.draw_stat(game_state['stat'])
        self.draw_stat({"hp": game_state["hp"], "gold": game_state["gold"], "wave": game_state["wave_index"]+1, "max_wave": len(game_state["wave_data"])})
        self.draw_message(game_state['current_message'])
        self.draw_blank()
        self.play_bgm(game_state['bgm'])

    def draw_map(self, game_map):
        for i in range(ROWS):
            for j in range(COLS):
                tile_rect = pygame.Rect(*get_pos_lefttop(j, i), TILE_SIZE, TILE_SIZE)
                if game_map[i][j] == 0:
                    if (i+j)%2 == 0:  
                        pygame.draw.rect(self.screen, 'lightgreen', tile_rect)
                    else:
                        pygame.draw.rect(self.screen, 0x5ea152, tile_rect)
                    if tile_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(self.screen, 'yellow', tile_rect, 1)
                    else:
                        pygame.draw.rect(self.screen, 'black', tile_rect, 1)
                elif game_map[i][j] == 1:
                    pygame.draw.rect(self.screen, 'brown', tile_rect)
                    pygame.draw.rect(self.screen, 'black', tile_rect, 1)
                elif game_map[i][j] == 2:
                    pygame.draw.rect(self.screen, 'red', tile_rect)
                    pygame.draw.rect(self.screen, 'black', tile_rect, 1)
                elif game_map[i][j] == 3:
                    pygame.draw.rect(self.screen, 'green', tile_rect)
                    pygame.draw.rect(self.screen, 'black', tile_rect, 1)

    def draw_stat(self, stat):
        if self.selected_tower:
            # attack range 그리기
            pygame.draw.circle(self.screen, 'white', (self.selected_tower.pos.x, self.selected_tower.pos.y), self.selected_tower.attack_range, 1)
            # 1. 하단 스탯 창 배경 (검은색 상자)
            stat_rect = (MARGIN, MARGIN*2 + MAP_HEIGHT, STAT_WIDTH, STAT_HEIGHT)
            pygame.draw.rect(self.screen, 'black', stat_rect)
                
            # 2. 버튼 그리기
            for btn in self.tower_btns.values():
                btn.draw(self.screen, self.font)
                    
            # 3. 하단 게임 정보 (버튼들 바로 아래에 한 줄로 표시)
            start_x = MARGIN * 2
            btn_y = MARGIN * 2 + MAP_HEIGHT + 15
            info_y = btn_y + TowerButton.HEIGHT + 20
            status_info = f"골드: {stat['gold']}   HP: {stat['hp']}   웨이브: {stat['wave']}/{stat['max_wave']}"
            stat_text = self.title_font.render(status_info, True, 'white')
                
            self.screen.blit(stat_text, (start_x, info_y))

            # tower 정보 적기
            start_x = MARGIN * 2
            tower_info_y = MARGIN * 2 + MAP_HEIGHT + 15
            tower_info_x = start_x + (TowerButton.WIDTH + 15) * 3

            tower_name_text = self.font.render(f'{self.selected_tower.type_name}(lv. {self.selected_tower.level}/{self.selected_tower.max_level})', True, 'white')
            tower_info_text = self.font.render(f'대미지: {self.selected_tower.damage}   범위: {self.selected_tower.attack_range/TILE_SIZE:.1f}   공격속도: {self.selected_tower.attack_speed}', True, 'white')

            self.screen.blit(tower_name_text, (tower_info_x, tower_info_y))
            self.screen.blit(tower_info_text, (tower_info_x, tower_info_y+20))

            # 스킬 준비 상태 바
            skill_bar_width = 200
            skill_bar_height = 10
            skill_bar_x = tower_info_x
            skill_bar_y = tower_info_y + 50
            pygame.draw.rect(self.screen, 'white', (skill_bar_x, skill_bar_y, skill_bar_width, skill_bar_height), 1)
            if 0 <= self.selected_tower.skill_rate <= 1:
                inner_bar_width = skill_bar_width * self.selected_tower.skill_rate
            elif self.selected_tower.skill_rate > 1:
                inner_bar_width = skill_bar_width
            else:
                inner_bar_width = 0
            pygame.draw.rect(self.screen, 'yellow', (skill_bar_x, skill_bar_y, inner_bar_width, skill_bar_height))

            # 레벨업 버튼
            self.levelup_btn = LevelupButton(self.selected_tower, tower_info_x, tower_info_y + 70)
            self.levelup_btn.draw(self.screen, self.font)

            # 판매 버튼
            self.sell_btn = SellButton(
                tower_info_x + 140,
                tower_info_y + 70
            )
            self.sell_btn.draw(self.screen, self.font, self.selected_tower.get_sell_price())
        else:
            # 1. 하단 스탯 창 배경 (검은색 상자)
            stat_rect = (MARGIN, MARGIN*2 + MAP_HEIGHT, STAT_WIDTH, STAT_HEIGHT)
            pygame.draw.rect(self.screen, 'black', stat_rect)
            
            # 2. 버튼 그리기
            for btn in self.tower_btns.values():
                btn.draw(self.screen, self.font)
                
            # 3. 하단 게임 정보 (버튼들 바로 아래에 한 줄로 표시)
            start_x = MARGIN * 2
            btn_y = MARGIN * 2 + MAP_HEIGHT + 15
            info_y = btn_y + TowerButton.HEIGHT + 20
            status_info = f"골드: {stat['gold']}   HP: {stat['hp']}   웨이브: {stat['wave']}/{stat['max_wave']}"
            stat_text = self.title_font.render(status_info, True, 'white')
            
            self.screen.blit(stat_text, (start_x, info_y))
            text1 = self.font.render("웨이브 시작: 스페이스 바", True, 'white')
            text2 = self.font.render("타워 선택/배치/합체: 좌클릭", True, 'white')
            text3 = self.font.render("선택 취소: 우클릭", True, 'white')
            text4 = self.font.render("F: 일시정지   ESC: 타이틀", True, 'white')
            text5 = self.font.render("2: 2배속 on/off", True, 'white')
            self.screen.blit(text1, (start_x + (TowerButton.WIDTH + 15) * 3, btn_y))
            self.screen.blit(text2, (start_x + (TowerButton.WIDTH + 15) * 3, btn_y + 40))
            self.screen.blit(text3, (start_x + (TowerButton.WIDTH + 15) * 3, btn_y + 60))
            self.screen.blit(text4, (start_x + (TowerButton.WIDTH + 15) * 3, btn_y + 80))
            self.screen.blit(text5, (start_x + (TowerButton.WIDTH + 15) * 3, btn_y + 100))


    def draw_path(self, path):
        for i in range(len(path) - 1):
            start_pos = get_pos(path[i][0], path[i][1])
            end_pos = get_pos(path[i+1][0], path[i+1][1])
            pygame.draw.line(self.screen, 'white', (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]), 3)

    def draw_towers(self, towers):
        for tower in towers:
            tower.draw(self.screen)

    def draw_enemies(self, enemies):
        for enemy in enemies:
            enemy.draw(self.screen)

    def draw_bullets(self, bullets):
        for bullet in bullets:
            bullet.draw(self.screen)
    
    def draw_skills(self, skills):
        for skill in skills:
            skill.draw(self.screen)
    
    def draw_message(self, msg):
        if not msg:
            return
        alpha = max(0, int((msg['timer']))/msg['max_duration'] * 255)
        text_surf = self.title_font.render(msg['text'], True, (255, 255, 255))
        
        temp_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
        temp_surf.blit(text_surf, (0, 0))
        temp_surf.set_alpha(alpha)

        text_rect = temp_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 80))

        bg_rect = text_rect.inflate(40, 20)
        bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)

        pygame.draw.rect(bg_surf, (0, 0, 0, int(alpha//1.5)), bg_surf.get_rect(), border_radius=10)

        self.screen.blit(bg_surf, bg_rect)
        self.screen.blit(temp_surf, text_rect)

    def draw_tower_preview(self, game_map):
        
        if not self.selected_tower_btn:
            return
        mouse_pos = pygame.mouse.get_pos()
        grid_pos = find_grid_pos(mouse_pos)
        if grid_pos:
            x, y = grid_pos
            if game_map[x][y] != 0:
                return
            center = get_pos(y, x)
            tower_class = self.selected_tower_btn.tower_class
            temp_surface = pygame.Surface(
                (WINDOW_WIDTH, WINDOW_HEIGHT),
                pygame.SRCALPHA
            )
            # 공격 범위
            pygame.draw.circle(
                temp_surface,
                (255, 255, 255, 70),
                center,
                tower_class.LEVEL_DATA[1]["attack_range"],
                2
            )

            # 타워 본체
            pygame.draw.circle(
                temp_surface,
                (*tower_class.LEVEL_DATA[1]["color"], 120),
                center,
                int(TILE_SIZE * 0.4)
            )
            self.screen.blit(temp_surface, (0, 0))

                    # 가상으로 타워 설치
            temp_map = deepcopy(game_map)
            temp_map[x][y] = 4

            new_path = find_shortest_path(
                temp_map,
                0,
                START_ROW
            )

            # 길이 존재하면 미리보기 표시
            if new_path:
                path_surface = pygame.Surface(
                    (WINDOW_WIDTH, WINDOW_HEIGHT),
                    pygame.SRCALPHA
                )

                for i in range(len(new_path) - 1):
                    start_pos = get_pos(
                        new_path[i][0],
                        new_path[i][1]
                    )

                    end_pos = get_pos(
                        new_path[i + 1][0],
                        new_path[i + 1][1]
                    )

                    pygame.draw.line(
                        path_surface,
                        (0, 255, 255, 120),   # 연한 하늘색
                        start_pos,
                        end_pos,
                        5
                    )

                self.screen.blit(path_surface, (0, 0))

    def draw_blank(self):
        # 가로
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (0, 0, WINDOW_WIDTH, MARGIN))
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (0, MARGIN+MAP_HEIGHT, WINDOW_WIDTH, MARGIN))
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (0, MARGIN*2+MAP_HEIGHT+STAT_HEIGHT, WINDOW_WIDTH, MARGIN))
        # 세로
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (0, 0, MARGIN, WINDOW_HEIGHT))
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (MARGIN+MAP_WIDTH, 0, MARGIN, WINDOW_HEIGHT))
    
    def play_bgm(self, bgm):
        if self.current_bgm == bgm:
            return
        try:
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.load(bgm)
            pygame.mixer.music.play(-1)
            self.current_bgm = bgm
        except Exception as e:
            print(f"BGM 에러: {e}")