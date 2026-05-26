import pygame
from src.map import *
from src.bullet import Bullet
from src.skill import InfiniteArrow, Bomb, Iceball


class Tower:
    # 타워마다 다르게 설정해야 함!!!example(archer)
    type_name = "archer"
    LEVEL_DATA = {
        1: {"damage": 10, "attack_range": 3.0*TILE_SIZE, "attack_speed": 0.50, "size_rate": 0.90, "cost": 50, "bullet_speed": 300, "color": (0, 255, 0)},
        2: {"damage": 15, "attack_range": 3.5*TILE_SIZE, "attack_speed": 0.40, "size_rate": 0.95, "cost": 30, "bullet_speed": 310, "color": (0, 150, 0)},
        3: {"damage": 20, "attack_range": 4.0*TILE_SIZE, "attack_speed": 0.35, "size_rate": 1.00, "cost": 20, "bullet_spped": 320, "color": (0, 100, 0)}
    }
    cost = LEVEL_DATA[1]["cost"]

    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.pos = pygame.Vector2((y+0.5)*TILE_SIZE + MARGIN, (x+0.5)*TILE_SIZE + MARGIN)
        self.rect = pygame.Rect(self.pos.x-TILE_SIZE/2, self.pos.y-TILE_SIZE/2, TILE_SIZE, TILE_SIZE)

        self.level = 1
        self.max_level = len(self.LEVEL_DATA)
        self.damage = self.LEVEL_DATA[self.level]["damage"]
        self.attack_range = self.LEVEL_DATA[self.level]["attack_range"]
        self.attack_speed = self.LEVEL_DATA[self.level]["attack_speed"]
        self.size_rate = self.LEVEL_DATA[self.level]["size_rate"]
        self.bullet_speed = self.LEVEL_DATA[self.level]["bullet_speed"]
        self.color = self.LEVEL_DATA[self.level]["color"]

        self.kill = 0
        self.deal = 0
        self.attack_cooldown = self.attack_speed
        self.skill_rate = 0
        self.is_selected = False # 선택된 타워는 range가 표시되고, 업그레이드, 정보창이 활성화됩니다.

        # tower마다 다르게 적어줘야 함
        # self.skill_coolkill = 10
        # self.skill_cooldown = self.skill_coolkill

    def draw(self, screen):
        pygame.draw.rect(screen, 'blue', self.rect)
        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), TILE_SIZE/2*self.size_rate)
    
    def update(self, dt, enemies): # bullet(또는 skill) instance를 return
        # 스킬 쿨타임이 업데이트
        # 공격 쿨타임 업데이트
        # 스킬 쿨타임이 돌았다면 -> 스킬
        # 스킬 쿨타임이 돌지 않았다면, 공격 쿨타임이 돌았다면 -> 공격
        pass

    # level이 max_level 보다 작은지 검사는 game_manager에서 해야 함
    def level_up(self): 
        self.level += 1
        self.damage = self.LEVEL_DATA[self.level]["damage"]
        self.attack_range = self.LEVEL_DATA[self.level]["attack_range"]
        self.attack_speed = self.LEVEL_DATA[self.level]["attack_speed"]
        self.size_rate = self.LEVEL_DATA[self.level]["size_rate"]
        self.bullet_speed = self.LEVEL_DATA[self.level]["bullet_speed"]
        self.color = self.LEVEL_DATA[self.level]["color"]
    
    # merge 조건을 game_manager에서 확인하고 이 함수를 실행해야 함
    def merge(self, other):
        self.level_up()
        self.kill += other.kill
        self.deal += other.deal
        self.skill_rate += other.skill_rate

    def _get_closest_enemy(self, enemies):
        closest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = (pygame.Vector2(enemy.x, enemy.y) - self.pos).length()
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
        return closest_enemy
    
    def _check_enemy_in_range(self, enemy):
        return (pygame.Vector2(enemy.x, enemy.y) - self.pos).length() <= self.attack_range
    
    # tower 마다 skill이 다르므로 skill 함수를 tower마다 구현해야 함
    def skill(self, enemies):
        pass

    def attack(self, enemies):
        # 가장 멀리간 enemy를 공격
        target_enemy = None
        for enemy in enemies[::-1]:
            if self._check_enemy_in_range(enemy):
                target_enemy = enemy
        if target_enemy:
            return Bullet(self, target_enemy, self.damage, self.bullet_speed, self.color)
        return None
    

