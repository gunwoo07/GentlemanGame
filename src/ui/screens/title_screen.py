import pygame
import os
from src.core.config import WINDOW_WIDTH, WINDOW_HEIGHT, SAVEGAME_PATH
from src.ui.components.button import MenuButton


class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("malgungothic", 30)
        self.title_font = pygame.font.SysFont("malgungothic", 60)
        
        
        btn_width = 250
        btn_height = 60
        start_x = (WINDOW_WIDTH - btn_width) // 2
        start_y = 250
        
        self.buttons = {
            "easy": MenuButton("이지 모드", start_x, start_y, btn_width, btn_height, self.font),
            "hard": MenuButton("하드 모드", start_x, start_y + 80, btn_width, btn_height, self.font),
            "continue": MenuButton("이어하기", start_x, start_y + 160, btn_width, btn_height, self.font),
            "ranking": MenuButton("랭킹 보기", start_x, start_y + 240, btn_width, btn_height, self.font),
            "exit": MenuButton("종료", start_x, start_y + 320, btn_width, btn_height, self.font)
        }
        
        self.save_exists = os.path.exists(SAVEGAME_PATH)
        if not self.save_exists:
            self.buttons["continue"].color = (50, 50, 50) # 비활성화된 느낌
            self.buttons["continue"].hover_color = (50, 50, 50)

    def draw(self):
        self.screen.fill((20, 20, 40)) # 배경색
        
        # 타이틀 텍스트
        title_surf = self.title_font.render("Gentleman's Defense", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 120))
        self.screen.blit(title_surf, title_rect)
        
        for btn in self.buttons.values():
            btn.draw(self.screen)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            
            if event.type == pygame.MOUSEMOTION:
                for btn in self.buttons.values():
                    btn.check_hover(event.pos)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.buttons["easy"].rect.collidepoint(event.pos):
                        return "easy"
                    if self.buttons["hard"].rect.collidepoint(event.pos):
                        return "hard"
                    if self.buttons["continue"].rect.collidepoint(event.pos) and self.save_exists:
                        return "continue"
                    if self.buttons["ranking"].rect.collidepoint(event.pos):
                        return "ranking"
                    if self.buttons["exit"].rect.collidepoint(event.pos):
                        return "exit"
        return None

    def run(self):
        clock = pygame.time.Clock()
        while True:
            result = self.handle_event()
            if result:
                return result
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
