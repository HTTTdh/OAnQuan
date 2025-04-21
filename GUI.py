import pygame
from pygame.locals import *
import os
from pygame.color import Color
import copy
from Minimax import Node, Minimax
class board:
    def __init__(self, pits, quan_pits, board):
        self.sound_effects = {
            'win': pygame.mixer.Sound(os.path.join('Assets', 'wingame.mp3')),
            'lose': pygame.mixer.Sound(os.path.join('Assets', 'losegame.mp3'))
        }
         # Điều chỉnh âm lượng
        for sound in self.sound_effects.values():
            sound.set_volume(0.5)
        self.step_index = 0
        self.step_interval = 300
        self.pits = pits
        self.quan_pits = quan_pits
        self.board = board
        self.cachdi=None
        self._luotnguoi = True  
        self._diemnguoi = 0     
        self._diemmay = 0      
        self._BanCo = copy.deepcopy(board)  
        self._endgame = False   
        self.pit_radius = 30
        self.pit_font = pygame.font.Font(None, 24)
        self.quan_font = pygame.font.Font(None, 28)
        self.background = pygame.image.load(os.path.join('Assets', 'ground.jpg'))
        self.background = pygame.transform.scale(self.background, (640, 400))
        self.stone_images = {
            1: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '1rock.png')), (60,60)),
            2: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '2rock.png')), (60,60)),
            3: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '3rock.png')), (60,60)),
            4: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '4rock.png')), (60,60)),
            5: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '5rock.png')), (60,60)),
            6: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '6rock.png')), (60,60))
        }
        self.default_stone_img = pygame.transform.scale(
            pygame.image.load(os.path.join('Assets', 'manyrock.png')), (60,60)
        )
        self.img_quan = pygame.image.load(os.path.join('Assets', 'quan.png'))
        self.img_quan = pygame.transform.scale(self.img_quan, (60,80))
        self.img_left = pygame.image.load(os.path.join('Assets', 'arrow_left.png'))
        self.img_left = pygame.transform.scale(self.img_left, (40,40))
        self.img_right = pygame.image.load(os.path.join('Assets', 'arrow_right.png'))
        self.img_right = pygame.transform.scale(self.img_right, (40,40))
        self._minimax = Minimax()
        self._searchDepth = 2   
        self.width, self.height = 640, 400
        self.selected_pit = None 
        self.pending_update = None
        self.animation_running= False
        self.animation_steps = []  # Danh sách các bước di chuyển
        self.current_animation_step = 0
        self.animation_delay = 300  # Thời gian delay giữa các bước (ms)
        self.last_animation_time = 0
        self.animation_speed = 0.3  # Tốc độ hiệu ứng (0.1-1.0), càng nhỏ càng chậm
        self.step_interval = int(500 / self.animation_speed)
        # Màu sắc mới
        self.pit_border_color = (100, 70, 30)  # Màu viền ô dân
        self.pit_fill_color = (240, 220, 180)  # Màu nền ô dân
        self.quan_border_color = (150, 100, 50)  # Màu viền ô quan
        self.quan_fill_color = (230, 200, 150)  # Màu nền ô quan
        self.text_color = (20, 20, 20)  # Màu chữ
    def UpdateGameState(self, nextNode):
            """Cập nhật trạng thái game sau khi di chuyển"""
            if not self.animation_running:  # Nếu không có hiệu ứng đang chạy
                self._apply_game_state(nextNode)
            else:
                self.pending_update = nextNode
    def _apply_game_state(self, nextNode):
        """Áp dụng trạng thái game sau khi animation kết thúc"""
        if nextNode is None:
            return
        self._BanCo = nextNode.s
        self._diemnguoi = nextNode.min_scored
        self._diemmay = nextNode.max_scored
        self._luotnguoi = nextNode.luotnguoi
        if self._luotnguoi == False:
            self.selected_pit = None
        print(f"Ban co: {self._BanCo}")
        self.KiemTra()
        self.ThieuQuan()  
        if not self._luotnguoi and not self._endgame:
            pygame.time.delay(1000)
            self.AIMove()
    def _draw_endgame(self, screen):
        """Vẽ màn hình kết thúc game"""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 36)

        if self._diemnguoi > self._diemmay:
            sound = self.sound_effects['win']
            sound.play()
            pygame.time.delay(1500)  # phát trong 2 giây
            sound.stop()
            result_text = font_large.render("YOU WIN!", True, (255, 50, 50))
        elif self._diemnguoi < self._diemmay:
            sound = self.sound_effects['lose']
            sound.play()
            sound.stop()
            result_text = font_large.render("GAME OVER!", True, (255, 100, 100))
        else:
            result_text = font_large.render("Draw!", True, (255, 255, 100))

        screen.blit(result_text, (self.width // 2 - result_text.get_width() // 2, self.height // 2 - 100))

        score_text = font_medium.render(
            f"Final Score: {self._diemnguoi} - {self._diemmay}", True, (255, 255, 255))
        screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, self.height // 2 + 50))

        restart_text = font_medium.render(
            "Press R to restart or ESC to quit", True, (200, 200, 200))
        screen.blit(restart_text, (self.width // 2 - restart_text.get_width() // 2, self.height // 2 + 100))
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for i, pit_rect in enumerate(self.pits):
            if i in (0, 6): continue  # Bỏ qua ô quan
            
            x, y, w, h = pit_rect
            pygame.draw.rect(screen, self.pit_fill_color, pit_rect, border_radius=5)
            pygame.draw.rect(screen, self.pit_border_color, pit_rect, 2, border_radius=5)
            
        # Vẽ các ô quan (luôn hiển thị đầy đủ)
        for i, quan_rect in enumerate(self.quan_pits):
            x, y, w, h = quan_rect
            pygame.draw.rect(screen, self.quan_fill_color, quan_rect, border_radius=10)
            pygame.draw.rect(screen, self.quan_border_color, quan_rect, 3, border_radius=10)
            
            quan_value = self._BanCo[0] if i == 0 else self._BanCo[6]
            if quan_value > 0:
                # Hiển thị hình ảnh quan
                img_rect = self.img_quan.get_rect(center=(x + w//2, y + h//2))
                screen.blit(self.img_quan, img_rect)
                # Hiển thị số lượng
                text = self.quan_font.render(str(quan_value), True, self.text_color)
                text_rect = text.get_rect(center=(x + w//2, y + h//2))
                screen.blit(text, text_rect)

        # Vẽ các viên đá trên các ô (khi không có animation)
        if not self.animation_steps:
            for i, pit_rect in enumerate(self.pits):
                if i in (0, 6): continue  # Bỏ qua ô quan
                
                x, y, w, h = pit_rect
                center_x, center_y = x + w//2, y + h//2
                num_stones = self._BanCo[i]
                
                if num_stones > 0:
                    stone_img = self.stone_images.get(num_stones, self.default_stone_img)
                    img_rect = stone_img.get_rect(center=(center_x, center_y))
                    screen.blit(stone_img, img_rect)

                    # Hiển thị số lượng quân
                    text = self.pit_font.render(str(num_stones), True, self.text_color)

                    if i in (1, 2, 3, 4, 5):  # Hàng trên
                        # Căn giữa theo chiều ngang, 15px phía trên ô
                        text_pos = (x + w//2 - text.get_width()//2, y - 25)
                    elif i in (7, 8, 9, 10, 11):  # Hàng dưới
                        # Căn giữa theo chiều ngang, 15px phía dưới ô
                        text_pos = (x + w//2 - text.get_width()//2, y + h + 10)

                    screen.blit(text, text_pos)
        else:
            # Vẽ animation di chuyển
            self._draw_animation(screen)

        # Vẽ UI và các thành phần khác
        self._draw_ui(screen)

        if self.selected_pit is not None and self._luotnguoi:
            pit_x, pit_y, _, _ = self.pits[self.selected_pit]
            screen.blit(self.img_left, (pit_x - 10, pit_y +60))
            screen.blit(self.img_right, (pit_x + 30, pit_y +60))

        if self._endgame:
            self._draw_endgame(screen)
    def _draw_ui(self, screen):
        """Vẽ giao diện người dùng (tách riêng để dễ quản lý)"""
        font_large = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)

        # Vẽ khung điểm
        pygame.draw.rect(screen, (50, 50, 50, 150), (30, 30, 200, 80), border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50, 150), (410, 30, 200, 80), border_radius=10)

        # Điểm người chơi
        player_title = font_small.render("PLAYER", True, (200, 200, 255))
        player_score = font_large.render(f"{self._diemnguoi}", True, (255, 255, 255))
        screen.blit(player_title, (50, 35))
        screen.blit(player_score, (50, 60))


        # Điểm AI
        ai_title = font_small.render("COMPUTER", True, (255, 200, 200))
        ai_score = font_large.render(f"{self._diemmay}", True, (255, 255, 255))
        screen.blit(ai_title, (430, 35))
        screen.blit(ai_score, (430, 60))

    def _draw_animation(self, screen):
        """Vẽ hiệu ứng di chuyển từng viên đá một, bao gồm cả ô quan"""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_animation_time > self.animation_delay:
            self.last_animation_time = current_time
            self.current_animation_step += 1
            
            if self.current_animation_step >= len(self.animation_steps):
                self.animation_steps = []
                self._apply_game_state(self.pending_update)
                self.pending_update = None
                return
        
        step = self.animation_steps[self.current_animation_step]
        
        # Vẽ tất cả các ô dân
        for i, pit_rect in enumerate(self.pits):
            if i in (0, 6): continue  # Ô quan vẽ riêng
            
            x, y, w, h = pit_rect
            center_x, center_y = x + w//2, y + h//2
            num_stones = step['board'][i]
            pygame.draw.rect(screen, self.pit_fill_color, pit_rect, border_radius=5)
            pygame.draw.rect(screen, self.pit_border_color, pit_rect, 2, border_radius=5)
            if num_stones > 0:
                stone_img = self.stone_images.get(num_stones, self.default_stone_img)
                img_rect = stone_img.get_rect(center=(center_x, center_y))
                screen.blit(stone_img, img_rect)

                text = self.pit_font.render(str(num_stones), True, self.text_color)

                if i in (1, 2, 3, 4, 5):  # Hàng trên
                    text_pos = (x + w//2 - text.get_width()//2, y - 25)
                elif i in (7, 8, 9, 10, 11):  # Hàng dưới
                    text_pos = (x + w//2 - text.get_width()//2, y + h + 10)

                screen.blit(text, text_pos)
                
                # Highlight ô đang di chuyển đến
                if i == step['current_pit']:
                    highlight = pygame.Surface((w, h), pygame.SRCALPHA)
                    highlight.fill((255, 255, 0, 80))
                    screen.blit(highlight, (x, y))
                
                

        # Vẽ các ô quan với hiệu ứng
        for i, quan_rect in enumerate(self.quan_pits):
            x, y, w, h = quan_rect
            quan_index = 0 if i == 0 else 6
            num_stones = step['board'][quan_index]
            
            # Thay đổi màu nền khi có hiệu ứng
            if quan_index == step['current_pit']:
                fill_color = (255, 220, 180)  # Màu sáng hơn khi được highlight
                border_color = (180, 120, 60)  # Màu viền đậm hơn
            else:
                fill_color = self.quan_fill_color
                border_color = self.quan_border_color
            
            pygame.draw.rect(screen, fill_color, quan_rect, border_radius=10)
            pygame.draw.rect(screen, border_color, quan_rect, 3, border_radius=10)
            
            if num_stones > 0:
                img_rect = self.img_quan.get_rect(center=(x + w // 2, y + h // 2))
                screen.blit(self.img_quan, img_rect)
                text = self.quan_font.render(str(num_stones), True, self.text_color)
                text_rect = text.get_rect(center=(x + w // 2, y + h + 15))
                screen.blit(text, text_rect)
    def prepare_move_animation(self, start_pos, direction, new_board_state):
        """Chuẩn bị các bước di chuyển cho animation, giống logic của hàm Move"""
        self.pending_update = new_board_state
        self.animation_steps = []

        temp_board = self._BanCo.copy()
        stones_to_move = temp_board[start_pos]
        temp_board[start_pos] = 0

        current_pos = start_pos
        self.animation_steps.append({
            'board': temp_board.copy(),
            'current_pit': None,
            'stones_left': stones_to_move
        })

        # Bước đầu tiên: rải toàn bộ stones_to_move
        while stones_to_move > 0:
            current_pos += direction
            current_pos %= 12  # vòng quanh bàn cờ (0-11)
            temp_board[current_pos] += 1
            stones_to_move -= 1
            self.animation_steps.append({
                'board': temp_board.copy(),
                'current_pit': current_pos,
                'stones_left': stones_to_move
            })

        # Giai đoạn sau lượt rải đầu tiên
        MATLUOT = False
        while not MATLUOT:
            next_pos = (current_pos + direction) % 12

            if temp_board[next_pos] > 0 and next_pos not in (0, 6):
                stones_to_move = temp_board[next_pos]
                temp_board[next_pos] = 0
                current_pos = next_pos

                self.animation_steps.append({
                    'board': temp_board.copy(),
                    'current_pit': current_pos,
                    'stones_left': stones_to_move
                })

                while stones_to_move > 0:
                    current_pos += direction
                    current_pos %= 12
                    temp_board[current_pos] += 1
                    stones_to_move -= 1
                    self.animation_steps.append({
                        'board': temp_board.copy(),
                        'current_pit': current_pos,
                        'stones_left': stones_to_move
                    })

            elif next_pos in (0, 6):  # Gặp ô quan
                MATLUOT = True
            else:
                next_next_pos = (next_pos + direction) % 12
                if temp_board[next_next_pos] > 0:
                    # "Ăn" quân tại ô kế tiếp của kế tiếp
                    temp_board[next_next_pos] = 0
                    self.animation_steps.append({
                        'board': temp_board.copy(),
                        'current_pit': next_next_pos,
                        'stones_left': 0
                    })
                    current_pos = next_next_pos
                    MATLUOT = True
                else:
                    MATLUOT = True

        self.current_animation_step = 0
        self.last_animation_time = pygame.time.get_ticks()

    def HumanMove(self, position, chieu):
        if not self._luotnguoi or self._endgame:
            return
            
        current = Node(self._luotnguoi, self._diemnguoi, self._diemmay, None, self._BanCo)
        move = [position, chieu]
        nextNode = self._minimax.Move(current, move)
        
        self.prepare_move_animation(position, chieu, nextNode)
    def AIMove(self):
        if self._luotnguoi or self._endgame:
            return

        current = Node(self._luotnguoi, self._diemnguoi, self._diemmay, None, self._BanCo)
        aiMove = self._minimax.MinimaxSearch(current, self._searchDepth)
        nextNode = self._minimax.Move(current, aiMove)
        self.prepare_move_animation(aiMove[0], aiMove[1], nextNode.s)
        self.UpdateGameState(nextNode)
    def handle_click(self, pos):
        x, y = pos
        
        for i, pit in enumerate(self.pits):
            pit_rect = pygame.Rect(pit)  
            if pit_rect.collidepoint(x, y):
                if ((self._luotnguoi and i > 6) or (not self._luotnguoi and i <= 6)) and self._BanCo[i] > 0:
                    print(f"Click vào ô dân {i} có {self._BanCo[i]} viên sỏi")
                    self.selected_pit = i  
                    self.cachdi = (i, None)
                    return "pit", i
                else:
                    print(f"Không thể chọn ô {i} (có {self._BanCo[i]} viên sỏi) trong lượt này")

        if self.selected_pit is not None:
            pit_x, pit_y, _, _ = self.pits[self.selected_pit]
            left_arrow = pygame.Rect(pit_x - 40, pit_y + 40, 50, 50)
            right_arrow = pygame.Rect(pit_x + 40, pit_y +40, 50, 50)

            if left_arrow.collidepoint(x, y):
                print("Click vào mũi tên trái")
                self.cachdi = (self.selected_pit, -1)
                self.HumanMove(self.selected_pit, -1)
                return "move", -1
                
            if right_arrow.collidepoint(x, y):
                print("Click vào mũi tên phải")
                self.cachdi = (self.selected_pit, 1)
                self.HumanMove(self.selected_pit, 1)
                return "move", 1
        self.cachdi = {}
        return None

    def KiemTra(self):
        if (
            (self._BanCo[0] == 0 and self._BanCo[6] == 0)
            or (self._diemmay < 5 and all(self._BanCo[i] == 0 for i in range(1, 6)))
            or (self._diemnguoi < 5 and all(self._BanCo[i] == 0 for i in range(7, 12)))
        ):
            self._endgame = True
            self._luotnguoi = False
            self._diemmay = self._diemmay + sum(self._BanCo[i] for i in range(1, 6))
            self._diemnguoi = self._diemnguoi + sum(self._BanCo[i] for i in range(7, 12))
            self._BanCo = [0] * 12

    def ThieuQuan(self):
        if not self._endgame:
            if (
                self._luotnguoi
                and self._diemnguoi >= 5
                and all(self._BanCo[i] == 0 for i in range(7, 12))
            ):
                for i in range(7, 12):
                    self._BanCo[i] = 1
                self._diemnguoi -= 5
                print("Player borrows stones")
                
            if (
                not self._luotnguoi
                and self._diemmay >= 5
                and all(self._BanCo[i] == 0 for i in range(1, 6))
            ):
                for i in range(1, 6):
                    self._BanCo[i] = 1
                self._diemmay -= 5
                print("AI borrows stones")
