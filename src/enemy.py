import pygame
from src.map import *
from src.config import *
import math

enemy_info = [
    (100, 15, 50), # hp, speed, gold,  / normal
    (100, 25, 70), # fast
    (200, 10, 100), # strong
    (1000, 30, 500) # boss
]

enemy_type = ["normal", "fast", "strong", "boss"]

def movex(tx, x, speed):
    if tx > x:
        x += speed
    else : 
        x -= speed
    return x
def movey(ty, y, speed):
    if ty > y:
        y += speed
    else : 
        y -= speed
    return y

class enemy:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.hp = 100
        self.max_hp = 100
        self.target_index = 1
        if type in enemy_type:
            self.hp = enemy_info[enemy_type.index(self.type)][0]
            self.max_hp = enemy_info[enemy_type.index(self.type)][0]
            self.speed = enemy_info[enemy_type.index(self.type)][1]
            self.gold = enemy_info[enemy_type.index(self.type)][2]


    def move(self, shortest_path,dt):
        # shortest_path = find_shortest_path(game_map, math.floor((self.x - MARGIN) / TILE_SIZE), math.floor((self.y - MARGIN) / TILE_SIZE))
        # tx, ty = get_pos(shortest_path[0][0], shortest_path[0][1])
        # tx2, ty2 = get_pos(shortest_path[1][0], shortest_path[1][1])
        # if tx == self.x:
        #     if (ty - self.y) * (ty2 - self.y) < 0:
        #         self.y = movey(ty2, self.y, self.speed * dt)


        remain = self.speed * dt
        # shortest_path = find_shortest_path(game_map, math.floor((self.x - MARGIN) / TILE_SIZE), math.floor((self.y - MARGIN) / TILE_SIZE))

        tx, ty = get_pos(shortest_path[self.target_index][0], shortest_path[self.target_index][1])

        if shortest_path[self.target_index][1] == shortest_path[self.target_index - 1][1]:
            dist = abs(tx - self.x)
            

            if remain >= dist:
                self.x = tx
                remain -= dist
                self.target_index += 1
                tx, ty = get_pos(shortest_path[self.target_index][0], shortest_path[self.target_index][1])
                if shortest_path[self.target_index][1] == shortest_path[self.target_index - 1][1]:
                    self.x = movex(tx, self.x, remain)
                else:
                    self.y = movey(ty, self.y, remain)
                
            else:
                self.x = movex(tx, self.x, self.speed * dt)

        elif shortest_path[self.target_index][0] == shortest_path[self.target_index - 1][0]:

            dist = abs(ty - self.y)

            if remain >= dist:
                self.y = ty
                remain -= dist
                self.target_index += 1
                tx, ty = get_pos(shortest_path[self.target_index][0], shortest_path[self.target_index][1])
                if shortest_path[self.target_index][1] == shortest_path[self.target_index - 1][1]:
                    self.x = movex(tx, self.x, remain)
                else:
                    self.y = movey(ty, self.y, remain)
            else:
                self.y = movey(ty, self.y, self.speed * dt)


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


        

    
    