import pygame
from src.core.map import *
from src.entities.bullet import Bullet
from src.entities.skill import InfiniteArrow, Bomb, Iceball, fire_skill
from src.core.towers_data import TOWERS_DATA


class Tower:
    # 타워마다 다르게 설정해야 함!!!example(archer)
    type_name = "archer"
    LEVEL_DATA = TOWERS_DATA[type_name]
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

    def get_sell_price(self):
        total_cost = self.cost

        for lv in range(2, self.level + 1):
            total_cost += self.LEVEL_DATA[lv]["cost"]

        return int(total_cost * 0.8)
    
    # merge 조건을 game_manager에서 확인하고 이 함수를 실행해야 함
    def merge(self, other):
        self.level_up()
        self.kill += other.kill
        self.deal += other.deal
        self.skill_rate += other.skill_rate

    def _find_enemy(self, enemies):
        enemy_distances = [(e, e.left_distance()) for e in enemies]
        enemy_distances.sort(key=lambda x: x[1])
        enemy_distances = list(filter(lambda x: self._check_enemy_in_range(x[0]), enemy_distances))
        return enemy_distances[0][0] if enemy_distances else None
    
    def _check_enemy_in_range(self, enemy):
        return (pygame.Vector2(enemy.x, enemy.y) - self.pos).length() <= self.attack_range
    
    def attack(self, enemies):
        # 가장 멀리간 enemy를 공격
        target_enemy = self._find_enemy(enemies)
        if target_enemy and self._check_enemy_in_range(target_enemy):
            return Bullet(self, target_enemy, self.damage, self.bullet_speed, self.color)
        return None
    

class Archer(Tower):
    type_name = "archer"
    LEVEL_DATA = TOWERS_DATA[type_name]

    cost = LEVEL_DATA[1]["cost"]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.skill_cooltime = self.LEVEL_DATA[self.level]["skill"]["cooltime"]
        self.skill_cooldown = self.skill_cooltime

    def update(self, dt, enemies):
        if self.skill_cooldown > 0 and self.attack_cooldown > 0:
            self.skill_cooldown -= dt
            self.skill_rate = 1 - self.skill_cooldown / self.skill_cooltime
            self.attack_cooldown -= dt
            return (None, None)
        else:
            target_enemy = self._find_enemy(enemies)
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
                    return (None, fire_skill(self, target_enemy, self.LEVEL_DATA[self.level]["skill"]))
                else:
                    return (None, None)
            else:
                if target_enemy:
                    self.skill_cooldown = self.skill_cooltime
                    self.skill_rate = 0
                    self.attack_cooldown = self.attack_speed
                    return (Bullet(self, target_enemy, self.damage, self.bullet_speed, self.color), fire_skill(self, target_enemy, self.LEVEL_DATA[self.level]["skill"]))
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
    LEVEL_DATA = TOWERS_DATA[type_name]

    cost = LEVEL_DATA[1]["cost"]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.skill_cooltime = self.LEVEL_DATA[self.level]["skill"]["cooltime"]
        self.skill_cooldown = self.skill_cooltime

    def update(self, dt, enemies):
        if self.skill_cooldown > 0 and self.attack_cooldown > 0:
            self.skill_cooldown -= dt
            self.skill_rate = 1 - self.skill_cooldown / self.skill_cooltime
            self.attack_cooldown -= dt
            return (None, None)
        else:
            target_enemy = self._find_enemy(enemies)
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
                    return (None, fire_skill(self, target_enemy, self.LEVEL_DATA[self.level]["skill"]))
                else:
                    return (None, None)
            else:
                if target_enemy:
                    self.skill_cooldown = self.skill_cooltime
                    self.skill_rate = 0
                    self.attack_cooldown = self.attack_speed
                    return (Bullet(self, target_enemy, self.damage, self.bullet_speed, self.color), fire_skill(self, target_enemy, self.LEVEL_DATA[self.level]["skill"]))
                else:
                    return (None, None)

class Frost(Tower):
    type_name = "frost"
    LEVEL_DATA = TOWERS_DATA[type_name]

    cost = LEVEL_DATA[1]["cost"]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.skill_cooltime = self.LEVEL_DATA[self.level]["skill"]["cooltime"]
        self.skill_cooldown = self.skill_cooltime

    def update(self, dt, enemies):
        if self.skill_cooldown > 0 and self.attack_cooldown > 0:
            self.skill_cooldown -= dt
            self.skill_rate = 1 - self.skill_cooldown / self.skill_cooltime
            self.attack_cooldown -= dt
            return (None, None)
        else:
            target_enemy = self._find_enemy(enemies)
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
                    return (None, fire_skill(self, target_enemy, self.LEVEL_DATA[self.level]["skill"]))
                else:
                    return (None, None)
            else:
                if target_enemy:
                    self.skill_cooldown = self.skill_cooltime
                    self.skill_rate = 0
                    self.attack_cooldown = self.attack_speed
                    return (Bullet(self, target_enemy, self.damage, self.bullet_speed, self.color), fire_skill(self, target_enemy, self.LEVEL_DATA[self.level]["skill"]))
                else:
                    return (None, None)
    
   
def create_tower(type_name, x, y):
    if type_name == "archer":
        return Archer(x, y)
    elif type_name == "cannon":
        return Cannon(x, y)
    elif type_name == "frost":
        return Frost(x, y)