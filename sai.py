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
          nodeke = self.NodeKe(node)
          for ke in nodeke:
              alpha = max(alpha, self.DeQuy(ke, depth - 1, alpha, beta))
              if beta <= alpha:
                  break
          return alpha
      else:
          nodeke = self.NodeKe(node)
          for ke in nodeke:
              beta = min(beta, self.DeQuy(ke, depth - 1, alpha, beta))
              if beta <= alpha:
                  break
          return beta
    def KiemTraKetThuc(self, node):
        return sum(node.s[1:6]) == 0 or sum(node.s[7:12]) == 0  

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
                while soluong > 0:
                    vitri = self.SuaViTri(vitri + chieu)
                    _s[vitri] += 1
                    soluong -= 1
            elif vitri_ke == 0 or vitri_ke == 6: 
                MATLUOT = True
            else:
                vitri_keke = self.SuaViTri(vitri_ke + chieu)
                if _s[vitri_keke] > 0:
                    diem += _s[vitri_keke]
                    _s[vitri_keke] = 0
                    vitri = vitri_keke
                    MATLUOT = True
                else:
                    MATLUOT = True    
        min_score = node.min_scored + (diem if node.luotnguoi else 0)
        max_score = node.max_scored + (diem if not node.luotnguoi else 0)    
        return Node(not node.luotnguoi, min_score, max_score, buocdi if node.cachdi is None else node.cachdi, _s)

    def SuaViTri(self, n):
        return (n + 12) % 12
    def MinimaxSearch(self, hientai, d):
        f = self.DeQuy(hientai, d, -500, 500)
        if f in self.DANHSACHDI:
            return self.DANHSACHDI[f]  
        if not self.DANHSACHDI:
            vitri = 0
            chieu = 1
            if not hientai.luotnguoi:
                for i in range(1, 6):
                    if hientai.s[i] > 0:
                        vitri = i
                        break
            else:
                for i in range(7, 12):
                    if hientai.s[i] > 0:
                        vitri = i
                        break
            return [vitri, chieu]

