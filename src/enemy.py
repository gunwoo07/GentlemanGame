import pygame
from src.skill import Skill
from src.map import *
from src.config import *
import math

enemy_info = [
    (100, 45, 50), # hp, speed, gold,  / normal
    (100, 25, 70), # fast
    (200, 10, 100), # strong
    (1000, 30, 500) # boss
]

enemy_type = ["normal", "fast", "strong", "boss"]

def movex(tx, x, speed):
    if abs(tx - x) < speed:
        return tx, speed - abs(tx - x)
    elif tx > x:
        x += speed
    else : 
        x -= speed
    return x, 0

def movey(ty, y, speed):
    if abs(ty - y) < speed:
        return ty, speed - abs(ty - y)
    elif ty > y:
        y += speed
    else : 
        y -= speed
    return y, 0

class Enemy:
    def __init__(self, type, x, y, game_map):
        self.type = type
        self.x = x
        self.y = y
        self.hp = 100
        self.max_hp = 100
        self.target_index = 1
        self.shortest_path = self.update_shortest_path(game_map)
        self.skill_cooldown = 8
        self.skill_timer = 0
        self.is_invincible = False
        self.is_casting = False

        self.game_map = game_map

        if type in enemy_type:
            self.hp = enemy_info[enemy_type.index(self.type)][0]
            self.max_hp = enemy_info[enemy_type.index(self.type)][0]
            self.speed = enemy_info[enemy_type.index(self.type)][1]
            self.gold = enemy_info[enemy_type.index(self.type)][2]

    def update_shortest_path(self, game_map):
        # 1. 현재 픽셀 위치를 격자 단위(소수점 포함)로 변환
        grid_y = (self.y - MARGIN) / TILE_SIZE
        grid_x = (self.x - MARGIN) / TILE_SIZE
        
        # 2. 현재 정수 좌표(Tile Index) 구하기
        logical_y = int(grid_y)
        logical_x = int(grid_x)
        
        # 3. [핵심] 0.5 타일 이상 이동했다면 다음 타일을 시작점으로 간주
        if grid_y - logical_y > 0.5: logical_y += 1
        if grid_x - logical_x > 0.5: logical_x += 1
        
        # 4. 예측된 '논리적 위치'에서 새 경로 탐색
        # (기존 find_shortest_path의 인자 순서에 맞춰 grid_x, grid_y를 적절히 배치)
        new_path = find_shortest_path(game_map, logical_x, logical_y)
        
        if new_path:
            self.shortest_path = new_path
            # 5. 타겟 인덱스를 1로 설정하여 다음 칸으로 즉시 향하게 함
            self.target_index = 1
        return self.shortest_path
    
    def left_distance(self):
        if self.target_index >= len(self.shortest_path):
            return 0
        tx, ty = get_pos(self.shortest_path[self.target_index][0], self.shortest_path[self.target_index][1])
        return math.hypot(tx - self.x, ty - self.y) + (len(self.shortest_path) - self.target_index - 1) * TILE_SIZE
    
    def move(self, dt):
        if self.is_casting:
            return
            
        # 더 이상 이동할 경로가 없다면 탈출 (기지 도달)
        if self.target_index >= len(self.shortest_path):
            return

        # 이번 프레임에 이동해야 할 총 거리
        distance_to_move = self.speed * dt

        while distance_to_move > 0 and self.target_index < len(self.shortest_path):
            # 목적지 타일의 픽셀 위치 구하기
            tx, ty = get_pos(self.shortest_path[self.target_index][0], self.shortest_path[self.target_index][1])

            # 현재 위치에서 목적지까지의 x, y 거리
            dx = tx - self.x
            dy = ty - self.y
            
            # 목적지까지 남은 직선 거리 직선 거리 계산 (피타고라스)
            distance_to_target = math.hypot(dx, dy)

            # 1. 이번 프레임 이동 거리가 목적지까지 남은 거리보다 크거나 같다면 (목적지 도달)
            if distance_to_move >= distance_to_target:
                self.x = tx  # 목적지에 정확히 안착
                self.y = ty
                distance_to_move -= distance_to_target  # 남은 이동 거리 차감
                self.target_index += 1  # ★ 다음 타일을 목적지로 설정!
            
            # 2. 아직 목적지에 도달하지 못했다면 현재 방향으로 전진 후 종료
            else:
                if distance_to_target > 0:
                    # 방향 벡터를 이용해 정확한 속도로 이동
                    self.x += (dx / distance_to_target) * distance_to_move
                    self.y += (dy / distance_to_target) * distance_to_move
                distance_to_move = 0  

    def update(self, dt):
        if self.type != "boss":
            return None

        if self.is_casting:
            return None

        self.skill_timer += dt

        if self.skill_timer >= self.skill_cooldown:
            self.skill_timer = 0
            return BossSkill(self)

    def draw(self, screen):
        # 적 몸통
        if self.type == "normal":
            radius = int(TILE_SIZE / 2.2)
            color = "green"
        elif self.type == "fast":
            radius = int(TILE_SIZE / 2.5)
            color = "yellow"
        elif self.type == "strong":
            radius = int(TILE_SIZE / 2)
            color = "red"
        elif self.type == "boss":
            radius = int(TILE_SIZE / 2 + 10)
            color = "red"

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), radius)

        # 체력 바
        bar_width = radius * 2
        bar_height = 6
        bar_x = int(self.x - bar_width / 2)
        bar_y = int(self.y - radius - 12)

        hp_ratio = max(0, self.hp) / self.max_hp
        hp_fill_width = int(bar_width * hp_ratio)

        # 배경 바
        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
        # 체력 바
        pygame.draw.rect(screen, (0, 220, 0), (bar_x, bar_y, hp_fill_width, bar_height))
        # 테두리
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)


class BossSkill(Skill):
    def __init__(self, boss):
        self.boss = boss

        self.is_finished = False

        self.duration = 3.0
        self.timer = 0

        self.spawn_interval = 0.5
        self.spawn_timer = 0

        # 보스 상태
        self.boss.is_invincible = True
        self.boss.is_casting = True

    def move(self, dt, enemies):
        self.timer += dt
        self.spawn_timer += dt

        # 적 소환
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0

            enemies.append(
                Enemy(
                    "normal",
                    self.boss.x,
                    self.boss.y,
                    self.boss.game_map
                )
            )

        # 종료
        if self.timer >= self.duration:
            self.boss.is_invincible = False
            self.boss.is_casting = False
            self.is_finished = True

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (180, 0, 255),
            (int(self.boss.x), int(self.boss.y)),
            60,
            5
        )