import pygame
from map import *

### 미완성입니다. 일단은 타워의 위치와 종류만 저장하는 형태로 구현했습니다. 공격과 스킬은 나중에 추가할 예정입니다.
class Bullet:
    def __init__(self, projectile, damage, speed, color):
        self.projectile = projectile
        self.damage = damage
        self.speed = speed
        self.color = color
    
    def draw(self):
        pass

class Skill:
    def __init__(self):
        pass
class InfiniteArrow(Skill):
    pass
class Bomb(Skill):
    pass
class Iceball(Skill):
    pass

class Tower:
    level = 1
    max_level = 3
    # example(archer)
    damage = 15
    range = 3*TILE_SIZE
    speed = 0.5 # seconds
    color = "green"
    bullet_speed = 300
    kill = 0
    deal = 0

    def __init__(self, x, y, type_name):
        self.grid_x = x
        self.grid_y = y
        self.pos = pygame.Vector2((x + 0.5) * TILE_SIZE + MAP_MARGIN, (y + 0.5) * TILE_SIZE + MAP_MARGIN)

        if type_name == "archer":
            self.damage = 15
            self.range = 3*TILE_SIZE
            self.speed = 0.5 # seconds
            self.color = "green"
            self.bullet_speed = 300
        elif type_name == "cannon":
            self.damage = 40
            self.range = 2.5*TILE_SIZE
            self.speed = 0.7
            self.color = "gray"
            self.bullet_speed = 400
        elif type_name == "frost":
            self.damage = 5
            self.range = 4*TILE_SIZE
            self.speed = 0.6
            self.collor = "white"
            self.bullet_speed = 350
    
    def draw(self, screen):
        pygame.draw.rect(screen, 'blue', (self.pos.x-TILE_SIZE/2, self.pos.y-TILE_SIZE/2, TILE_SIZE, TILE_SIZE))
        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), TILE_SIZE/2)
    
    def skill_counter(self):
        pass
    def skill(self):
        pass
    def attack(self, target):
        pass
    def level_up(self):
        pass

class Archer(Tower):
    type_name = "archer"
    damage = 10
    range = 3*TILE_SIZE
    speed = 0.5
    color = "green"
    bullet_speed = 300
    skill_active = False

    def __init__(self, x, y):
        super().__init__(x, y)

    # dt마다 호출 필요
    def skill_counter(self):
        if not self.skill_active and self.deal >= 70:
            self.skill_active = True
            self.deal = 0
    
    def attack(self, target):
        if self.skill_active:
            pass
        else:
            b = Bullet()
        

def create_tower(type_name):
    if type_name == "archer":
        return Archer()
    elif type_name == "cannon":
        pass
    elif type_name == "frost":
        pass