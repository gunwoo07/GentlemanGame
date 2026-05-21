import pygame
from src.map import *
from src.enemy import *
from src.renderer import *




class Game:
    def __init__(self):
        pygame.init()
        self.renderer = Renderer(pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)))
        pygame.display.set_caption("gentleman's tower defense")
        self.clock = pygame.time.Clock()
        self.running = True
        self.shortest_path = find_shortest_path(game_map)
        self.tower_list = []
        self.enemy_list = []
        self.enemy_list.append(enemy("normal", *get_pos(0, 8)))


    def update(self, dt):
        self.shortest_path = find_shortest_path(game_map)
        
        for e in self.enemy_list:
            e.move(self.shortest_path, dt)

    def handle_event(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

    

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
                "stat": {
                    "gold" : 0,
                    "hp" : 100,
                    "wave" : 1,
                    "max_wave" : 5 
                }
            }


    
            self.renderer.render(game_state)
            pygame.display.flip()

        