import pygame

class Bullet:
    def __init__(self, tower, enemy, damage, speed, color, size=5):
        self.tower = tower
        self.enemy = enemy
        self.tower_pos = tower.pos.copy()
        self.enemy_pos = pygame.Vector2(enemy.x, enemy.y)
        self.pos = tower.pos.copy()
        self.damage = damage
        self.speed = speed
        self.velocity = (self.enemy_pos - self.tower_pos).normalize() * self.speed
        self.color = color
        self.size = size # radius
        self.is_finished = False
    
    def move(self, dt):
        if (self.enemy_pos - self.pos).length() <= self.speed * dt:
            self.pos = self.target_pos.copy()
            self.enemy.hp -= self.damage
            self.is_finished = True
        else:
            self.pos += self.velocity * dt
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.collor, (self.pos.x, self.pos.y), self.size)