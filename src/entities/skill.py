import pygame
from src.core.config import *

class Skill:
    def __init__(self, tower, target_enemy=None):
        self.tower = tower
        self.damage = tower.damage
        self.speed = tower.bullet_speed
        self.pos = pygame.Vector2(tower.pos.x, tower.pos.y)
        self.is_finished = False

    def move(self, dt, enemies):
        pass

    def draw(self, screen):
        pass

class InfiniteArrow(Skill):
    def __init__(self, tower, target_enemy, damage, bullet_speed, damage_range=1.0*TILE_SIZE, color="blue"):
        self.tower = tower
        self.damage = damage
        self.speed = bullet_speed
        self.damage_range = damage_range
        self.color = color
        self.pos = pygame.Vector2(tower.pos.x, tower.pos.y)
        self.target_pos = pygame.Vector2(target_enemy.x, target_enemy.y)
        self.is_finished = False
        # Calculate direction towards target_pos and normalize
        direction = self.target_pos - self.pos
        self.velocity = direction.normalize() * self.speed
        self.hit_enemies = set() # To prevent multiple hits on the same enemy

    def move(self, dt, enemies):
        self.pos += self.velocity * dt
        
        # 1. Collision Check (within 1 TILE_SIZE)
        for enemy in enemies:
            if enemy not in self.hit_enemies:
                dist = (pygame.Vector2(enemy.x, enemy.y) - self.pos).length()
                if dist <= self.damage_range:
                    if not enemy.is_invincible:
                        enemy.hp -= self.damage
                        self.tower.deal += self.damage
                        if enemy.hp <= 0:
                            self.tower.kill += 1
                    self.hit_enemies.add(enemy)

        # 2. Map Boundary Check (Remove if outside map area)
        if not (MARGIN <= self.pos.x <= MARGIN + MAP_WIDTH and 
                MARGIN <= self.pos.y <= MARGIN + MAP_HEIGHT):
            self.is_finished = True

    def draw(self, screen):
        # Blue projectile
        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), 0.5*self.damage_range)

class Bomb(Skill):
    def __init__(self, tower, target_enemy, damage, bullet_speed, damage_range=2.0*TILE_SIZE, color='orange'):
        self.tower = tower
        self.damage = damage
        self.speed = bullet_speed
        self.enemy = target_enemy
        self.pos = pygame.Vector2(tower.pos.x, tower.pos.y)
        self.target_pos = pygame.Vector2(target_enemy.x, target_enemy.y)
        self.is_finished = False
        self.velocity = (self.target_pos - self.pos).normalize() * self.speed
        self.explosion_radius = damage_range
        self.is_exploding = False
        self.explosion_timer = 0.3 # Explosion effect duration
        self.color = color

    def move(self, dt, enemies):
        if not self.is_exploding:
            # Traveling to target
            target_current = pygame.Vector2(self.enemy.x, self.enemy.y)
            if (target_current - self.pos).length() <= self.speed * dt:
                self.pos = target_current
                self.explode(enemies)
            else:
                # Slight homing towards enemy current position
                direction = (target_current - self.pos).normalize()
                self.velocity = direction * self.speed
                self.pos += self.velocity * dt
        else:
            # Exploding (wait for timer to finish)
            self.explosion_timer -= dt
            if self.explosion_timer <= 0:
                self.is_finished = True

    def explode(self, enemies):
        self.is_exploding = True
        for enemy in enemies:
            dist = (pygame.Vector2(enemy.x, enemy.y) - self.pos).length()
            if dist <= self.explosion_radius:
                enemy.hp -= self.damage
                self.tower.deal += self.damage
                if enemy.hp <= 0:
                    self.tower.kill += 1

    def draw(self, screen):
        if not self.is_exploding:
            pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), 10)
        else:
            # Transparent explosion effect
            s = pygame.Surface((self.explosion_radius * 2, self.explosion_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 165, 0, 100), (self.explosion_radius, self.explosion_radius), self.explosion_radius)
            screen.blit(s, (self.pos.x - self.explosion_radius, self.pos.y - self.explosion_radius))

class Iceball(Skill):
    def __init__(self, tower, target_enemy, damage, bullet_speed, slow_duration=3.0, slow_rate=0.7, color=(173, 216, 230)):
        self.tower = tower
        self.damage = damage
        self.speed = bullet_speed
        self.pos = pygame.Vector2(tower.pos.x, tower.pos.y)
        self.is_finished = False
        self.enemy = target_enemy
        self.target_pos = pygame.Vector2(target_enemy.x, target_enemy.y)
        self.velocity = (self.target_pos - self.pos).normalize() * self.speed
        self.is_hit = False
        self.slow_timer = 0
        self.slow_duration = slow_duration
        self.slow_rate = slow_rate
        self.original_speed = 0
        self.color = color

    def move(self, dt, enemies):
        if not self.is_hit:
            # 페이즈 1: 적을 향해 이동
            target_current = pygame.Vector2(self.enemy.x, self.enemy.y)
            if (target_current - self.pos).length() <= self.speed * dt:
                self.pos = target_current
                self.is_hit = True
                
                # 대미지
                self.enemy.hp -= self.damage
                self.tower.deal += self.damage
                if self.enemy.hp <= 0:
                    self.tower.kill += 1
                
                # 슬로우 적용
                self.original_speed = self.enemy.speed
                self.enemy.speed *= self.slow_rate
                # 너무 느린 경우 예외(중첩 가능)
                if self.enemy.speed < 10:
                    self.enemy.speed = 10
            else:
                self.velocity = (target_current - self.pos).normalize() * self.speed
                self.pos += self.velocity * dt
        else:
            # 페이즈 2: 적을 맞춘 후
            self.slow_timer += dt
            # 적을 따라 이동(보이지는 않게)
            self.pos = pygame.Vector2(self.enemy.x, self.enemy.y)
            
            if self.slow_timer >= self.slow_duration or self.enemy.hp <= 0:
                # 적의 스피드 원래대로
                if self.enemy.hp > 0:
                    self.enemy.speed = self.original_speed
                self.is_finished = True

    def draw(self, screen):
        if not self.is_hit:
            # 하늘색 원
            pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), 7)
        else:
            # 이후엔 그리지 않기
            pass


def fire_skill(tower, target_enemy, skill):
    if skill["skill_name"] == "InfiniteArrow":
        return InfiniteArrow(tower, target_enemy, skill["damage"], skill["bullet_speed"], skill["damage_range"], skill["color"])
    elif skill["skill_name"] == "Bomb":
        return Bomb(tower, target_enemy, skill["damage"], skill["bullet_speed"], skill["damage_range"], skill["color"])
    elif skill["skill_name"] == "Iceball":
        return Iceball(tower, target_enemy, skill["damage"], skill["bullet_speed"], skill["slow_duration"], skill["slow_rate"], skill["color"])