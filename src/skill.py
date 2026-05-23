import pygame
from src.map import *

class InfiniteArrow:
    def __init__(self, tower_pos, target_pos, damage, speed):
        self.tower_pos = tower_pos
        self.target_pos = target_pos
        self.pos = tower_pos
        self.projectile = target_pos - tower_pos
        self.damage = damage
        self.speed = speed
        self.velocity = self.projectile.normalize() * self.speed
    def move(self, dt, enemies): # True 리탄하면 요소 삭제
        pass
        # self.pos += self.velocity * dt
        # for enemy in enemies:
        #     if (pygame.Vector2(enemy.x, enemy.y) - self.pos).length() <= TILE_SIZE:
        #         enemy.hp -= self.damage
        # if self.pos.x < MARGIN or self.pos.x > MARGIN+MAP_HEIGHT or self.pos.y < 0 or self.pos.y > HEIGHT:
        #     return True
    def draw(self, screen):
        pygame.draw.circle(screen, 'blue', (self.pos.x, self.pos.y), TILE_SIZE/2)

class Bomb:
    pass

class Iceball:
    pass