import pygame
from pygame.locals import *
import os
from pygame.color import Color
from GUI import board
class App:
    def __init__(self):
        self.ai_pending = False
        self.ai_start_time = 0
        self.ai_delay = 3000  # Thời gian chờ trước khi AI đi (ms)
        pygame.init()
        self.screen = pygame.display.set_mode((640, 400), RESIZABLE)
        pygame.display.set_caption("Ô Ăn Quan")
        self.sound_effects = {
            'stone_pickup': pygame.mixer.Sound(os.path.join('Assets', 'stone_pickup.mp3')),
            'win': pygame.mixer.Sound(os.path.join('Assets', 'wingame.mp3')),
            'lose': pygame.mixer.Sound(os.path.join('Assets', 'losegame.mp3'))
        }
         # Điều chỉnh âm lượng
        for sound in self.sound_effects.values():
            sound.set_volume(0.5)
        self.initial_pits = [
            (470, 140, 60, 120),
            (410, 140, 60, 60),
            (350, 140, 60, 60),
            (290, 140, 60, 60), 
            (230, 140, 60, 60),  
            (170, 140, 60, 60),   
            (110, 140, 60, 120),
            (170, 200, 60, 60),    
            (230, 200, 60, 60),    
            (290, 200, 60, 60),    
            (350, 200, 60, 60),    
            (410, 200, 60, 60) 
        ]
        self.initial_quan_pits = [(470, 140, 60, 120), (110, 140, 60, 120)]
        self.initial_board_state = [10] + [5] * 5 + [10] + [5] * 5
        
        self.reset_game()
        self.running = True

    def reset_game(self):
        self.t = board(
            self.initial_pits,
            self.initial_quan_pits,
            self.initial_board_state.copy()
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                if event.key == K_r and self.t._endgame:
                    self.reset_game()
                    return True

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  
                    pos = pygame.mouse.get_pos()
                    clicked = self.t.handle_click(pos)

                    if clicked and not self.t._luotnguoi and not self.t._endgame:
                        self.t.step_index = 0  
                        self.ai_pending = True
                        self.ai_start_time = pygame.time.get_ticks()

        return True

    def run(self):
        """Vòng lặp chính của game"""
        clock = pygame.time.Clock()
        self.sound_effects['stone_pickup'].play() 
        
        while self.running:
            self.running = self.handle_events()

            # Xử lý AI nếu đang chờ
            current_time = pygame.time.get_ticks()
            if self.ai_pending and current_time - self.ai_start_time >= self.ai_delay:
                self.t.AIMove()
                self.t.step_index = 0  # Reset hiệu ứng vẽ
                self.ai_pending = False

            # Vẽ game
            self.screen.fill(Color('gray'))
            self.t.draw(self.screen)
            pygame.display.update()

            clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    App().run()