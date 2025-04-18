import pygame
from pygame.locals import *
import os
from pygame.color import Color
import copy
class Node:
    def __init__(self, luotnguoi, min_scored, max_scored, cachdi, s):
        self.luotnguoi = luotnguoi
        self.min_scored = min_scored
        self.max_scored = max_scored
        self.cachdi = cachdi  # (vị trí, hướng)
        self.s = copy.deepcopy(s) if s is not None else [0] * 12

class Minimax:
    def __init__(self):
        self.DANHSACHDI = {}  
    def DeQuy(self, node, depth, alpha, beta):
      if (node.s[0] == 0 and node.s[6] == 0) or depth <= 0:
          return self.DanhGia(node)

      if not node.luotnguoi:
          max_eval = -float('inf')
          nodeke = self.NodeKe(node)
          for ke in nodeke:
              eval = self.DeQuy(ke, depth - 1, alpha, beta)
              max_eval = max(max_eval, eval)
              alpha = max(alpha, eval)
              if beta <= alpha:
                  break
          return max_eval
      else:
          min_eval = float('inf')
          nodeke = self.NodeKe(node) 
          for ke in nodeke:
            eval = self.DeQuy(ke, depth - 1, alpha, beta) 
            min_eval = min(min_eval, eval) 
            beta = min(beta, eval) 
            if beta <= alpha:
                break  
          return min_eval

    def KiemTraKetThuc(self, node):
        if (
            (node.s[0] == 0 and node.s[6] == 0) or
            (node.diemmay < 5 and all(node.s[i] == 0 for i in range(1, 6))) or
            (node.diemnguoi < 5 and all(node.s[i] == 0 for i in range(7, 12)))
          ):
          return True
        return False
    def DanhGia(self, hientai):
      f = hientai.max_scored - hientai.min_scored

      if f not in self.DANHSACHDI:
         self.DANHSACHDI[f] = hientai.cachdi

      return f

    def NodeKe(self, node):
        buoc_di = self.BuocDi(node)
        return [self.Move(node, buocdi) for buocdi in buoc_di]

    def BuocDi(self, node):
        buocdi = []
        start, end = (1, 6) if not node.luotnguoi else (7, 12)
        for i in range(start, end):
            if node.s[i] > 0:
                buocdi.append([i, -1])
                buocdi.append([i, 1])
        return buocdi

    def Move(self, node, buocdi):
        vitri, chieu = buocdi
        _s = copy.deepcopy(node.s)
        diem = 0
        soluong = _s[vitri]
        _s[vitri] = 0
        MATLUOT = False
        while soluong > 0:
            vitri = self.SuaViTri(vitri + chieu)
            _s[vitri] += 1
            soluong -= 1
        while not MATLUOT:
            vitri_ke = self.SuaViTri(vitri + chieu)
            if _s[vitri_ke] > 0 and (vitri_ke != 0 and vitri_ke != 6):
                soluong = _s[vitri_ke]
                _s[vitri_ke] = 0
                vitri = vitri_ke
                # print(f"Bắt đầu di chuyển từ vị trí {vitri} với {soluong} quân cờ")
                while soluong > 0:
                    vitri = self.SuaViTri(vitri + chieu)
                    _s[vitri] += 1
                    soluong -= 1
                    # print(f"Di chuyển đến vị trí {vitri}, trạng thái hiệ1n tại: {_s}")
            elif vitri_ke == 0 or vitri_ke == 6:
                MATLUOT = True
                # print("Kết thúc")
            else:
                vitri_keke = self.SuaViTri(vitri_ke + chieu)
                # print(f"Kiểm tra vị trí kế tiếp của kế tiếp {vitri_keke}, giá trị: {_s[vitri_keke]}")
                if _s[vitri_keke] > 0:
                    diem += _s[vitri_keke]
                    _s[vitri_keke] = 0
                    vitri = vitri_keke
                    # print(f"Ăn được điểm tại vị trí {vitri_keke}, điểm hiện tại: {diem}")
                    MATLUOT = True
                    # print("Kết thúc lượt di chuyển")
                else:
                    MATLUOT = True
                    # print("Kết thúc lượt di chuyển")

        min_score = node.min_scored + (diem if node.luotnguoi else 0)
        max_score = node.max_scored + (diem if not node.luotnguoi else 0)
        # print(f"Kết quả cuối cùng: min_score={min_score}, max_score={max_score}, trạng thái: {_s}")
        return Node(not node.luotnguoi, min_score, max_score, buocdi if node.cachdi is None else node.cachdi, _s)

    def SuaViTri(self, n):
        return (n + 12) % 12
    def MinimaxSearch(self, hientai, d):
        best_move = None
        best_value = -float('inf') if not hientai.luotnguoi else float('inf')
        nodeke = self.NodeKe(hientai)  
        for ke in nodeke:
          if not hientai.luotnguoi:  
            eval = self.DeQuy(ke, d - 1, -float('inf'), float('inf'))
            # print(f"move found: {self.DANHSACHDI}")
            if eval > best_value:
                best_value = eval
                best_move = ke.cachdi
          else:  # Lượt của người chơi (minimizing)
            eval = self.DeQuy(ke, d - 1, -float('inf'), float('inf'))
            if eval < best_value:
                best_value = eval
                best_move = ke.cachdi

        return best_move
