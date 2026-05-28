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
    def __init__(self, tower, target_enemy):
        super().__init__(tower)
        self.target_pos = pygame.Vector2(target_enemy.x, target_enemy.y)
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
                if dist <= TILE_SIZE:
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
        pygame.draw.circle(screen, 'blue', (self.pos.x, self.pos.y), 8)

class Bomb(Skill):
    def __init__(self, tower, target_enemy):
        super().__init__(tower, target_enemy)
        self.enemy = target_enemy
        self.target_pos = pygame.Vector2(target_enemy.x, target_enemy.y)
        self.velocity = (self.target_pos - self.pos).normalize() * self.speed
        self.explosion_radius = 2 * TILE_SIZE
        self.is_exploding = False
        self.explosion_timer = 0.3 # Explosion effect duration

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
            pygame.draw.circle(screen, 'orange', (int(self.pos.x), int(self.pos.y)), 10)
        else:
            # Transparent explosion effect
            s = pygame.Surface((self.explosion_radius * 2, self.explosion_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 165, 0, 100), (self.explosion_radius, self.explosion_radius), self.explosion_radius)
            screen.blit(s, (self.pos.x - self.explosion_radius, self.pos.y - self.explosion_radius))

class Iceball(Skill):
    def __init__(self, tower, target_enemy):
        super().__init__(tower, target_enemy)
        self.enemy = target_enemy
        self.target_pos = pygame.Vector2(target_enemy.x, target_enemy.y)
        self.velocity = (self.target_pos - self.pos).normalize() * self.speed
        self.is_hit = False
        self.slow_timer = 0
        self.slow_duration = 3.0
        self.original_speed = 0

    def move(self, dt, enemies):
        if not self.is_hit:
            # Phase 1: Moving towards enemy
            target_current = pygame.Vector2(self.enemy.x, self.enemy.y)
            if (target_current - self.pos).length() <= self.speed * dt:
                self.pos = target_current
                self.is_hit = True
                
                # Damage
                self.enemy.hp -= self.damage
                self.tower.deal += self.damage
                if self.enemy.hp <= 0:
                    self.tower.kill += 1
                
                # Apply Slow (40% reduction)
                self.original_speed = self.enemy.speed
                self.enemy.speed *= 0.7
                if self.enemy.speed < 10:
                    self.enemy.speed = 10
            else:
                self.velocity = (target_current - self.pos).normalize() * self.speed
                self.pos += self.velocity * dt
        else:
            # Phase 2: Counting time after hit
            self.slow_timer += dt
            # Keep position attached to enemy (though invisible)
            self.pos = pygame.Vector2(self.enemy.x, self.enemy.y)
            
            if self.slow_timer >= self.slow_duration or self.enemy.hp <= 0:
                # Restore speed and finish
                if self.enemy.hp > 0:
                    self.enemy.speed = self.original_speed
                self.is_finished = True

    def draw(self, screen):
        if not self.is_hit:
            # Light blue projectile
            pygame.draw.circle(screen, (173, 216, 230), (int(self.pos.x), int(self.pos.y)), 7)
        else:
            # Size 0 (don't draw) after hit
            pass
