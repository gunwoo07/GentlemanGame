import pygame
from src.map import *
from src.config import *

enemy_info = [
    (100, 29, 50), # hp, speed, gold,  / normal
    (100, 45, 70), # fast
    (200, 40, 100), # strong
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
        self.target_index = 1
        if type in enemy_type:
            self.hp = enemy_info[enemy_type.index(self.type)][0]
            self.speed = enemy_info[enemy_type.index(self.type)][1]
            self.gold = enemy_info[enemy_type.index(self.type)][2]


    def move(self, shortest_path, dt):
        print(self.target_index)

        remain = self.speed * dt

        tx, ty = get_pos(shortest_path[self.target_index][0], shortest_path[self.target_index][1])

        if shortest_path[self.target_index][1] == shortest_path[self.target_index - 1][1]:
            dist = abs(tx - self.x)
            

            if remain >= dist:
                self.x = tx
                remain -= dist
                print(1)
                print(remain, dist)
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
                print(2)
                print(remain, dist)
                self.target_index += 1
                tx, ty = get_pos(shortest_path[self.target_index][0], shortest_path[self.target_index][1])
                if shortest_path[self.target_index][1] == shortest_path[self.target_index - 1][1]:
                    self.x = movex(tx, self.x, remain)
                else:
                    self.y = movey(ty, self.y, remain)
            else:
                self.y = movey(ty, self.y, self.speed * dt)


    def draw(self, screen):
        if self.type == "normal":
            pygame.draw.circle(screen, "green", (self.x, self.y), TILE_SIZE/2.2)
        if self.type == "fast":
            pygame.draw.circle(screen, "yellow", (self.x, self.y), TILE_SIZE/2.5)
        if self.type == "strong":
            pygame.draw.circle(screen, "red", (self.x, self.y), TILE_SIZE/2)
        if self.type == "boss":
            pygame.draw.circle(screen, "red", (self.x, self.y), TILE_SIZE/2 + 10)

        

    
    