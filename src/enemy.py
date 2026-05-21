import pygame
from map import *
from config import *

enemy_info = [
    (100, 10, 50), # hp, speed, gold,  / normal
    (100, 15, 70), # fast
    (200, 7, 100), # strong
    (1000, 10, 500) # boss
]

enemy_type = ["normal", "fast", "strong", "boss"]

def movex(tx, x, speed):
    if tx > x:
        x += speed
    else : 
        x -= speed
def movey(ty, y, speed):
    if ty > y:
        y += speed
    else : 
        y -= speed

class enemy:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.target_index = 0
        if type in enemy_type:
            self.hp = enemy_info[enemy_type.index(self.type)][0]
            self.speed = enemy_info[enemy_type.index(self.type)][1]
            self.gold = enemy_info[enemy_type.index(self.type)][2]


    def move(self):

        remain = self.speed

        tx, ty = get_pos(SHORTEST_PATH[self.target_index][0], SHORTEST_PATH[self.target_index][1])

        if self.x != tx:
            dist = abs(tx - self.x)

            if self.speed >= dist:
                self.x = tx
                remain -= dist
                self.target_index += 1
                tx, ty = get_pos(SHORTEST_PATH[self.target_index][0], SHORTEST_PATH[self.target_index][1])
                movey(ty, self.y, remain)
            else:
                movex(tx, self.x, self.speed)

        elif self.y != ty:

            dist = abs(ty - self.y)

            if remain >= dist:
                self.y = ty
                remain -= dist
                self.target_index += 1
                tx, ty = get_pos(SHORTEST_PATH[self.target_index][0], SHORTEST_PATH[self.target_index][1])
                movex(tx, self.x, remain)
            else:
                movey(ty, self.y, self.speed)

        else:
            self.target_index += 1

    def draw(self, screen):
        if self.type == "normal":
            pygame.draw.circle(screen, "green", (self.x, self.y), TILE_SIZE/2.2)
        if self.type == "fast":
            pygame.draw.circle(screen, "yellow", (self.x, self.y), TILE_SIZE/2.5)
        if self.type == "strong":
            pygame.draw.circle(screen, "red", (self.x, self.y), TILE_SIZE/2)
        if self.type == "boss":
            pygame.draw.circle(screen, "red", (self.x, self.y), TILE_SIZE/2 + 10)

        

    
    