class Archer(Tower):
    type_name = "archer"
    LEVEL_DATA = {
        1: {"damage": 10, "attack_range": 3.0*TILE_SIZE, "attack_speed": 0.50, "size_rate": 0.90, "cost": 50, "bullet_speed": 300, "color": (0, 255, 0)},
        2: {"damage": 15, "attack_range": 3.5*TILE_SIZE, "attack_speed": 0.40, "size_rate": 0.95, "cost": 30, "bullet_speed": 310, "color": (0, 150, 0)},
        3: {"damage": 20, "attack_range": 4.0*TILE_SIZE, "attack_speed": 0.35, "size_rate": 1.00, "cost": 20, "bullet_speed": 320, "color": (0, 100, 0)}
    }
    cost = LEVEL_DATA[1]["cost"]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.skill_cooltime = 4
        self.skill_cooldown = self.skill_cooltime

    def update(self, dt, enemies):
        if self.skill_cooldown > 0 and self.attack_cooldown > 0:
            self.skill_cooldown -= dt
            self.skill_rate = 1 - self.skill_cooldown / self.skill_cooltime
            self.attack_cooldown -= dt
            return (None, None)
        else:
            target_enemy = None
            for enemy in enemies[::-1]:
                if self._check_enemy_in_range(enemy):
                    target_enemy = enemy
            if self.skill_cooldown > 0 and self.attack_cooldown <= 0:
                self.skill_cooldown -= dt
                self.skill_rate = 1 - self.skill_cooldown / self.skill_cooltime
                if target_enemy:
                    self.attack_cooldown = self.attack_speed
                    return (Bullet(self, target_enemy, self.damage, self.bullet_speed, self.color), None)
                else:
                    return (None, None)
            elif self.skill_cooldown <= 0 and self.attack_cooldown > 0:
                self.attack_cooldown -= dt
                if target_enemy:
                    self.skill_cooldown = self.skill_cooltime
                    self.skill_rate = 0
                    return (None, InfiniteArrow(self, target_enemy))
                else:
                    return (None, None)
            else:
                if target_enemy:
                    self.skill_cooldown = self.skill_cooltime
                    self.skill_rate = 0
                    self.attack_cooldown = self.attack_speed
                    return (Bullet(self, target_enemy, self.damage, self.bullet_speed, self.color), InfiniteArrow(self, target_enemy))
                else:
                    return (None, None)
        # if self.skill_cooldown > 0:
        #     self.skill_cooldown = self.skill_coolkill-self.kill
        #     self.skill_rate = self.kill / self.skill_coolkill
        #     if self.attack_cooldown > 0:
        #         self.attack_cooldown -= dt
        #         return None
        #     else:
        #         # 공격 가능한 상태
        #         self.attack_cooldown = self.attack_speed
        #         return self.attack(enemies)
        # else:
        #     s = self.skill(enemies)
        #     if s:
        #         self.skill_cooldown = self.skill_coolkill
        #         self.skill_rate = 0
        #         return s
        #     else:
        #         return None
    

