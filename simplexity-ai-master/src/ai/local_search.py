import random
from time import time

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List

class LocalSearch:
    def __init__(self):
        self.streak_candidates_self = []
        self.streak_candidates_enemy = []

    def neighbors(self, state: State, row: int, column: int) -> List[List[Tuple[int, int]]]:
        neighbors = []
        batasKiri = max(0, column - 3)
        batasKanan = min(6, column + 3)
        batasAtas = min(5, row + 3)
        batasBawah = max(0, row - 3)
        for i in range(batasKiri, batasKanan - 2):
            neighbors.append([(row, j) for j in range(i,i+4)])
            neighbors.append([(batasAtas - (j-i), j) for j in range(i, i+4)])
        for i in range(batasBawah, batasAtas - 2):
            neighbors.append([(j, column) for j in range(i,i+4)])
            neighbors.append([(j, batasKanan - (j-i)) for j in range(i, i+4)])
        return neighbors

    def is_diagonal (self, point1: Tuple[int, int],point2: Tuple[int, int]):
        return ((point1[0] + 1 == point2[0] and point1[1] + 1 == point2[1]) or (point1[0] - 1 == point2[0] and point1[1] + 1 == point2[1]) or (point1[0] + 1 == point2[0] and point1[1] - 1 == point2[1]) or (point1[0] - 1 == point2[0] and point1[1] - 1 == point2[1]))
    
    def total_point(self,c1,c2,c3,c4,c5,c6,c7):
        return (c1+c2+c3+(2*c4)+(2*c5)+c6+c7)
        

    
    def is_check(self, point1,point2,point3):
        Cond_diagonal = False
        Cond_vertikal = False
        Cond_horizontal = False
        if((point1.x - point2.y == 0) and abs(point1.x - point1.y == 1) and (point3.y - point1.y == 0 and abs(point3.x - point1.x == 1))):
            Cond_horizontal = True

        if((point1.x - point2.x == 0 and abs(point1.y - point2.y == 1)) and (point3.x - point1.x == 0 and abs(point3.y - point1.y == 1))):
            Cond_vertikal = True
            
        if(self.is_diagonal(point1, point2, point3)):
            Cond_diagonal = True
            
        return (Cond_horizontal or Cond_vertikal or Cond_horizontal)    
    

    def is_streak(self, point1: Tuple[int, int], point2: Tuple[int, int], point3: Tuple[int, int], point4: Tuple[int, int]):
        if(point1[0] == point2[0] and point2[0] == point3[0] and point3[0] == point4[0] and point1[1] == point2[1] - 1
        and point2[1] == point3[1] - 1 and point3[1] == point4[1] - 1):
            return True
        elif(point1[1] == point2[1] and point2[1] == point3[1] and point3[1] == point4[1] and point1[0] == point2[0] - 1
        and point2[0] == point3[0] - 1 and point3[0] == point4[0] - 1):
            return True
        elif(self.is_diagonal(point1, point2) and self.is_diagonal(point2, point3) and self.is_diagonal(point3, point4)) :
            return True
        

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement

            
            