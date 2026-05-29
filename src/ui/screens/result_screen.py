import pygame
from src.core.config import WINDOW_WIDTH, WINDOW_HEIGHT
from src.ui.components.button import MenuButton


class ResultScreen:
    def __init__(self, screen, is_win, score, wave):
        self.screen = screen
        self.is_win = is_win
        self.score = score
        self.wave = wave
        
        self.font = pygame.font.SysFont("malgungothic", 30)
        self.title_font = pygame.font.SysFont("malgungothic", 80)
        self.input_font = pygame.font.SysFont("malgungothic", 40)
        
        self.player_name = ""
        self.max_name_length = 10
        
        # 버튼 설정
        btn_width = 300
        btn_height = 60
        self.confirm_button = MenuButton("기록 저장 및 종료", (WINDOW_WIDTH - btn_width) // 2, WINDOW_HEIGHT - 120, btn_width, btn_height, self.font)
        
    def draw(self):
        # 배경 (어두운 인디고 블루 톤)
        self.screen.fill((20, 20, 40))
        
        # 장식용 사각형
        border_rect = pygame.Rect(50, 50, WINDOW_WIDTH - 100, WINDOW_HEIGHT - 100)
        pygame.draw.rect(self.screen, (40, 40, 80), border_rect, 0, 15)
        pygame.draw.rect(self.screen, (255, 215, 0) if self.is_win else (200, 0, 0), border_rect, 3, 15)
        
        # 결과 타이틀
        title_text = "VICTORY!" if self.is_win else "GAME OVER"
        title_color = (255, 215, 0) if self.is_win else (255, 50, 50)
        title_surf = self.title_font.render(title_text, True, title_color)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 160))
        self.screen.blit(title_surf, title_rect)
        
        # 통계 표시 영역
        stats_y = 300
        wave_surf = self.font.render(f"최종 도달 웨이브: {self.wave}", True, (255, 255, 255))
        score_surf = self.font.render(f"최종 획득 점수: {self.score}", True, (255, 255, 255))
        
        self.screen.blit(wave_surf, wave_surf.get_rect(center=(WINDOW_WIDTH // 2, stats_y)))
        self.screen.blit(score_surf, score_surf.get_rect(center=(WINDOW_WIDTH // 2, stats_y + 45)))
        
        # 이름 입력 안내
        prompt_surf = self.font.render("명예의 전당에 등록할 이름:", True, (200, 200, 200))
        self.screen.blit(prompt_surf, prompt_surf.get_rect(center=(WINDOW_WIDTH // 2, stats_y + 130)))
        
        # 이름 입력 박스
        input_rect = pygame.Rect(WINDOW_WIDTH // 2 - 200, stats_y + 170, 400, 60)
        pygame.draw.rect(self.screen, (30, 30, 60), input_rect, 0, 10)
        pygame.draw.rect(self.screen, (255, 255, 255), input_rect, 2, 10)
        
        # 입력된 텍스트 표시
        display_name = self.player_name if self.player_name else "이름을 입력하세요..."
        text_color = (255, 255, 255) if self.player_name else (100, 100, 100)
        name_surf = self.input_font.render(display_name, True, text_color)
        name_rect = name_surf.get_rect(center=input_rect.center)
        self.screen.blit(name_surf, name_rect)
        
        # 버튼 그리기
        self.confirm_button.draw(self.screen)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", None
            
            if event.type == pygame.MOUSEMOTION:
                self.confirm_button.check_hover(event.pos)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.confirm_button.rect.collidepoint(event.pos):
                        name = self.player_name if self.player_name else "Anonymous"
                        return "confirm", name
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name = self.player_name if self.player_name else "Anonymous"
                    return "confirm", name
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    # 간단한 텍스트 입력 처리 (영문/숫자 중심)
                    if len(self.player_name) < self.max_name_length:
                        if event.unicode.isprintable() and event.unicode != '\r':
                            self.player_name += event.unicode
        return None, None

    def run(self):
        clock = pygame.time.Clock()
        while True:
            action, name = self.handle_event()
            if action:
                return action, name
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