class Cannon(Tower):
    type_name = "cannon"
    LEVEL_DATA = {
        1: {"damage": 40, "attack_range": 2.5*TILE_SIZE, "attack_speed": 0.70, "size_rate": 0.90, "cost": 60, "bullet_speed": 400, "color": (211, 211, 211)},
        2: {"damage": 42, "attack_range": 3.0*TILE_SIZE, "attack_speed": 0.75, "size_rate": 0.95, "cost": 30, "bullet_speed": 410, "color": (169, 169, 169)},
        3: {"damage": 45, "attack_range": 4.0*TILE_SIZE, "attack_speed": 0.80, "size_rate": 1.00, "cost": 20, "bullet_speed": 420, "color": (128, 128, 128)}
    }
    cost = LEVEL_DATA[1]["cost"]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.skill_cooltime = 5
        self.skill_cooldown = self.skill_cooltime

    def update(self, dt, enemies):
        if self.skill_cooldown > 0 and self.attack_cooldown > 0:
            self.skill_cooldown -= dt
            self.skill_rate = 1 - self.skill_cooldown / self.skill_cooltime
            self.attack_cooldown -= dt
            return (None, None)
        else:
            target_enemy = None
            for enemy in enemies[::-1]:
                if self._check_enemy_in_range(enemy):
                    target_enemy = enemy
            if self.skill_cooldown > 0 and self.attack_cooldown <= 0:
                self.skill_cooldown -= dt
                self.skill_rate = 1 - self.skill_cooldown / self.skill_cooltime
                if target_enemy:
                    self.attack_cooldown = self.attack_speed
                    return (Bullet(self, target_enemy, self.damage, self.bullet_speed, self.color), None)
                else:
                    return (None, None)
            elif self.skill_cooldown <= 0 and self.attack_cooldown > 0:
                self.attack_cooldown -= dt
                if target_enemy:
                    self.skill_cooldown = self.skill_cooltime
                    self.skill_rate = 0
                    return (None, Bomb(self, target_enemy))
                else:
                    return (None, None)
            else:
                if target_enemy:
                    self.skill_cooldown = self.skill_cooltime
                    self.skill_rate = 0
                    self.attack_cooldown = self.attack_speed
                    return (Bullet(self, target_enemy, self.damage, self.bullet_speed, self.color), Bomb(self, target_enemy))
                else:
                    return (None, None)

class Frost(Tower):
    type_name = "frost"
    LEVEL_DATA = {
        1: {"damage": 5, "attack_range": 4.0*TILE_SIZE, "attack_speed": 0.60, "size_rate": 0.90, "cost": 40, "bullet_speed": 350, "color": (245, 254, 253)},
        2: {"damage": 10, "attack_range": 4.5*TILE_SIZE, "attack_speed": 0.50, "size_rate": 0.95, "cost": 30, "bullet_speed": 400, "color": (248, 248, 255)},
        3: {"damage": 12, "attack_range": 4.7*TILE_SIZE, "attack_speed": 0.45, "size_rate": 1.00, "cost": 30, "bullet_speed": 420, "color": (255, 255, 255)}
    }
    cost = LEVEL_DATA[1]["cost"]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.skill_cooltime = 3
        self.skill_cooldown = self.skill_cooltime

    def update(self, dt, enemies):
        if self.skill_cooldown > 0 and self.attack_cooldown > 0:
            self.skill_cooldown -= dt
            self.skill_rate = 1 - self.skill_cooldown / self.skill_cooltime
            self.attack_cooldown -= dt
            return (None, None)
        else:
            target_enemy = None
            for enemy in enemies[::-1]:
                if self._check_enemy_in_range(enemy):
                    target_enemy = enemy
            if self.skill_cooldown > 0 and self.attack_cooldown <= 0:
                self.skill_cooldown -= dt
                self.skill_rate = 1 - self.skill_cooldown / self.skill_cooltime
                if target_enemy:
                    self.attack_cooldown = self.attack_speed
                    return (Bullet(self, target_enemy, self.damage, self.bullet_speed, self.color), None)
                else:
                    return (None, None)
            elif self.skill_cooldown <= 0 and self.attack_cooldown > 0:
                self.attack_cooldown -= dt
                if target_enemy:
                    self.skill_cooldown = self.skill_cooltime
                    self.skill_rate = 0
                    return (None, Iceball(self, target_enemy))
                else:
                    return (None, None)
            else:
                if target_enemy:
                    self.skill_cooldown = self.skill_cooltime
                    self.skill_rate = 0
                    self.attack_cooldown = self.attack_speed
                    return (Bullet(self, target_enemy, self.damage, self.bullet_speed, self.color), Iceball(self, target_enemy))
                else:
                    return (None, None)
    
   
def create_tower(type_name, x, y):
    if type_name == "archer":
        return Archer(x, y)
    elif type_name == "cannon":
        return Cannon(x, y)
    elif type_name == "frost":
        return Frost(x, y)