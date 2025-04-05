import copy
import sys

class Node:
    def __init__(self, luotnguoi, min_scored, max_scored, cachdi, s):
        self.luotnguoi = luotnguoi  # True nếu là lượt của người, False nếu của AI
        self.min_scored = min_scored  # Điểm của người
        self.max_scored = max_scored  # Điểm của AI
        self.cachdi = cachdi  # Cách đi từ node hiện tại tới node mới (vị trí, hướng)
        self.s = copy.deepcopy(s) if s is not None else [0] * 12  # Sao chép trạng thái bàn cờ

class Minimax:
    def __init__(self):
        self.DANHSACHDI = {}  # Lưu trữ các bước đi
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
        """Kiểm tra nếu trạng thái node là trạng thái kết thúc."""
        return sum(node.s[1:6]) == 0 or sum(node.s[7:12]) == 0  # Một bên hết quân là kết thúc

    def DanhGia(self, hientai):
      f = hientai.max_scored - hientai.min_scored

      if f not in self.DANHSACHDI:
         self.DANHSACHDI[f] = hientai.cachdi

      return f


    def NodeKe(self, node):
        """Tạo danh sách các node kế tiếp từ trạng thái hiện tại."""
        buoc_di = self.BuocDi(node)
        return [self.Move(node, buocdi) for buocdi in buoc_di]

    def BuocDi(self, node):
        """Trả về danh sách các nước đi hợp lệ."""
        buocdi = []
        start, end = (1, 6) if not node.luotnguoi else (7, 12)
        for i in range(start, end):
            if node.s[i] > 0:
                buocdi.append([i, -1])
                buocdi.append([i, 1])
        return buocdi

    def Move(self, node, buocdi):
        """Di chuyển theo bước đi và trả về trạng thái mới của bàn cờ."""
        vitri, chieu = buocdi
        _s = copy.deepcopy(node.s)
        # print(f"Trạng thái ban đầu: {_s}")
        diem = 0
        soluong = _s[vitri]
        _s[vitri] = 0
        MATLUOT = False
    
        # print(f"Bắt đầu di chuyển từ vị trí {vitri} theo chiều {chieu}")
        
    
        while soluong > 0:
            vitri = self.SuaViTri(vitri + chieu)
            _s[vitri] += 1
            soluong -= 1
            # print(f"Di chuyển đến vị trí {vitri}, trạng thái hiện tại: {_s}")
    
        while not MATLUOT:
            vitri_ke = self.SuaViTri(vitri + chieu)
            # print(f"Kiểm tra vị trí kế tiếp {vitri_ke}, giá trị: {_s[vitri_ke]}")
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
        """Điều chỉnh vị trí trên bàn cờ để không vượt quá giới hạn."""
        return (n + 12) % 12
    def MinimaxSearch(self, hientai, d):
        # Lượng giá node hiện tại
        f = self.DeQuy(hientai, d, -500, 500)
        # print("Kết quả tìm kiếm minimax:", f)
        # print("Danh sách nước đi hợp lệ:", self.DANHSACHDI)
        if f in self.DANHSACHDI:
            print(f"move found: {self.DANHSACHDI}")
            return self.DANHSACHDI[f]  # Trả về nước đi tốt nhất đã lưu
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
class QuanCoGame:
    def __init__(self):
        self._BanCo = [0] * 12  # The board
        self._luotnguoi = True  # Human's turn initially
        self._diemnguoi = 0  # Human's score
        self._diemmay = 0  # AI's score
        self._endgame = False  # Game over flag

        self._minimax = Minimax()  # Minimax instance
        self._searchDepth = 2  # Search depth for Minimax

        self.NewGame()

    def NewGame(self):
        # Initialize the board
        self._BanCo = [0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5]
        self._diemnguoi = 0
        self._diemmay = 0
        self._luotnguoi = True
        self._endgame = False
        # self.UpdateUI()  # Assuming you have a UI update method

    def HumanMove(self, position, chieu):
        if not self._luotnguoi or self._endgame:
            return

        if position < 7 or position > 11 or self._BanCo[position] <= 0:
            return

        current = Node(self._luotnguoi, self._diemnguoi, self._diemmay, chieu, self._BanCo)
        move = [position, chieu]
        nextNode = self._minimax.Move(current, move)
        self.UpdateGameState(nextNode)
        self.print_board()
        print("AI Turn Starts")  # Debug: Xem AI có được gọi không
        self.AIMove()

    def AIMove(self):
        if self._luotnguoi or self._endgame:
            print("AI Move Skipped")  # Debug
            return

        current = Node(self._luotnguoi, self._diemnguoi, self._diemmay, None, self._BanCo)
        aiMove = self._minimax.MinimaxSearch(current, self._searchDepth)
        print(f"AI chooses move: {aiMove}")  # Debug: Xem AI chọn gì
        nextNode = self._minimax.Move(current, aiMove)
        self.UpdateGameState(nextNode)

        self.print_board()
        self._luotnguoi = True  # Chuyển lượt lại cho người chơi


    def UpdateGameState(self, nextNode):
        self._BanCo = nextNode.s
        self._diemnguoi = nextNode.min_scored
        self._diemmay = nextNode.max_scored
        self._luotnguoi = nextNode.luotnguoi

        print(f"Next turn: {'Human' if self._luotnguoi else 'AI'}")  # Debug
        self.KiemTra()
        self.ThieuQuan()


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
            # labThongbao.Text = "Máy Thắng!!"
            # LostGameSoundPlayer.Play();// âm thanh trong game.
            self._BanCo = [0] * 12
            # ThayDoi();

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
                # ThayDoi();
            if (
                not self._luotnguoi
                and self._diemmay >= 5
                and all(self._BanCo[i] == 0 for i in range(1, 6))
            ):
                for i in range(1, 6):
                    self._BanCo[i] = 1
                self._diemmay -= 5
            # ThayDoi()

    def print_board(self):
        print("\n========= BOARD STATE =========")
        print(f"AI Score: {self._diemmay}   |   Human Score: {self._diemnguoi}")
        print("================================")

        # Hàng trên (AI)
        print("   ", "  ".join(f"{self._BanCo[i]:2}" for i in range(5, 0, -1)))

        # Ô Quan ở giữa
        print(f" {self._BanCo[6]:2} ----------------- {self._BanCo[0]:2} ")

        # Hàng dưới (Human)
        print("   ", "  ".join(f"{x:2}" for x in self._BanCo[7:12]))  

        print("================================")
        print(f"Turn: {'Human' if self._luotnguoi else 'AI'}")



# Example usage:
if __name__ == "__main__":
    game = QuanCoGame()
    game.print_board()
    while not game._endgame:
        if game._luotnguoi:  # Human's turn
            try:
                pos = int(input("Enter position (7-11) to move: "))
                if pos < 7 or pos > 11 or game._BanCo[pos] <= 0:
                    print("Invalid move. Try again.")
                    continue
                chieu = int(input("Enter direction (-1 for left, 1 for right): "))
                print (f"Human chooses move: {pos, chieu}")
                game.HumanMove(pos, chieu)
            except ValueError:
                print("Please enter a valid integer.")
        else:  # AI's turn
            game.AIMove()
        game.print_board()


    print("Game Over!")
    if game._diemmay > game._diemnguoi:
        print("AI Wins!")
    elif game._diemmay < game._diemnguoi:
        print("Human Wins!")
    else:
        print("It's a Draw!")