class board:
    def __init__(self, pits, quan_pits, board):
        self.pits = pits
        self.quan_pits = quan_pits
        self.board = board
        self.background = pygame.image.load(os.path.join('Assets', 'ground.jpg'))
        self.background = pygame.transform.scale(self.background, (640, 400))
        self.stone_images = {
            1: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '1rock.png')), (50,50)),
            2: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '2rock.png')), (50,50)),
            3: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '3rock.png')), (50,50)),
            4: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '4rock.png')), (50,50)),
            5: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '5rock.png')), (50,50)),
            6: pygame.transform.scale(pygame.image.load(os.path.join('Assets', '5rock.png')), (50,50))
        }
        self.default_stone_img = pygame.transform.scale(
            pygame.image.load(os.path.join('Assets', 'manyrock.png')), (50, 50)
        )
        self.img_quan = pygame.image.load(os.path.join('Assets', 'quan.png'))
        self.img_quan = pygame.transform.scale(self.img_quan, (60,80))
        self.img_left = pygame.image.load(os.path.join('Assets', 'arrow_left.png'))
        self.img_left = pygame.transform.scale(self.img_left, (50, 50))
        self.img_right = pygame.image.load(os.path.join('Assets', 'arrow_right.png'))
        self.img_right = pygame.transform.scale(self.img_right, (50, 50))
        self._minimax = Minimax()
        self._searchDepth = 2
        self._luotnguoi = True 
        self._diemnguoi = 0  
        self._diemmay = 0  
        self._endgame = False
        self.pit_colors = [(255, 204, 102), (255, 100, 100)]
        self.quan_colors = [(255, 204, 102), (255, 100, 100)]
        self.width, self.height = 640, 400
        self.selected_pit = None 

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        
        for i, pit in enumerate(self.pits):
            pygame.draw.rect(screen, self.pit_colors[0], pit)
            num_stones = self.board[i]
            if num_stones in self.stone_images:
                stone_img = self.stone_images[num_stones]
            else:
                stone_img = self.default_stone_img  
            screen.blit(stone_img, (pit[0], pit[1]))

            if num_stones > 5:
                font = pygame.font.Font(None, 24)
                text = font.render(str(num_stones), True, (0, 0, 0))  
                screen.blit(text, (pit[0] + 15, pit[1] + 15))
        
        for quan in self.quan_pits:
            pygame.draw.rect(screen, self.quan_colors[1], quan)
            screen.blit(self.img_quan, (quan[0], quan[1]))

        if self.selected_pit is not None:
            pit_x, pit_y, _, _ = self.pits[self.selected_pit]
            screen.blit(self.img_left, (pit_x - 40, pit_y))
            screen.blit(self.img_right, (pit_x + 40, pit_y))

    def handle_click(self, pos):
        x, y = pos

        for i, pit in enumerate(self.pits):
            if i<6: 
                continue
            pit_rect = pygame.Rect(pit)  
            if pit_rect.collidepoint(x, y):
                print(f"Click vào ô dân {i}")
                self.selected_pit = i  
                return "pit", i  
        if self.selected_pit is not None:
            pit_x, pit_y, _, _ = self.pits[self.selected_pit]
            if pit_x - 40 <= x <= pit_x - 40 + 50 and pit_y <= y <= pit_y + 50:
                print("Click vào mũi tên trái")
                self.HumanMove(self.selected_pit, -1)
                return "arrow_left"
            if pit_x + 40 <= x <= pit_x + 40 + 50 and pit_y <= y <= pit_y + 50:
                print("Click vào mũi tên phải")
                self.HumanMove(self.selected_pit, 1)
                return "arrow_right"   
        return None  

    def HumanMove(self, position, chieu):
        if not self._luotnguoi or self._endgame:
            return
        current = Node(self._luotnguoi, self._diemnguoi, self._diemmay, chieu, self.board)
        move = [position, chieu]
        nextNode = self._minimax.Move(current, move)
        self.UpdateGameState(nextNode)
        self.draw()
        print("AI Turn Starts")  # Debug: Xem AI có được gọi không
        self.AIMove()

    def AIMove(self):
        if self._luotnguoi or self._endgame:
            print("AI Move Skipped")  # Debug
            return

        current = Node(self._luotnguoi, self._diemnguoi, self._diemmay, None, self.board)
        aiMove = self._minimax.MinimaxSearch(current, self._searchDepth)
        print(f"AI chooses move: {aiMove}")  # Debug: Xem AI chọn gì
        nextNode = self._minimax.Move(current, aiMove)
        self.UpdateGameState(nextNode)

        self.draw()
        self._luotnguoi = True  # Chuyển lượt lại cho người chơi


    def UpdateGameState(self, nextNode):
        self.board = nextNode.s
        self._diemnguoi = nextNode.min_scored
        self._diemmay = nextNode.max_scored
        self._luotnguoi = nextNode.luotnguoi

        print(f"Next turn: {'Human' if self._luotnguoi else 'AI'}")  # Debug
        self.KiemTra()
        self.ThieuQuan()


    def KiemTra(self):
        if (
            (self.board[0] == 0 and self.board[6] == 0)
            or (self._diemmay < 5 and all(self.board[i] == 0 for i in range(1, 6)))
            or (self._diemnguoi < 5 and all(self.board[i] == 0 for i in range(7, 12)))
        ):
            self._endgame = True
            self._luotnguoi = False
            self._diemmay = self._diemmay + sum(self.board[i] for i in range(1, 6))
            self._diemnguoi = self._diemnguoi + sum(self.board[i] for i in range(7, 12))
            self.board = [0] * 12

    def ThieuQuan(self):
        if not self._endgame:
            if (
                self._luotnguoi
                and self._diemnguoi >= 5
                and all(self.board[i] == 0 for i in range(7, 12))
            ):
                for i in range(7, 12):
                    self.board[i] = 1
                self._diemnguoi -= 5
            if (
                not self._luotnguoi
                and self._diemmay >= 5
                and all(self.board[i] == 0 for i in range(1, 6))
            ):
                for i in range(1, 6):
                    self.board[i] = 1
                self._diemmay -= 5
class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 400), RESIZABLE)
        pygame.display.set_caption("Ô Ăn Quan")
        
        self.t = board(
            [
                (455, 145, 60, 80),   # Ô quan phải (vị trí 0)
                (395, 115, 50, 50),   # Ô dân hàng trên số 1
                (325, 115, 50, 50),   # Ô dân hàng trên số 2
                (255, 115, 50, 50),   # Ô dân hàng trên số 3
                (185, 115, 50, 50),   # Ô dân hàng trên số 4
                (115, 115, 50, 50),   # Ô dân hàng trên số 5
                (45, 145, 60, 80),    # Ô quan trái (vị trí 6)
                (115, 185, 50, 50),   # Ô dân hàng dưới số 7
                (185, 185, 50, 50),   # Ô dân hàng dưới số 8
                (255, 185, 50, 50),   # Ô dân hàng dưới số 9
                (325, 185, 50, 50),   # Ô dân hàng dưới số 10
                (395, 185, 50, 50),   # Ô dân hàng dưới số 11
            ],
            [(45, 145, 60, 80), (455, 145, 60, 80)],
            [10] + [5] * 5 + [10] + [5] * 5  

        )
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked = self.t.handle_click(pos)
                        
            self.screen.fill(Color('gray'))
            self.t.draw(self.screen)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    App().run()
