import pygame
from src.entities.skill import Skill
from src.core.map import *
from src.core.config import *
import math

enemy_info = [
    (250, 45, 5), # hp, speed, gold,  / normal
    (200, 80, 8), # fast
    (500, 35, 10), # strong
    (12000, 20, 500) # boss
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
    def __init__(self, type, x, y, game_map, difficulty=None):
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
        self.difficulty = difficulty

        self.game_map = game_map

        if type in enemy_type:
            self.hp = enemy_info[enemy_type.index(self.type)][0]
            self.max_hp = enemy_info[enemy_type.index(self.type)][0]
            if self.difficulty == "hard":
                self.hp *= 1.5
                self.max_hp *= 1.5
            self.speed = enemy_info[enemy_type.index(self.type)][1]
            self.gold = enemy_info[enemy_type.index(self.type)][2]

    def update_shortest_path(self, game_map):
        grid_y = (self.y - MARGIN) / TILE_SIZE
        grid_x = (self.x - MARGIN) / TILE_SIZE
        
        logical_y = int(grid_y)
        logical_x = int(grid_x)
        
        if grid_y - logical_y > 0.5: logical_y += 1
        if grid_x - logical_x > 0.5: logical_x += 1
        
        new_path = find_shortest_path(game_map, logical_x, logical_y)
        
        if new_path:
            self.shortest_path = new_path
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
            
        if self.target_index >= len(self.shortest_path):
            return

        distance_to_move = self.speed * dt

        while distance_to_move > 0 and self.target_index < len(self.shortest_path):
            tx, ty = get_pos(self.shortest_path[self.target_index][0], self.shortest_path[self.target_index][1])

            dx = tx - self.x
            dy = ty - self.y
            
            distance_to_target = math.hypot(dx, dy)

            if distance_to_move >= distance_to_target:
                self.x = tx
                self.y = ty
                distance_to_move -= distance_to_target  
                self.target_index += 1  
            
            else:
                if distance_to_target > 0:
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

        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 220, 0), (bar_x, bar_y, hp_fill_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)


class BossSkill(Skill):
    def __init__(self, boss):
        self.boss = boss

        self.is_finished = False

        self.duration = 3.0
        self.timer = 0

        self.spawn_interval = 0.5
        self.spawn_timer = 0

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
                    "strong",
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
            TILE_SIZE / 2 + 10,
            5
        )