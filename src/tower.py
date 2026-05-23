import pygame
from src.map import *
from src.bullet import Bullet
from src.skill import InfiniteArrow, Bomb, Iceball

class Tower:
    # 타워마다 다르게 설정해야 함!!!example(archer)
    damage = 15
    range = 3*TILE_SIZE
    speed = 0.5 # seconds
    color = "green"
    bullet_speed = 300
    cost = 40
    attack_cooldown = speed # 공격 쿨타임 계산용 변수입니다. attack_cooldown이 0이 되면 공격이 가능합니다.
    skill_cooldown = 70 # 스킬 쿨타임 계산용 변수입니다. skill_cooldown이 0이 되면 스킬이 사용 가능합니다.
    
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.level = 1
        self.max_level = 3
        self.kill = 0
        self.deal = 0
        self.skill_rate = 0
        self.is_selected = False # 선택된 타워는 range가 표시되고, 업그레이드, 정보창이 활성화됩니다.
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

        # 스킬이 어느정도 준비되었는지 막대바로 pygame 그리기
        skill_bar_width = 100
        skill_bar_height = 10
        skill_bar_x = bx
        skill_bar_y = by + 50
        pygame.draw.rect(screen, 'white', (skill_bar_x, skill_bar_y, skill_bar_width, skill_bar_height), 1)
        if self.skill_rate >= 0:
            inner_bar_width = skill_bar_width * self.skill_rate
        else:
            inner_bar_width = 0
        pygame.draw.rect(screen, 'yellow', (skill_bar_x, skill_bar_y, inner_bar_width, skill_bar_height))

    def update(self, dt, enemies): # bullet(또는 skill) instance를 return
        # 스킬 쿨타임이 업데이트
        # 공격 쿨타임 업데이트
        # 스킬 쿨타임이 돌았다면 -> 스킬
        # 스킬 쿨타임이 돌지 않았다면, 공격 쿨타임이 돌았다면 -> 공격
        pass
    # tower 마다 skill이 다르므로 skill 함수를 tower마다 구현해야 합니다.
    def skill(self, enemies):
        pass
    def attack(self, enemies):
        closest_enemy = self._get_closest_enemy(enemies)
        if closest_enemy and (pygame.Vector2(closest_enemy.x, closest_enemy.y) - self.pos).length() <= self.range:
            # 공격 가능한 상태입니다. 총알을 생성하여 반환해야 합니다.
            return Bullet(self.pos, closest_enemy, self.damage, self.bullet_speed, self.color)
        return None
    def level_up(self):
        pass
    def _get_closest_enemy(self, enemies):
        closest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = (pygame.Vector2(enemy.x, enemy.y) - self.pos).length()
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
        return closest_enemy
    
class Archer(Tower):
    type_name = "archer"
    damage = 10
    range = 3*TILE_SIZE
    speed = 0.5
    color = "green"
    bullet_speed = 300
    cost = 50
    attack_cooldown = speed # 공격 쿨타임 계산용 변수입니다. attack_cooldown이 0이 되면 공격이 가능합니다.
    skill_coolkill = 10
    skill_cooldown = skill_coolkill # 스킬 쿨타임 계산용 변수

    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self, dt, enemies):
        if self.skill_cooldown > 0:
            self.skill_cooldown = self.skill_coolkill-self.kill
            self.skill_rate = self.kill / self.skill_coolkill
            if self.attack_cooldown > 0:
                self.attack_cooldown -= dt
                return None
            else:
                # 공격 가능한 상태입니다. 공격 로직을 구현해야 합니다. 아직 공격 범위는 확인 안 함
                self.attack_cooldown = self.speed
                return self.attack(enemies)
        else:
            self.skill_cooldown = self.skill_coolkill
            self.skill_rate = 0
            return self.skill(enemies)
    
    def skill(self, enemies):
        return None
        # closest_enemy = self._get_closest_enemy(enemies)
        # if closest_enemy:
        #     return InfiniteArrow(self.pos, pygame.Vector2(closest_enemy.x, closest_enemy.y), self.damage, self.bullet_speed)
        # return None
    
class Cannon(Tower):
    type_name = "cannon"
    damage = 40
    range = 2.5*TILE_SIZE
    speed = 0.7
    color = "gray"
    bullet_speed = 400
    cost = 60
    attack_cooldown = speed # 공격 쿨타임 계산용 변수입니다. attack_cooldown이 0이 되면 공격이 가능합니다.
    skill_cooltime = 15
    skill_cooldown = skill_cooltime # 스킬 쿨타임 계산용 변수입니다. skill_cooldown이 0이 되면 스킬이 사용 가능합니다

    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self, dt, enemies):
        if self.skill_cooldown > 0:
            self.skill_cooldown -= dt
            self.skill_rate = 1 - self.skill_cooldown / self.skill_cooltime
            if self.attack_cooldown > 0:
                self.attack_cooldown -= dt
                return None
            else:
                # 공격 가능한 상태입니다. 공격 로직을 구현해야 합니다. 아직 공격 범위는 확인 안 함
                self.attack_cooldown = self.speed
                return self.attack(enemies)
        else:
            self.skill_cooldown = self.skill_cooltime
            self.skill_rate = 0
            return self.skill(enemies)
    

class Frost(Tower):
    type_name = "frost"
    damage = 5
    range = 4*TILE_SIZE
    speed = 0.6
    color = "white"
    bullet_speed = 350
    cost = 40
    attack_cooldown = speed # 공격 쿨타임 계산용 변수입니다. attack_cooldown이 0이 되면 공격이 가능합니다.
    skill_cooldamage = 60
    skill_cooldown = skill_cooldamage # 스킬 쿨타임 계산용 변수입니다. skill_cooldown이 0이 되면 스킬이 사용 가능합니다.

    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self, dt, enemies):
        if self.skill_cooldown > 0:
            self.skill_cooldown = self.skill_cooldamage - self.kill
            self.skill_rante = self.kill / self.skill_cooldamage
            if self.attack_cooldown > 0:
                self.attack_cooldown -= dt
                return None
            else:
                # 공격 가능한 상태입니다. 공격 로직을 구현해야 합니다. 아직 공격 범위는 확인 안 함
                self.attack_cooldown = self.speed
                return self.attack(enemies)
        else:
            self.skill_cooldown = self.skill_cooldamage
            self.skill_rate = 0
            return self.skill(enemies)
    

        
def create_tower(type_name):
    if type_name == "archer":
        return Archer()
    elif type_name == "cannon":
        return Cannon()
    elif type_name == "frost":
        return Frost()