import pygame


class TowerButton:
    WIDTH = 120
    HEIGHT = 80

    def __init__(self, tower_class, bx, by):
        self.tower_class = tower_class
        self.bx = bx
        self.by = by
        self.rect = pygame.Rect(bx, by, self.WIDTH, self.HEIGHT)
    
    def draw(self, screen, font):
        # 버튼 배경 및 테두리
        pygame.draw.rect(screen, (60, 60, 60), self.rect)
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