import pygame
from src.map import *

### 미완성입니다. 일단은 타워의 위치와 종류만 저장하는 형태로 구현했습니다. 공격과 스킬은 나중에 추가할 예정입니다.
class Bullet:
    size = 5
    def __init__(self, tower_pos, target_pos, damage, speed, color):
        self.tower_pos = tower_pos
        self.target_pos = target_pos
        self.pos = tower_pos
        self.projectile = target_pos - tower_pos
        self.damage = damage
        self.speed = speed
        self.velocity = self.projectile.normalize() * self.speed
        self.color = color
    
    def move(self, dt):
        if (self.target_pos - self.pos).length() <= self.speed * dt:
            self.pos = self.target_pos
            
        else:
            self.pos += self.velocity * dt

    def draw(self, screen):
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
    kill = 0
    deal = 0
    # example(archer)
    damage = 15
    range = 3*TILE_SIZE
    speed = 0.5 # seconds
    color = "green"
    bullet_speed = 300
    cost = 40
    is_selected = False # 선택된 타워는 range가 표시되고, 업그레이드, 정보창이 활성화됩니다.

    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.pos = pygame.Vector2((x + 0.5) * TILE_SIZE + MARGIN, (y + 0.5) * TILE_SIZE + MARGIN)
        self.rect = pygame.Rect(self.pos.x-TILE_SIZE/2, self.pos.y-TILE_SIZE/2, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, 'blue', self.rect)
        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), TILE_SIZE/2)
    
    def draw_range(self, screen):
        pygame.draw.circle(screen, 'white', (self.pos.x, self.pos.y), self.range, 1)

    def draw_info(self, screen, bx, by, font):
        tower_name = f"{self.type_name}(lv. {self.level})"
        tower_info = f"대미지: {self.deal}   범위: {self.range}   공격속도: {self.speed}"
        tower_name_text = font.render(tower_name, True, 'white')
        tower_info_text = font.render(tower_info, True, 'white')

        screen.blit(tower_name_text, (bx, by))
        screen.blit(tower_info_text, (bx, by + 20))

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
    cost = 50
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
        
class Cannon(Tower):
    type_name = "cannon"
    damage = 40
    range = 2.5*TILE_SIZE
    speed = 0.7
    color = "gray"
    bullet_speed = 400
    cost = 60
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

class Frost(Tower):
    type_name = "frost"
    damage = 5
    range = 4*TILE_SIZE
    speed = 0.6
    color = "white"
    bullet_speed = 350
    cost = 40
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
        return Cannon()
    elif type_name == "frost":
        return Frost()