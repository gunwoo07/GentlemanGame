import pygame
from src.map import *
from src.enemy import *
from src.tower import Tower, Archer, Cannon, Frost, create_tower
from src.renderer import *
from src.title_screen.title_screen import TitleScreen
import sys
import pickle



wave_list = [
    ["normal", "normal", "normal", "normal", "normal", "normal", "normal"],
    ["normal", "normal", "normal", "normal", "fast", "fast", "fast", "fast", "fast", "fast"],
    ["strong", "strong", "strong", "normal", "normal", "normal", "normal", "fast", "fast", "fast"],
    ["strong", "strong", "strong", "strong", "strong", "strong", "fast", "fast", "fast", "fast", "fast"],
    ["strong", "strong", "strong", "boss"]
]

ENEMY_SPAWN = pygame.USEREVENT + 1

class Game:
    def __init__(self):
        pygame.init()
        self.renderer = Renderer(pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)))
        pygame.display.set_caption("gentleman's tower defense")
        self.clock = pygame.time.Clock()
        self.game_map = game_map[:]
        self.running = True
        self.enemy_list = []
        self.tower_list = []
        self.bullet_list = []
        self.skill_list = []
        self.hp = 100
        self.wave = 1
        self.gold = 100
        self.is_wave = False
        self.selected_tower_btn = None
        self.selected_tower = None # 
    
    def save(self):
        if self.selected_tower:
            self.selected_tower.is_selected = False
        save_data = {
            "map": self.game_map,
            "towers": self.tower_list,
            "enemies": self.enemy_list,
            "path": self.shortest_path,
            "bullets": self.bullet_list,
            "skills": self.skill_list,
            "stat": {
                "gold" : self.gold,
                "hp" : self.hp,
                "wave" : self.wave,
                "max_wave" : len(wave_list)
            },
            "wave_list": wave_list
        }
        try:
            with open("savegame.pkl", "wb") as f:
                pickle.dump(save_data, f)
            print("게임이 성공적으로 저장되었습니다!")
        except Exception as e:
            print(f"저장 중 오류 발생: {e}")

    def load(self):
        global wave_list
        try:
            with open("savegame.pkl", "rb") as f:
                save_data = pickle.load(f)
            
            # stat 딕셔너리에서 데이터 복원
            stats = save_data.get("stat", {})
            self.hp = stats.get("hp", 100)
            self.wave = stats.get("wave", 0)
            self.gold = stats.get("gold", 100)
            
            # 나머지 리스트 및 데이터 복원 (save의 키와 일치)
            self.tower_list = save_data.get("towers", [])
            self.enemy_list = save_data.get("enemies", [])
            self.bullet_list = save_data.get("bullets", [])
            self.skill_list = save_data.get("skills", [])
            self.game_map = save_data.get("map", game_map[:])
            self.shortest_path = save_data.get("path", [])
            self.is_wave = False # save 데이터에 없으므로 기본값 설정
            wave_list = save_data.get("wave_list", [])
            print("게임을 성공적으로 불러왔습니다!")
            return True
        except FileNotFoundError:
            print("저장된 게임 파일을 찾을 수 없습니다.")
            return False
        except Exception as e:
            print(f"불러오기 중 오류 발생: {e}")
            return False
    
    def go_title(self):
        print('go title! 구현 안함')

    def quit(self):
        sys.exit()

    def pause(self):
        print('pause 구현 안함')

    def game_over(self):
        print('game over 구현 안함ㅜ')

    def finish(self):
        print("아직 구현 안함")
    def update(self, dt):
        # 종료 조건
        if len(wave_list[self.wave-1]) == 0 and len(self.enemy_list) == 0:
            self.bullet_list = []
            self.skill_list = []
            self.enemy_list = []
            self.is_wave = False
        # enemy, tower, bullet, skill update
        for enemy in self.enemy_list:
            if enemy.hp <= 0:
                self.gold += enemy.gold
                self.enemy_list.remove(enemy)
            elif enemy.target_index >= len(enemy.shortest_path):
                self.hp -= 10
                self.enemy_list.remove(enemy)
        for enemy in self.enemy_list:
            enemy.move(dt)
        
        for tower in self.tower_list:
            result = tower.update(dt, self.enemy_list)
            if result[0]:
                self.bullet_list.append(result[0])
            if result[1]:
                self.skill_list.append(result[1])
        
        self.bullet_list = [b for b in self.bullet_list if not b.is_finished]
        for bullet in self.bullet_list:
            bullet.move(dt)

        self.skill_list = [s for s in self.skill_list if not s.is_finished]
        for skill in self.skill_list:
            skill.move(dt, self.enemy_list)

    def find_grid_pos(self, pos):
        if not (MARGIN <= pos[0] <= MARGIN+MAP_WIDTH and MARGIN <= pos[1] <= MARGIN+MAP_HEIGHT):
            return None
        return ((pos[1]-MARGIN)//TILE_SIZE, (pos[0]-MARGIN)//TILE_SIZE)
            
    def inactivate_selected_tower(self):
        if self.selected_tower:
            self.selected_tower.is_selected = False
            self.selected_tower = None

    def rest_event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.save()
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # wave 시작
                    self.is_wave = True
                    pygame.time.set_timer(ENEMY_SPAWN, 3000)
                elif event.key == pygame.K_ESCAPE: # 게임 나가기
                    self.save()
                    self.go_title()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 좌클릭
                    # map 영역
                    grid_pos = self.find_grid_pos(event.pos)
                    if grid_pos:
                        if self.selected_tower_btn and self.game_map[grid_pos[0]][grid_pos[1]] == 0:
                            self.inactivate_selected_tower() # 선택된 타워 해제
                            new_tower = create_tower(self.selected_tower_btn.tower_class.type_name, grid_pos[0], grid_pos[1]) # 새 타워 건설
                            self.tower_list.append(new_tower)
                            self.game_map[grid_pos[0]][grid_pos[1]] = 4
                            self.gold -= new_tower.cost
                            new_tower.is_selected = True # 건설한 타워 활성화
                            self.selected_tower = new_tower
                            self.selected_tower_btn.activation = False # 타워 버튼 비활성화
                            self.selected_tower_btn = None
                            self.shortest_path = find_shortest_path(game_map, 0, START_ROW) # 최단경로 재탐색
                        elif self.selected_tower and self.game_map[grid_pos[0]][grid_pos[1]] == 4: # 선택한 부분에 타워가 있다면
                            for tower in self.tower_list:
                                if tower.rect.collidepoint(event.pos):
                                    if tower != self.selected_tower and tower.type_name == self.selected_tower.type_name and tower.level == self.selected_tower.level and tower.level < tower.max_level:
                                        tower.merge(self.selected_tower) # 타워 merge
                                        self.game_map[self.selected_tower.grid_x][self.selected_tower.grid_y] = 0
                                        self.tower_list.remove(self.selected_tower)
                                        self.selected_tower = tower # merge한 타워 활성
                                        self.selected_tower.is_selected = True
                                        self.shortest_path = find_shortest_path(game_map, 0, START_ROW) # 최단경로 재탐색
                                    else:
                                        self.selected_tower.is_selected = False # 기존에 선택되어있던 타워 비활성화
                                        self.selected_tower = tower # 새로운 타워 활성화
                                        self.selected_tower.is_selected = True
                        elif self.game_map[grid_pos[0]][grid_pos[1]] == 4: # 선택한 부분에 타워가 있다면
                            for tower in self.tower_list:
                                if tower.rect.collidepoint(event.pos):
                                    self.selected_tower = tower # 선택한 타워 활성화
                                    self.selected_tower.is_selected = True

                    # 타워 버튼
                    for tower_btn in self.renderer.tower_btns.values():
                        if tower_btn.rect.collidepoint(event.pos):
                            if self.selected_tower: # 선택된 타워 해제
                                self.selected_tower.is_selected = False
                                self.selected_tower = None
                            if self.selected_tower_btn: # 선택된 버튼 해제
                                self.selected_tower_btn.activation = False
                                self.selected_tower_btn = None
                            # 골드가 있는지 확인
                            if self.gold < tower_btn.tower_class.cost:
                                print('골드가 부족합니다.')
                            else:
                                self.selected_tower_btn = tower_btn # 선택된 타워 버튼 활성화
                                tower_btn.activation = True

                    # 레벨업 버튼(if selected_tower)
                    if self.selected_tower:
                        if self.renderer.levelup_btn.rect.collidepoint(event.pos):
                            # 레벨이 레벨업 가능한지, 골드가 충분한지 확인
                            if not self.selected_tower.level < self.selected_tower.max_level:
                                print('이미 최고레벨 입니다.')
                            elif self.gold < self.selected_tower.LEVEL_DATA[self.selected_tower.level+1]['cost']:
                                print('골드가 부족합니다.')
                            else:
                                self.selected_tower.level_up()
                
                # 취소 버튼
                elif event.button == 3:
                    if self.selected_tower: # 선택된 타워 해제
                        self.selected_tower.is_selected = False
                        self.selected_tower = None
                    if self.selected_tower_btn: # 선택된 버튼 해제
                        self.selected_tower_btn.activation = False
                        self.selected_tower_btn = None

    def wave_event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 저장 및 프로그램 종료
                pygame.quit()
                self.save()
                self.quit()
            elif event.type == ENEMY_SPAWN: # 적 생성
                if len(wave_list[self.wave-1]) == 0: # 생성할 적이 있을 때만
                    pygame.time.set_timer(ENEMY_SPAWN, 0)
                else:
                    enemy_type = wave_list[self.wave-1].pop(0)
                    self.enemy_list.append(Enemy(enemy_type, *get_pos(0, START_ROW)))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.pause()
                elif event.key == pygame.K_ESCAPE:
                    self.save()
                    self.go_title()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # map 영역
                    grid_pos = self.find_grid_pos(event.pos)
                    if grid_pos:
                        if self.selected_tower_btn and self.game_map[grid_pos[0]][grid_pos[1]] == 0:
                            if self.selected_tower: # 기존 선택된 타워 비활성화
                                self.selected_tower_btn.activation = False
                                self.selected_tower_btn = None
                            new_tower = create_tower(self.selected_tower_btn.tower_class.type_name, grid_pos[0], grid_pos[1]) # 새 타워 건설
                            self.tower_list.append(new_tower)
                            self.game_map[grid_pos[0]][grid_pos[1]] = 4
                            self.gold -= new_tower.cost
                            new_tower.is_selected = True # 건설한 타워 활성화
                            self.selected_tower = new_tower
                            self.selected_tower_btn.activation = False # 타워 버튼 비활성화
                            self.selected_tower_btn = None
                            for enemy in self.enemy_list: enemy.update_shortest_path() # enemy들 최단경로 재탐색
                        elif self.selected_tower and self.game_map[grid_pos[0]][grid_pos[1]] == 4: # 선택한 부분에 타워가 있다면
                            for tower in self.tower_list:
                                if tower.rect.collidepoint(event.pos):
                                    if tower != self.selected_tower and tower.type_name == self.selected_tower.type_name and tower.level == self.selected_tower.level and tower.level < tower.max_level:
                                        tower.merge(self.selected_tower) # 타워 merge
                                        self.game_map[self.selected_tower.grid_x][self.selected_tower.grid_y] = 0
                                        self.tower_list.remove(self.selected_tower)
                                        self.selected_tower = tower # merge한 타워 활성
                                        self.selected_tower.is_selected = True
                                        for enemy in self.enemy_list: enemy.update_shortest_path() # enemy들 최단경로 재탐색
                                    else:
                                        self.selected_tower.is_selected = False # 기존에 선택되어있던 타워 비활성화
                                        self.selected_tower = tower # 새로운 타워 활성화
                                        self.selected_tower.is_selected = True
                        elif self.game_map[grid_pos[0]][grid_pos[1]] == 4: # 선택한 부분에 타워가 있다면
                            for tower in self.tower_list:
                                if tower.rect.collidepoint(event.pos):
                                    self.selected_tower = tower # 선택한 타워 활성화
                                    self.selected_tower.is_selected = True

                    # 타워 버튼
                    for tower_btn in self.renderer.tower_btns.values():
                        if tower_btn.rect.collidepoint(event.pos):
                            if self.selected_tower: # 선택된 타워 해제
                                self.selected_tower.is_selected = False
                                self.selected_tower = None
                            if self.selected_tower_btn: # 선택된 버튼 해제
                                self.selected_tower_btn.activation = False
                                self.selected_tower_btn = None
                            # 골드가 있는지 확인
                            if self.gold < tower_btn.tower_class.cost:
                                print('골드가 부족합니다.')
                            else:
                                self.selected_tower_btn = tower_btn # 선택된 타워 버튼 활성화
                                tower_btn.activation = True

                    # 레벨업 버튼(if selected_tower)
                    if self.selected_tower:
                        if self.renderer.levelup_btn.rect.collidepoint(event.pos):
                            # 레벨이 레벨업 가능한지, 골드가 충분한지 확인
                            if not self.selected_tower.level < self.selected_tower.max_level:
                                print('이미 최고레벨 입니다.')
                            elif self.gold < self.selected_tower.LEVEL_DATA[self.selected_tower.level+1]['cost']:
                                print('골드가 부족합니다.')
                            else:
                                self.selected_tower.level_up()
                
                # 취소 버튼
                elif event.button == 3:
                    if self.selected_tower: # 선택된 타워 해제
                        self.selected_tower.is_selected = False
                        self.selected_tower = None
                    if self.selected_tower_btn: # 선택된 버튼 해제
                        self.selected_tower_btn.activation = False
                        self.selected_tower_btn = None
    def play(self):
        # title screen
        title = TitleScreen(self.renderer.screen)
        choice = title.run()
        
        if choice == "exit":
            self.quit()
        elif choice == "continue":
            if not self.load():
                # 불러오기 실패 시 새 게임으로 진행하거나 타이틀로 돌아감
                pass
        elif choice == "ranking":
            # 랭킹 페이지 구현 전이므로 메시지만 출력하거나 타이틀로 돌아감
            print("랭킹 페이지는 아직 구현되지 않았습니다.")
            return self.play() # 다시 타이틀로

        # wave part(rest -> wave -> rest -> wave -> ... -> wave -> "finish")
        for i in range(self.wave-1, len(wave_list)):
            # rest part
            self.is_wave = False
            self.wave = i + 1
            self.shortest_path = find_shortest_path(game_map, 0, START_ROW) # 건물이 새로 생겼을 때
            while not self.is_wave:
                self.clock.tick(60)
                self.rest_event_handler()
                game_state = {
                    "map":game_map,
                    "towers":self.tower_list,
                    "enemies":self.enemy_list,
                    "path":self.shortest_path,
                    "bullets": self.bullet_list,
                    "skills": self.skill_list,
                    "stat": {
                        "gold" : self.gold,
                        "hp" : self.hp,
                        "wave" : self.wave,
                        "max_wave" : len(wave_list)
                    }
                }
                self.renderer.render(game_state)
                pygame.display.flip()
            while self.is_wave:
                self.clock.tick(60)
                dt = self.clock.get_time() / 1000

                if self.hp <= 0:
                    self.game_over()
                    return
                
                self.wave_event_handler()
                self.update(dt)
                
                game_state = {
                    "map":game_map,
                    "towers":self.tower_list,
                    "enemies":self.enemy_list,
                    "path":self.shortest_path,
                    "bullets": self.bullet_list,
                    "skills": self.skill_list,
                    "stat": {
                        "gold" : self.gold,
                        "hp" : self.hp,
                        "wave" : self.wave,
                        "max_wave" : len(wave_list)
                    }
                }

                self.renderer.render(game_state)
                pygame.display.flip()
        # saving part
        
        # while self.running:
        #     self.clock.tick(60)
        #     dt = self.clock.get_time() / 1000

            

            
        #     self.handle_event()
        #     self.update(dt)
            

        #     game_state = {
        #         "map":game_map,
        #         "towers":self.tower_list,
        #         "enemies":self.enemy_list,
        #         "path":self.shortest_path,
        #         "bullets": self.bullet_list,
        #         "skills": self.skill_list,
        #         "stat": {
        #             "gold" : self.gold,
        #             "hp" : self.hp,
        #             "wave" : self.wave,
        #             "max_wave" : 5 
        #         }
        #     }




    
        #     self.renderer.render(game_state)
        #     pygame.display.flip()

        