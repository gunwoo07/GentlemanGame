import pygame


class TowerButton:
    WIDTH = 120
    HEIGHT = 80

    def __init__(self, tower_class, bx, by):
        self.tower_class = tower_class
        self.bx = bx
        self.by = by
        self.rect = pygame.Rect(bx, by, self.WIDTH, self.HEIGHT)
        self.activation = False
    
    def draw(self, screen, font):
        # 버튼 배경 및 테두리
        pygame.draw.rect(screen, (60, 60, 60), self.rect)
        if self.activation:
            pygame.draw.rect(screen, 'yellow', self.rect, 1)
        else:
            pygame.draw.rect(screen, 'white', self.rect, 1)

        # 타워 아이콘(왼쪽 배치)
        pygame.draw.circle(screen, self.tower_class.LEVEL_DATA[1]['color'], (self.bx + 30, self.by + 40), 20)

        # 텍스트 정보(오른쪽 배치)
        name_text = font.render(self.tower_class.type_name, True, 'white')
        cost_text = font.render(f'{self.tower_class.cost}G', True, 'yellow')

        screen.blit(name_text, (self.bx + 60, self.by + 25))
        screen.blit(cost_text, (self.bx + 60, self.by + 45))


class LevelupButton:
    WIDTH = 200
    HEIGHT = 30

    def __init__(self, tower, bx, by):
        self.tower = tower
        self.bx = bx
        self.by = by
        self.rect = pygame.Rect(bx, by, self.WIDTH, self.HEIGHT)
    
    def draw(self, screen, font):
        # 버튼 배경 및 테두리
        pygame.draw.rect(screen, (60, 60, 60), self.rect)
        pygame.draw.rect(screen, 'white', self.rect, 1)

        # 텍스트 정보(최고레벨이면 레벨업 불가능)
        if self.tower.level < self.tower.max_level:
            levelup_text = font.render(f'레벨업 ({self.tower.LEVEL_DATA[self.tower.level+1]['cost']}G)', True, 'white')
        else:
            levelup_text = font.render(f'최고레벨입니다.(lv {self.tower.max_level})', True, 'white')
        screen.blit(levelup_text, (self.bx + 10, self.by + 5))


class MenuButton:
    def __init__(self, text, x, y, width, height, font, color=(100, 100, 100), hover_color=(150, 150, 150)):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
class SellButton:
    WIDTH = 120
    HEIGHT = 40

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.sell_price = 0

    def draw(self, screen, font, sell_price):
        self.sell_price = sell_price
        pygame.draw.rect(screen, (180, 60, 60), self.rect)
        pygame.draw.rect(screen, "white", self.rect, 2)

        text = font.render(
            f"판매 ({self.sell_price}G)",
            True,
            "white"
        )
        screen.blit(
            text,
            text.get_rect(center=self.rect.center)
        )