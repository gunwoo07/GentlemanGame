import pygame
from src.map import *
from src.enemy import *
from src.renderer import *



wave_list = [
    ["normal", "normal", "normal", "normal", "normal", "normal", "normal"],
    ["normal", "normal", "normal", "normal", "fast", "fast", "fast", "fast", "fast", "fast"],
    ["strong", "strong", "strong", "normal", "normal", "normal", "normal", "fast", "fast", "fast"],
    ["strong", "strong", "strong", "strong", "strong", "strong", "fast", "fast", "fast", "fast", "fast"],
    ["strong", "strong", "strong", "boss"]
]

ENEMY_SPAWN = pygame.USEREVENT + 1

class Game:
    def __init__(self):
        pygame.init()
        self.renderer = Renderer(pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)))
        pygame.display.set_caption("gentleman's tower defense")
        self.clock = pygame.time.Clock()
        self.running = True
        self.shortest_path = find_shortest_path(game_map)
        self.enemy_list = [enemy("normal", *get_pos(0, 8))]*7
        self.tower_list = [Cannon(7, 8)]
        self.tower_list[0].is_selected = True
        self.bullet_list = []
        self.wave = 0

    def update(self, dt):
        self.shortest_path = find_shortest_path(game_map)
        
        for e in self.enemy_list:
            e.move(self.shortest_path, dt)
        
        for tower in self.tower_list:
            result = tower.update(dt, self.enemy_list)
            if result:
                self.bullet_list.append(result)

        for bullet in self.bullet_list:
            if bullet.is_finished:
                self.bullet_list.remove(bullet)
            print("bullet is here")
            bullet.move(dt)
    
    def handle_event(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.wave += 1
                    pygame.time.set_timer(ENEMY_SPAWN, 1000)

            elif event.type == ENEMY_SPAWN:
                if self.wave <= len(wave_list):
                    if wave_list[self.wave-1]:
                        enemy_type = wave_list[self.wave-1].pop(0)
                        self.enemy_list.append(enemy(enemy_type, *get_pos(0, 8)))
                else:
                    pygame.time.set_timer(ENEMY_SPAWN, 0)


    def play(self):

        while self.running:
            self.clock.tick(60)
            dt = self.clock.get_time() / 1000

            

            
            self.handle_event()
            self.update(dt)
            

            game_state = {
                "map":game_map,
                "towers":self.tower_list,
                "enemies":self.enemy_list,
                "path":self.shortest_path,
                "bullets": self.bullet_list,
                "stat": {
                    "gold" : 0,
                    "hp" : 100,
                    "wave" : 1,
                    "max_wave" : 5 
                }
            }




    
            self.renderer.render(game_state)
            pygame.display.flip()

        