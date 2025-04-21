from pygame.locals import *
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
                while soluong > 0:
                    vitri = self.SuaViTri(vitri + chieu)
                    _s[vitri] += 1
                    soluong -= 1
            elif vitri_ke == 0 or vitri_ke == 6:
                MATLUOT = True
            else:
                while True:
                    vitri_keke = self.SuaViTri(vitri_ke + chieu)
                    if _s[vitri_ke] == 0 and _s[vitri_keke] > 0 and vitri_ke != 0 and vitri_ke != 6:
                        diem += _s[vitri_keke]
                        _s[vitri_keke] = 0
                        vitri = vitri_keke
                        vitri_ke = self.SuaViTri(vitri + chieu)
                    else:
                        MATLUOT = True
                        break
        min_score = node.min_scored + (diem if node.luotnguoi else 0)
        max_score = node.max_scored + (diem if not node.luotnguoi else 0)
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