class board:
    def __init__(self, pits, quan_pits, board):
        self.step_index = 0
        self.last_update_time = pygame.time.get_ticks()
        self.step_interval = 300
        self.pits = pits
        self.quan_pits = quan_pits
        self.board = board
        self._luotnguoi = True  
        self._diemnguoi = 0     
        self._diemmay = 0      
        self._BanCo = copy.deepcopy(board)  
        self._endgame = False   
        self.pit_radius = 30
        self.quan_width, self.quan_height = 60, 80
        self.pit_font = pygame.font.Font(None, 24)
        self.quan_font = pygame.font.Font(None, 28)
        self.quan_border_color = (150, 100, 50)
        self.pit_border_color = (120, 90, 40)
        self.pit_fill_color = (250, 230, 200)
        self.quan_fill_color = (255, 220, 160)
        self.text_color = (20, 20, 20)
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
        self.img_left = pygame.transform.scale(self.img_left, (60,60))
        self.img_right = pygame.image.load(os.path.join('Assets', 'arrow_right.png'))
        self.img_right = pygame.transform.scale(self.img_right, (60,60))
        self._minimax = Minimax()
        self._searchDepth = 2
        self.pit_colors = [(255, 255, 255), (255, 255, 255)]
        self.quan_colors = [(255, 255, 255), (255, 255, 255)]
        self.width, self.height = 640, 400
        self.rendered_pits = set()
        self.selected_pit = None 
        self.selected_pit_initialized = False
        self.current_move_path = []  # Danh sách các ô sẽ di chuyển qua
        self.current_move_index = 0  # Vị trí hiện tại trong đường đi
        self.pending_update = None
        self.animation_running= False
    def UpdateGameState(self, nextNode):
        self._BanCo = nextNode.s
        self._diemnguoi = nextNode.min_scored
        self._diemmay = nextNode.max_scored
        self._luotnguoi = nextNode.luotnguoi
        if self._luotnguoi == False:
            self.selected_pit = None
        print(f"Ban co: {self._BanCo}")
        self.KiemTra()
        self.ThieuQuan()   
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        current_time = pygame.time.get_ticks()

        # Cập nhật hiệu ứng di chuyển
        if self.current_move_path and current_time - self.last_update_time >= self.step_interval:
            self.current_move_index += 1
            self.last_update_time = current_time
            if self.current_move_index >= len(self.current_move_path):
                self.current_move_path = []
                self.current_move_index = 0
                self.animation_running = False
                if self.pending_update:
                    self._apply_game_state(self.pending_update)
                    self.pending_update = None

        # Vẽ tất cả các ô dân (chỉ phần nền)
        for i, pit_rect in enumerate(self.pits):
            x, y, w, h = pit_rect
            center_x, center_y = x + w // 2, y + h // 2
            pygame.draw.circle(screen, self.pit_fill_color, (center_x, center_y), self.pit_radius)
            pygame.draw.circle(screen, self.pit_border_color, (center_x, center_y), self.pit_radius, 2)

        # Vẽ các ô quan (luôn hiển thị đầy đủ)
        for i, quan_rect in enumerate(self.quan_pits):
            x, y, w, h = quan_rect
            pygame.draw.rect(screen, self.quan_fill_color, quan_rect, border_radius=10)
            pygame.draw.rect(screen, self.quan_border_color, quan_rect, 3, border_radius=10)

            img_rect = self.img_quan.get_rect(center=(x + w // 2, y + h // 2))
            screen.blit(self.img_quan, img_rect)

            quan_value = self._BanCo[0] if i == 0 else self._BanCo[6]
            if quan_value > 0:
                text = self.quan_font.render(str(quan_value), True, self.text_color)
                text_rect = text.get_rect(center=(x + w // 2, y + h + 15))
                screen.blit(text, text_rect)

        # Vẽ các viên đá trên tất cả các ô (giữ nguyên trạng thái)
        for i, pit_rect in enumerate(self.pits):
            if i in (0, 6):  # Bỏ qua ô quan (đã vẽ ở trên)
                continue

            x, y, w, h = pit_rect
            center_x, center_y = x + w // 2, y + h // 2
            num_stones = self._BanCo[i]

            # Chỉ vẽ đá nếu:
            # 1. Không có hiệu ứng di chuyển nào đang chạy, HOẶC
            # 2. Ô này chưa nằm trong phần đường đi sắp tới của hiệu ứng
            if not self.animation_running or i not in self.current_move_path[self.current_move_index:]:
                if num_stones > 0:
                    stone_img = self.stone_images.get(num_stones, self.default_stone_img)
                    img_rect = stone_img.get_rect(center=(center_x, center_y))
                    screen.blit(stone_img, img_rect)

                    text = self.pit_font.render(str(num_stones), True, self.text_color)
                    text_rect = text.get_rect(bottomright=(x + w - 5, y + h - 5))
                    screen.blit(text, text_rect)

        # Vẽ hiệu ứng di chuyển (nếu có)
        if self.animation_running and self.current_move_path:
            current_pit = self.current_move_path[self.current_move_index]
            if current_pit not in (0, 6):  # Không vẽ hiệu ứng trên ô quan
                x, y, w, h = self.pits[current_pit]
                center_x, center_y = x + w // 2, y + h // 2
                num_stones = self._BanCo[current_pit]

                if num_stones > 0:
                    # Vẽ hiệu ứng đặc biệt cho ô đang được di chuyển qua
                    stone_img = self.stone_images.get(num_stones, self.default_stone_img)
                    img_rect = stone_img.get_rect(center=(center_x, center_y))
                    screen.blit(stone_img, img_rect)

                    # Làm nổi bật ô đang di chuyển qua
                    highlight_surface = pygame.Surface((w, h), pygame.SRCALPHA)
                    highlight_surface.fill((255, 255, 0, 50))  # Màu vàng nhạt trong suốt
                    screen.blit(highlight_surface, (x, y))

                    text = self.pit_font.render(str(num_stones), True, (255, 0, 0))  # Chữ đỏ
                    text_rect = text.get_rect(bottomright=(x + w - 5, y + h - 5))
                    screen.blit(text, text_rect)

        # Vẽ UI và các thành phần khác
        self._draw_ui(screen)

        if self.selected_pit is not None and self._luotnguoi:
            pit_x, pit_y, _, _ = self.pits[self.selected_pit]
            screen.blit(self.img_left, (pit_x - 40, pit_y))
            screen.blit(self.img_right, (pit_x + 40, pit_y))

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

        # Lượt chơi hiện tại
        turn_text = font_small.render(
            "Your turn" if self._luotnguoi else "Computer's turn",
            True,
            (100, 255, 100) if self._luotnguoi else (255, 100, 100)
        )
        screen.blit(turn_text, (270, 30))

    def _draw_endgame(self, screen):
        """Vẽ màn hình kết thúc game"""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 36)

        if self._diemnguoi > self._diemmay:
            result_text = font_large.render("YOU WIN!", True, (255, 50, 50))
        elif self._diemnguoi < self._diemmay:
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
        def UpdateGameState(self, nextNode):
            """Cập nhật trạng thái game sau khi di chuyển"""
            if not self.animation_running:  # Nếu không có hiệu ứng đang chạy
                self._apply_game_state(nextNode)
            else:
                self.pending_update = nextNode
    def _apply_game_state(self, nextNode):
        """Áp dụng trạng thái game ngay lập tức"""
        self._BanCo = nextNode.s
        self._diemnguoi = nextNode.min_scored
        self._diemmay = nextNode.max_scored
        self._luotnguoi = nextNode.luotnguoi
        
        if not self._luotnguoi:
            self.selected_pit = None
            
        self.KiemTra()
        self.ThieuQuan()
    

    def prepare_move_animation(self, start_pos, direction, new_board_state):
        """Chuẩn bị đường đi cho hiệu ứng di chuyển"""
        self.current_move_path = [start_pos]  # Bắt đầu từ ô được chọn
        stones = self._BanCo[start_pos]
        current_pos = start_pos
        
        for _ in range(stones):
            current_pos += direction
            # Xử lý vòng quanh bàn cờ
            if current_pos < 0: current_pos = 11
            elif current_pos > 11: current_pos = 0
                
            # Bỏ qua ô quan trừ khi là điểm cuối
            if (current_pos in (0, 6)) and (_ != stones - 1):
                current_pos += direction
                if current_pos < 0: current_pos = 11
                elif current_pos > 11: current_pos = 0
                    
            self.current_move_path.append(current_pos)
        
        self.current_move_index = 0
        self.last_update_time = pygame.time.get_ticks()
        self.animation_running = True  # Bật cờ hiệu ứng
    
    def handle_click(self, pos):
        x, y = pos

        for i, pit in enumerate(self.pits):
            pit_rect = pygame.Rect(pit)  
            if pit_rect.collidepoint(x, y):
                if ((self._luotnguoi and i > 6) or (not self._luotnguoi and i <= 6)) and self._BanCo[i] > 0:
                    print(f"Click vào ô dân {i} có {self._BanCo[i]} viên sỏi")
                    self.selected_pit = i  
                    return "pit", i
                else:
                    print(f"Không thể chọn ô {i} (có {self._BanCo[i]} viên sỏi) trong lượt này")

        if self.selected_pit is not None:
            pit_x, pit_y, _, _ = self.pits[self.selected_pit]
            left_arrow = pygame.Rect(pit_x - 40, pit_y, 50, 50)
            right_arrow = pygame.Rect(pit_x + 40, pit_y, 50, 50)

            if left_arrow.collidepoint(x, y):
                print("Click vào mũi tên trái")
                self.HumanMove(self.selected_pit, -1)
                return "move", -1
                
            if right_arrow.collidepoint(x, y):
                print("Click vào mũi tên phải")
                self.HumanMove(self.selected_pit, 1)
                return "move", 1

        return None
    def HumanMove(self, position, chieu):
        if not self._luotnguoi or self._endgame:
            return
            
        current = Node(self._luotnguoi, self._diemnguoi, self._diemmay, None, self._BanCo)
        move = [position, chieu]
        nextNode = self._minimax.Move(current, move)
        
        self.prepare_move_animation(position, chieu, nextNode.s)
        self.UpdateGameState(nextNode)

    def AIMove(self):
        if self._luotnguoi or self._endgame:
            return

        current = Node(self._luotnguoi, self._diemnguoi, self._diemmay, None, self._BanCo)
        aiMove = self._minimax.MinimaxSearch(current, self._searchDepth)
        nextNode = self._minimax.Move(current, aiMove)
        
        self.prepare_move_animation(aiMove[0], aiMove[1], nextNode.s)
        self.UpdateGameState(nextNode)
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
class App:
    def __init__(self):
        self.ai_pending = False
        self.ai_start_time = 0
        self.ai_delay = 3000  # Thời gian chờ trước khi AI đi (ms)
        pygame.init()
        self.screen = pygame.display.set_mode((640, 400), RESIZABLE)
        pygame.display.set_caption("Ô Ăn Quan")
        self.sound_effects = {
            # 'stone_drop': pygame.mixer.Sound(os.path.join('Assets', 'stone_drop.wav')),
            'stone_pickup': pygame.mixer.Sound(os.path.join('Assets', 'stone_pickup.mp3')),
            # 'capture': pygame.mixer.Sound(os.path.join('Assets', 'capture.wav')),
            # 'win': pygame.mixer.Sound(os.path.join('Assets', 'win.wav')),
            # 'lose': pygame.mixer.Sound(os.path.join('Assets', 'lose.wav'))
        }
         # Điều chỉnh âm lượng
        for sound in self.sound_effects.values():
            sound.set_volume(0.5)
        self.initial_pits = [
            (535, 170, 60, 80),
            (150, 140, 50, 50),   
            (220, 140, 50, 50),    
            (290, 140, 50, 50),    
            (360, 140, 50, 50),    
            (430, 140, 50, 50),
            (45, 170, 60, 80),
            (150, 230, 50, 50),    
            (220, 230, 50, 50),    
            (290, 230, 50, 50),    
            (360, 230, 50, 50),    
            (430, 230, 50, 50) 
        ]
        self.initial_quan_pits = [(45, 170, 60, 80), (535, 170, 60, 80)]
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

        self.ai_pending = False
        self.ai_start_time = 0
        self.ai_delay = 5000  

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