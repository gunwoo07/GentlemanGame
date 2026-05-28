import pygame
import json
import os
from src.core.config import WINDOW_WIDTH, WINDOW_HEIGHT, RANKING_PATH
from src.ui.screens.title_screen import MenuButton

class RankingScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("malgungothic", 30)
        self.title_font = pygame.font.SysFont("malgungothic", 60)
        
        # 랭킹 데이터 로드
        self.rankings = self.load_rankings()
        
        # 뒤로 가기 버튼
        btn_width = 250
        btn_height = 60
        self.back_button = MenuButton("뒤로 가기", (WINDOW_WIDTH - btn_width) // 2, WINDOW_HEIGHT - 120, btn_width, btn_height, self.font)

    def load_rankings(self):
        # rankings.json 파일에서 데이터를 가져옴
        if os.path.exists(RANKING_PATH):
            try:
                with open(RANKING_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 스코어(웨이브) 기준 내림차순 정렬
                    return sorted(data, key=lambda x: x.get('score', 0), reverse=True)
            except Exception as e:
                print(f"랭킹 로딩 중 오류: {e}")
                return []
        return []

    def draw(self):
        self.screen.fill((20, 20, 40)) # 배경색
        
        # 타이틀
        title_surf = self.title_font.render("명예의 전당", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_surf, title_rect)
        
        # 랭킹 목록 헤더
        header_y = 150
        rank_header = self.font.render("순위", True, (200, 200, 200))
        name_header = self.font.render("이름", True, (200, 200, 200))
        score_header = self.font.render("점수", True, (200, 200, 200))
        
        self.screen.blit(rank_header, (WINDOW_WIDTH // 2 - 200, header_y))
        self.screen.blit(name_header, (WINDOW_WIDTH // 2 - 80, header_y))
        self.screen.blit(score_header, (WINDOW_WIDTH // 2 + 100, header_y))
        
        # 구분선
        pygame.draw.line(self.screen, (100, 100, 100), (WINDOW_WIDTH // 2 - 220, header_y + 35), (WINDOW_WIDTH // 2 + 220, header_y + 35), 2)
        
        # 랭킹 데이터 표시 (상위 20개)
        y_offset = header_y + 50
        entry_font = pygame.font.SysFont("malgungothic", 24) # 폰트 크기 약간 축소
        
        if not self.rankings:
            no_rank_surf = self.font.render("아직 기록이 없습니다.", True, (150, 150, 150))
            self.screen.blit(no_rank_surf, (WINDOW_WIDTH // 2 - 120, y_offset + 50))
        else:
            for i, entry in enumerate(self.rankings[:20]):
                color = (255, 255, 255)
                if i == 0: color = (255, 215, 0) # 1등 금색
                elif i == 1: color = (192, 192, 192) # 2등 은색
                elif i == 2: color = (205, 127, 50) # 3등 동색
                
                rank_surf = entry_font.render(f"{i+1}", True, color)
                name_surf = entry_font.render(f"{entry.get('name', 'Anonymous')}", True, color)
                score_surf = entry_font.render(f"{entry.get('score', 0)}", True, color)
                
                self.screen.blit(rank_surf, (WINDOW_WIDTH // 2 - 180, y_offset + i * 32)) # 간격 축소
                self.screen.blit(name_surf, (WINDOW_WIDTH // 2 - 80, y_offset + i * 32))
                self.screen.blit(score_surf, (WINDOW_WIDTH // 2 + 140, y_offset + i * 32))
        
        # 뒤로 가기 버튼
        self.back_button.draw(self.screen)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            
            if event.type == pygame.MOUSEMOTION:
                self.back_button.check_hover(event.pos)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.back_button.rect.collidepoint(event.pos):
                        return "back"
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
