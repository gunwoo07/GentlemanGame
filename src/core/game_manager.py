import sys
import os
import pickle
import json
import copy
import pygame
from src.core.config import *
from src.core.map import *
from src.core.renderer import Renderer
from src.entities.tower import Tower, Archer, Cannon, Frost, create_tower
from src.entities.enemy import Enemy
from src.ui.screens.title_screen import TitleScreen

ENEMY_SPAWN = pygame.USEREVENT + 1
ENEMY_SPAWN_INTERVAL = 1000 # 1초마다 적 생성


class Game:
    def __init__(self):
        # pygame 초기화
        pygame.init()
        pygame.display.set_caption("gentleman's tower defense")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # 렌더링 인스턴스 생성
        self.renderer = Renderer(self.screen)

        # 게임구성 정보
        self.game_map = [[]]
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.skills = []
        self.path = [[]]
        self.gold = 200
        self.hp = 100
        self.wave_data = [[]]
        self.wave_index = 0
        self.before_game_state = {}; self.update_before_game_state() # 저장 시 필요함

        # 실행 중 필요한 정보
        self.current_message = None
        self.wave_data_progressed = copy.deepcopy(self.wave_data)
        self.selected_tower = None
        self.selected_tower_btn = None
        self.is_wave = False

    def update_before_game_state(self):
        self.before_game_state = {
            "game_map": self.game_map,
            "towers": self.towers,
            "enemies": [],
            "bullets": [],
            "skills": [],
            "path": self.path,
            "gold": self.gold,
            "hp": self.hp,
            "wave_data": self.wave_data,
            "wave_index": self.wave_index,
            "current_message": None
        }

    def export_game_state(self):
        return {
            "game_map": self.game_map,
            "towers": self.towers,
            "enemies": self.enemies,
            "bullets": self.bullets,
            "skills": self.skills,
            "path": self.path,
            "gold": self.gold,
            "hp": self.hp,
            "wave_data": self.wave_data,
            "wave_index": self.wave_index,
            "current_message": self.current_message
        }
    
    def inactivate_selected_tower(self):
        if self.selected_tower:
            self.selected_tower.is_selected = False
            self.selected_tower = None

    def activate_selected_tower(self, tower):
        tower.is_selected = True
        self.selected_tower = tower
    
    def inactivate_selected_tower_btn(self):
        if self.selected_tower_btn:
            self.selected_tower_btn.activation = False
            self.selected_tower_btn = None
    
    def activate_selected_tower_btn(self, tower_btn):
        self.selected_tower_btn = tower_btn
        self.selected_tower_btn.activation = True
    
    def save(self):
        # 실행중 필요한 정보 초기화
        self.inactivate_selected_tower()
        self.inactivate_selected_tower_btn()

        # pickle로 게임 정보 저장
        try:
            with open(SAVEGAME_PATH, "wb") as f:
                pickle.dump(self.before_game_state, f)
            print("게임이 성공적으로 저장되었습니다!")
        except Exception as e:
            print(f"게임 저장 중 오류 발생: {e}")

    def save_score(self, name, score):
        rankings = []

        if os.path.exists(RANKING_PATH):
            try:
                with open(RANKING_PATH, 'r', encoding='utf-8') as f:
                    rankings = json.load(f)
            except (json.JSONDecodeError, Exception):
                rankings = []
        
        new_entry = {
            'name': name,
            'score': score
        }
        rankings.append(new_entry)
        rankings.sort(key=lambda x: x.get('score', 0), reverse=True)

        try:
            with open(RANKING_PATH, 'w', encoding='utf-8') as f:
                json.dump(rankings, f, ensure_ascii=False, indent=4)
                return True
        except:
            return False

    def load(self):
        try:
            with open(SAVEGAME_PATH, "rb") as f:
                save_data = pickle.load(f)
            self.game_map = save_data.get("game_map", [])
            self.towers = save_data.get("towers", [])
            self.enemies = save_data.get("enemies", [])
            self.bullets = save_data.get("bullets", [])
            self.skills = save_data.get("skills", [])
            self.path = save_data.get("path", [])
            self.gold = save_data.get("gold", 100)
            self.hp = save_data.get("hp", 100)
            self.wave_data = save_data.get("wave_data", [])
            self.wave_index = save_data.get("wave_index", 0)
            self.current_message = save_data.get("current_message", None)
            self.update_before_game_state()
            self.wave_data_progressed = copy.deepcopy(self.wave_data)
            
            print("게임을 성공적으로 불러왔습니다!")
            return True
        except Exception as e:
            print(f"불러오기 중 오류 발생: {e}")
            return False
    
    def pause(self):
        print("멈춤")
    
    def get_score(self):
        return (self.wave_index+1) + self.hp + self.gold

    def game_over(self):
        score = self.get_score()
        result = self.renderer.show_result(False, score, self.wave_index)
        if result[0] == 'exit':
            self.quit()
        elif result[0] == 'confirm':
            self.save_score(result[1], score)
            self.quit()

    def game_clear(self):
        score = self.get_score()
        result = self.renderer.show_result(True, score, self.wave_index)
        if result[0] == 'exit':
            self.quit()
        elif result[1] == 'confirm':
            self.save_score(result[1], score)
            self.quit()

    def add_message(self, text, duration=1.5):
        self.current_message = {
            'text': text,
            'timer': duration,
            'max_duration': duration
        }
    def quit(self):
        sys.exit(0)

    def rest_update(self, dt):
        if self.current_message:
            self.current_message['timer'] -= dt
            if self.current_message['timer'] <= 0:
                self.current_message = None

    def wave_update(self, dt):
        # 종료 조건
        if len(self.wave_data_progressed[self.wave_index]) == 0 and len(self.enemies) == 0:
            self.bullets = []
            self.skills = []
            self.enemies = []
            self.is_wave = False
            self.gold += 100 + 20*(self.wave_index-1)

        if self.current_message:
            self.current_message['timer'] -= dt
            if self.current_message['timer'] <= 0:
                self.current_message = None
        
        # enemy, tower, bullet, skill update
        for enemy in self.enemies:
            if enemy.hp <= 0:
                self.gold += enemy.gold
                self.enemies.remove(enemy)
            elif enemy.target_index >= len(enemy.shortest_path):
                self.hp -= 10
                self.enemies.remove(enemy)
        for enemy in self.enemies:
            
            enemy.move(dt)
            
            result = enemy.update(dt)

            if result:
                self.skills.append(result)
        
        for tower in self.towers:
            result = tower.update(dt, self.enemies)
            if result[0]:
                self.bullets.append(result[0])
            if result[1]:
                self.skills.append(result[1])
        
        self.bullets = [b for b in self.bullets if not b.is_finished]
        for bullet in self.bullets:
            bullet.move(dt)

        self.skills = [s for s in self.skills if not s.is_finished]
        for skill in self.skills:
            skill.move(dt, self.enemies)

    def rest_event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.save()
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_wave = True
                    pygame.time.set_timer(ENEMY_SPAWN, ENEMY_SPAWN_INTERVAL)
                    return
                elif event.key == pygame.K_ESCAPE:
                    self.save()
                    self.play()
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    grid_pos = find_grid_pos(event.pos)
                    # map 영역을 클릭했을 때
                    if grid_pos:
                        # 타워 버튼이 선택되어있고, 빈칸을 클릭했을 때
                        if self.selected_tower_btn and self.game_map[grid_pos[0]][grid_pos[1]] == 0:
                            # 타워 설치
                            new_tower = create_tower(self.selected_tower_btn.tower_class.type_name, grid_pos[0], grid_pos[1])
                            self.towers.append(new_tower)
                            self.game_map[grid_pos[0]][grid_pos[1]] = 4
                            # 그 외
                            self.inactivate_selected_tower() # 타워 비활성화
                            self.inactivate_selected_tower_btn() # 타워버튼 비활성화
                            self.gold -= new_tower.cost # 골드 차감
                            self.activate_selected_tower(new_tower) # 타워 활성화
                            self.path = find_shortest_path(self.game_map, 0, START_ROW) # 최단경로 재탐색
                        # 타워가 선택되어있고, 타워를 클릭했을 때
                        elif self.selected_tower and self.game_map[grid_pos[0]][grid_pos[1]] == 4:
                            for tower in self.towers:
                                if tower.rect.collidepoint(event.pos):
                                    if tower != self.selected_tower and tower.type_name == self.selected_tower.type_name \
                                        and tower.level == self.selected_tower.level and tower.level < tower.max_level:
                                        # 타워 병합
                                        tower.merge(self.selected_tower)
                                        self.game_map[self.selected_tower.grid_x][self.selected_tower.grid_y] = 0
                                        self.towers.remove(self.selected_tower)
                                        # 그 외
                                        self.inactivate_selected_tower() # 기존 타워 비활성화
                                        self.activate_selected_tower(tower) # 병합한 타워 활성화
                                        self.path = find_shortest_path(self.game_map, 0, START_ROW) # 최단 경로 재탐색
                                    else:
                                        self.inactivate_selected_tower() # 타워 비활성화
                                        self.activate_selected_tower(tower)
                        # 타워가 선택되어있지 않고, 타워를 클릭했을 때
                        elif self.game_map[grid_pos[0]][grid_pos[1]] == 4:
                            for tower in self.towers:
                                if tower.rect.collidepoint(event.pos):
                                    self.activate_selected_tower(tower)
                    # stat 영역 - 타워 버튼 클릭했을 때
                    for tower_btn in self.renderer.tower_btns.values():
                        if tower_btn.rect.collidepoint(event.pos):
                            self.inactivate_selected_tower() # 타워 해제
                            self.inactivate_selected_tower_btn() # 타워 버튼 해제
                            # 골드가 충분한지 확인
                            if self.gold < tower_btn.tower_class.cost:
                                self.add_message("골드가 부족합니다.")
                            else:
                                self.activate_selected_tower_btn(tower_btn) # 타워 버튼 활성화
                    # stat 영역 - 레벨업 버튼 클릭했을 때
                    if self.selected_tower:
                        if self.renderer.levelup_btn.rect.collidepoint(event.pos):
                            # 레벨업이 가능한지 확인
                            if not self.selected_tower.level < self.selected_tower.max_level:
                                self.add_message("이미 최고레벨입니다.")
                            elif self.gold < self.selected_tower.LEVEL_DATA[self.selected_tower.level + 1]["cost"]:
                                self.add_message("골드가 부족합니다.")
                            else:
                                self.gold -= self.selected_tower.LEVEL_DATA[self.selected_tower.level + 1]["cost"]
                                self.selected_tower.level_up()
                    self.update_before_game_state()
                elif event.button == 3:
                    self.inactivate_selected_tower() # 타워 해제
                    self.inactivate_selected_tower_btn() # 타워 버튼 해제

    def wave_event_handler(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.save()
                    self.quit()
                elif event.type == ENEMY_SPAWN:
                    if len(self.wave_data_progressed[self.wave_index]) == 0:
                        pygame.time.set_timer(ENEMY_SPAWN, 0)
                    else:
                        enemy_type = self.wave_data_progressed[self.wave_index].pop(0)
                        self.enemies.append(Enemy(enemy_type, *get_pos(0, START_ROW), self.game_map))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.pause()
                    elif event.key == pygame.K_ESCAPE:
                        self.save()
                        self.go_title()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        grid_pos = find_grid_pos(event.pos)
                        # map 영역을 클릭했을 때
                        if grid_pos:
                            # 타워 버튼이 선택되어있고, 빈칸을 클릭했을 때
                            if self.selected_tower_btn and self.game_map[grid_pos[0]][grid_pos[1]] == 0:
                                # 타워 설치
                                new_tower = create_tower(self.selected_tower_btn.tower_class.type_name, grid_pos[0], grid_pos[1])
                                self.towers.append(new_tower)
                                self.game_map[grid_pos[0]][grid_pos[1]] = 4
                                # 그 외
                                self.inactivate_selected_tower() # 타워 비활성화
                                self.inactivate_selected_tower_btn() # 타워버튼 비활성화
                                self.gold -= new_tower.cost # 골드 차감
                                self.activate_selected_tower(new_tower) # 타워 활성화
                                for enemy in self.enemies: enemy.update_shortest_path(self.game_map) # enemy들 최단경로 재탐색
                            # 타워가 선택되어있고, 타워를 클릭했을 때
                            elif self.selected_tower and self.game_map[grid_pos[0]][grid_pos[1]] == 4:
                                for tower in self.towers:
                                    if tower.rect.collidepoint(event.pos):
                                        if tower != self.selected_tower and tower.type_name == self.selected_tower.type_name \
                                            and tower.level == self.selected_tower.level and tower.level < tower.max_level:
                                            # 타워 병합
                                            tower.merge(self.selected_tower)
                                            self.game_map[self.selected_tower.grid_x][self.selected_tower.grid_y] = 0
                                            self.towers.remove(self.selected_tower)
                                            # 그 외
                                            self.inactivate_selected_tower() # 기존 타워 비활성화
                                            self.activate_selected_tower(tower) # 병합한 타워 활성화
                                            for enemy in self.enemies: enemy.update_shortest_path(self.game_map) # enemy들 최단경로 재탐색
                                        else:
                                            self.inactivate_selected_tower() # 타워 비활성화
                                            self.activate_selected_tower(tower) # 타워 활성화
                            # 타워가 선택되어있지 않고, 타워를 클릭했을 때
                            elif self.game_map[grid_pos[0]][grid_pos[1]] == 4:
                                for tower in self.towers:
                                    if tower.rect.collidepoint(event.pos):
                                        self.activate_selected_tower(tower) # 타워 활성화
                        # stat 영역 - 타워 버튼 클릭했을 때
                        for tower_btn in self.renderer.tower_btns.values():
                            if tower_btn.rect.collidepoint(event.pos):
                                self.inactivate_selected_tower() # 타워 해제
                                self.inactivate_selected_tower_btn() # 타워 버튼 해제
                                # 골드가 충분한지 확인
                                if self.gold < tower_btn.tower_class.cost:
                                    self.add_message("골드가 부족합니다.")
                                else:
                                    self.activate_selected_tower_btn(tower_btn) # 타워 버튼 활성화
                        # stat 영역 - 레벨업 버튼 클릭했을 때
                        if self.selected_tower:
                            if self.renderer.levelup_btn.rect.collidepoint(event.pos):
                                # 레벨업이 가능한지 확인
                                if not self.selected_tower.level < self.selected_tower.max_level:
                                    self.add_message("이미 최고레벨입니다.")
                                elif self.gold < self.selected_tower.LEVEL_DATA[self.selected_tower.level + 1]["cost"]:
                                    self.add_message("골드가 부족합니다.")
                                else:
                                    self.gold -= self.selected_tower.LEVEL_DATA[self.selected_tower.level + 1]["cost"]
                                    self.selected_tower.level_up()
                    elif event.button == 3:
                        self.inactivate_selected_tower() # 타워 해제
                        self.inactivate_selected_tower_btn() # 타워 버튼 해제

    def play(self):
        for i in range(self.wave_index, len(self.wave_data)):
            self.wave_index = i
            self.path = find_shortest_path(self.game_map, 0, START_ROW)
            self.update_before_game_state()
            while not self.is_wave:
                dt = self.clock.tick(60) / 1000
                self.rest_update(dt)
                self.rest_event_handler()
                self.renderer.render(self.export_game_state())
                pygame.display.flip()
            self.update_before_game_state()
            while self.is_wave:
                dt = self.clock.tick(60) / 1000

                if self.hp <= 0:
                    self.is_wave = False
                    self.game_over()
                    return
                
                self.wave_event_handler()
                self.wave_update(dt)
                self.renderer.render(self.export_game_state())
                pygame.display.flip()
            
    def run(self):
        # 타이틀 띄우기
        choice = self.renderer.show_title()
        if choice == "exit":
            self.quit()
        elif choice == "continue":
            if not self.load():
                self.quit()
        elif choice == "ranking":
            choice = self.renderer.show_ranking()
            if choice == 'exit':
                self.quit()
            elif choice == 'back':
                self.run()
                return
            self.run()
        elif choice == "easy":
            self.wave_data = [
                ["normal", "normal", "normal", "normal", "normal"],
                ["normal", "normal", "normal", "normal", "fast", "fast", "fast", "fast", "fast", "fast"],
                ["strong", "strong", "strong", "normal", "normal", "normal", "normal", "fast", "fast", "fast"],
                ["strong", "strong", "strong", "strong", "strong", "strong", "fast", "fast", "fast", "fast", "fast"],
                ["strong", "strong", "strong", "boss"]
            ]
            self.wave_data_progressed = copy.deepcopy(self.wave_data)
            self.game_map = [
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
            ]

        elif choice == "hard":
            self.wave_data = [
                ["normal", "normal", "normal", "normal", "normal", "normal", "normal"],
                ["normal", "normal", "normal", "normal", "fast", "fast", "fast", "fast", "fast", "fast","fast","fast","fast"],
                ["strong", "strong", "strong", "strong", "strong","strong", "normal", "normal", "normal", "normal", "fast", "fast", "fast"],
                ["strong", "strong", "strong", "strong", "strong", "strong", "fast", "fast", "fast", "fast", "fast", "strong", "strong", "strong", "strong", "strong", "strong", "fast", "fast", "fast"],
                ["strong", "strong", "strong", "strong", "strong", "strong", "strong", "boss"]
            ]
            self.wave_data_progressed = copy.deepcopy(self.wave_data)
            self.game_map = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
                [2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3],
                [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]


        self.update_before_game_state()

        # 웨이브 시작
        self.play()
        # 게임 오버 혹은 랭킹 페이지 저장
        self.game_clear()

# game_state = {
#     "game_map": [[]],
#     "towers": [],
#     "enemies": [],
#     "bullets": [],
#     "skills": [],
#     "path": [[]],
#     "gold": 0,
#     "hp": 0,
#     "wave_data": [],
#     "wave_index": 0,
# }