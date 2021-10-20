import random
import copy
from time import time
from math import inf as infinity

from src.constant import ShapeConstant
from src.model import State
from src.utility import place
from collections import Counter

from typing import Tuple, List

class Minimax:
    def __init__(self):
        self.streak_candidates_self = []
        self.streak_candidates_enemy = []

    def all_movements(self, state: State, n_player: int):
        movement_lists = []
        for key in state.players[n_player].quota.keys():
            if state.players[n_player].quota.get(key) > 0:
                for i in range(0, state.board.col):
                    if state.board.__getitem__((0,i)).shape == ShapeConstant.BLANK:
                        movement_lists.append((i, key))
        return movement_lists

    def minimax_decision(self, state: State, n_player: int, depth: int):
        all_movements = self.all_movements(state, n_player)
        next_player = (n_player + 1) % 2
        if len(all_movements) > 0:
            movement_choosed = all_movements[0]
            for movement in all_movements:
                if self.max_value(self.apply_movement(state, movement, next_player), depth + 1, next_player) > \
                    self.max_value(self.apply_movement(state, movement_choosed, next_player), depth + 1, next_player):
                    movement_choosed = movement       
            return movement_choosed
    
    def apply_movement(self, state: State, movement: Tuple[int, ShapeConstant], n_player: int):
        new_state = copy.deepcopy(state)
        place(new_state, n_player, movement[1], movement[0])
        return new_state

    def max_value(self, state: State, depth: int, n_player: int):
        if depth == 4:
            return self.total_point(state, n_player)
        else:
            next_player = (n_player + 1) % 2
            temp = infinity
            for movement in self.all_movements(state, n_player):
                temp = max(temp, self.min_value(self.apply_movement(state, movement, next_player), depth + 1, next_player))
            return temp
    
    def min_value(self, state: State, depth: int, n_player: int):
        if depth == 4:
            return self.total_point(state, n_player)
        else:
            next_player = (n_player + 1) % 2
            temp = -infinity
            for movement in self.all_movements(state, n_player):
                temp = min(temp, self.max_value(self.apply_movement(state, movement, next_player), depth + 1, next_player))
            return temp

    # Neighbors digunakan untuk mencari empat posisi segaris yang melewati sebuah titik
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

    # Bernilai true ketika dua titik bersebelahan secara diagonal
    def is_diagonal(self, point1: Tuple[int, int],point2: Tuple[int, int]):
        return(
            abs(point1[0] - point2[0]) == 1 and abs(point1[1] - point2[1]) == 1
        )
    
    # Bernilai true ketika dua titik bersebelahan secara horizontal
    def is_horizontal(self, point1: Tuple[int, int], point2: Tuple[int, int]):
        return (
            (point1[0] == point2[0] and abs(point1[1] - point2[1]) == 1)
        )

    # Bernilai true ketika dua titik bersebelahan secara vertikal
    def is_vertikal(self, point1: Tuple[int, int], point2: Tuple[int, int]):
        return (
            (point1[1] == point2[1] and abs(point1[0] - point2[0]) == 1)
        )

    # Bernilai true ketika dua titik hanya terpisah satu titik kosoong secara horizontal
    def is_near_horizontal(self, state: State, point1: Tuple[int, int], point2: Tuple[int, int]):
        return (
            point1[0] == point2[0] and abs(point1[1] - point2[1]) == 2 and 
            state.board.__getitem__((point1[0], (point1[1] + point2[1])//2)).shape == ShapeConstant.BLANK
        )

    # Bernilai true ketika dua titik hanya terpisah satu titik kosong secara vertikal
    def is_near_vertikal(self, state: State, point1: Tuple[int, int], point2: Tuple[int, int]):
        return (
            point1[1] == point2[1] and abs(point1[0] - point2[0]) == 2 and 
            state.board.__getitem__(((point1[0] + point2[0])//2, point1[1])).shape == ShapeConstant.BLANK
        )

    # Bernilai true ketika dua titik hanya terpisah satu titik kosong secara diagonal
    def is_near_diagonal(self, state: State, point1: Tuple[int, int], point2: Tuple[int, int]):
        return (
            abs(point1[1] - point2[1]) == 2 and abs(point1[0] - point2[0]) == 2 and
            state.board.__getitem__(((point1[0] + point2[0])//2, (point1[1] + point2[1])//2)).shape == ShapeConstant.BLANK
        )

    # Bernilai true ketika tiga titik ini bisa membentuk streak apabila ditambah satu pion lagi
    # Diasumsikan titik-titik ini sudah terurut
    def is_check3(self, state: State, point1: Tuple[int, int], point2: Tuple[int, int], point3: Tuple[int, int]):
        if(
            (state.board.__getitem__((point1[0], point1[1])).color == state.board.__getitem__((point2[0], point2[1])).color and
            state.board.__getitem__((point2[0], point2[1])).color == state.board.__getitem__((point3[0], point3[1])).color) or
            (state.board.__getitem__((point1[0], point1[1])).shape == state.board.__getitem__((point2[0], point2[1])).shape and
            state.board.__getitem__((point2[0], point2[1])).shape == state.board.__getitem__((point3[0], point3[1])).shape)
        ):     
            if(
                (self.is_horizontal(point1, point2) and self.is_horizontal(point2, point3)) or
                (self.is_near_horizontal(state, point1, point2) and self.is_horizontal(point2, point3)) or
                (self.is_horizontal(point1, point2) and self.is_near_horizontal(state, point2, point3))         
            ):
                return True
            elif(
                (self.is_vertikal(point1, point2) and self.is_vertikal(point2, point3)) or
                (self.is_near_vertikal(state, point1, point2) and self.is_vertikal(point2, point3)) or
                (self.is_vertikal(point1, point2) and self.is_near_vertikal(state, point2, point3))
            ):
                return True
            elif(
                (self.is_diagonal(point1, point2) and self.is_diagonal(point2, point3)) or 
                (self.is_near_diagonal(state, point1, point2) and self.is_diagonal(point2, point3)) or 
                (self.is_diagonal(point1, point2) and self.is_near_diagonal(state, point2, point3))
            ):
                return True
            else:
                return False
        else:
            return False

    def is_check4(self, state: State, point1: Tuple[int, int], point2: Tuple[int, int], point3: Tuple[int, int], point4: Tuple[int, int]):
        return(
            (self.is_check3(state, point1, point2, point3) and state.board.__getitem__((point4[0], point4[1])).shape == ShapeConstant.BLANK) or
            self.is_check3(state, point1, point3, point4) or
            self.is_check3(state, point1, point2, point4) or
            (self.is_check3(state, point2, point3, point4) and state.board.__getitem__((point1[0], point1[1])).shape == ShapeConstant.BLANK)
        )

    def find_check(self, state: State, point1: Tuple[int, int], point2: Tuple[int, int], point3: Tuple[int, int], point4: Tuple[int, int]):
        if self.is_check3(state, point1, point2, point3) and state.board.__getitem__((point4[0], point4[1])).shape == ShapeConstant.BLANK:
            return point4
        elif self.is_check3(state, point1, point3, point4):
            return point2
        elif self.is_check3(state, point1, point2, point4):
            return point3
        elif self.is_check3(state, point2, point3, point4) and state.board.__getitem__((point1[0], point1[1])).shape == ShapeConstant.BLANK:
            return point1
        else:
            return None

     # Bernilai true ketika empat titik ini membentuk streak 
     # Diasumsikan titik-titik ini sudah terurut  
    def is_streak_ordered(self, point1: Tuple[int, int], point2: Tuple[int, int], point3: Tuple[int, int], point4: Tuple[int, int]):
        if(
            is_horizontal(point1, point2) and is_horizontal(point2, point3) and is_horizontal(point3, point4)
        ): 
            return True
        elif(
            is_vertikal(point1, point2) and is_vertikal(point2, point3) and is_vertikal(point3, point4)
        ):
            return True
        elif(
            is_diagonal(point1, point2) and is_diagonal(point2, point3) and is_diagonal(point3, point4)
        ):
            return True
        else:
            return False
    
    # is_streak tetapi bisa menerima titik yang unordered
    def is_streak(self, point1: Tuple[int, int], point2: Tuple[int, int], point3: Tuple[int, int], point4: Tuple[int, int]):
        return(
            is_streak_ordered(point1, point2, point3, point4) or
            is_streak_ordered(point1, point2, point4, point3) or
            is_streak_ordered(point1, point3, point2, point4) or
            is_streak_ordered(point1, point3, point4, point2) or
            is_streak_ordered(point1, point4, point2, point3) or
            is_streak_ordered(point1, point4, point3, point2) or
            is_streak_ordered(point2, point1, point3, point4) or
            is_streak_ordered(point2, point1, point4, point3) or
            is_streak_ordered(point2, point3, point1, point4) or
            is_streak_ordered(point2, point4, point1, point3) or
            is_streak_ordered(point3, point1, point2, point4) or
            is_streak_ordered(point3, point2, point1, point4)
        )

    # Bernilai true ketika saat meletakkan bidak di sebuah titik, akan terbentuk double streak
    def is_double_streak(self, state: State, point: Tuple[int, int]):
        num_double_streak = 0
        for streak_candidate in self.streak_candidates_self:
            (point2, point3, point4) = streak_candidate
            if(is_streak(point, point2, point3, point4)):
                num_double_streak += 1
        if num_double_streak > 1:
            return True

    def potential_streaks(self, state: State, point: Tuple[int, int]):
        streak_point = 0

        # Hitung kiri
        jarak = min(3, point[0])
        for i in range(1, jarak):
            if(
                state.board[point[0] - i][point[1]].shape != state.board[point[0]][point[1]].shape and
                state.board[point[0] - i][point[1]].color != state.board[point[0]][point[1]].color
            ): break
        hitung_kiri = i

        # Hitung kanan
        jarak = min(3, 6 - point[0])
        for i in range(1, jarak):
            if(
                state.board[point[0] + i][point[1]].shape != state.board[point[0]][point[1]].shape and
                state.board[point[0] + i][point[1]].color != state.board[point[0]][point[1]].color
            ): break
        hitung_kanan = i

        horizontal = max(0, hitung_kanan + hitung_kiri - 2)

        # Hitung atas
        hitung_atas = min(3, 5 - point[1])

        # Hitung bawah
        jarak = min(3, point[1])
        for i in range(1, jarak):
            if(
                state.board[point[0]][point[1] - i].shape != state.board[point[0]][point[1]].shape and
                state.board[point[0]][point[1] - i].color != state.board[point[0]][point[1]].color
            ): break
        hitung_bawah = i

        vertikal = max(0, hitung_atas + hitung_bawah - 2)

        # Hitung kiri bawah
        jarak = min(3, point[0], point[1])
        for i in range(1, jarak):
            if(
                state.board[point[0] - i][point[1] - i].shape != state.board[point[0]][point[1]].shape and
                state.board[point[0] - i][point[1] - i].color != state.board[point[0]][point[1]].color
            ): break
        hitung_kiri_bawah = i

        # Hitung kanan atas
        jarak = min(3, 5 - point[0], 6 - point[1])
        for i in range(1, jarak):
            if(
                state.board[point[0] + i][point[1] + i].shape != state.board[point[0]][point[1]].shape and
                state.board[point[0] + i][point[1] + i].color != state.board[point[0]][point[1]].color
            ): break
        hitung_kanan_atas = i

        diagonal_kiri_ke_atas = max(0, hitung_kiri_bawah + hitung_kanan_atas - 2)

        # Hitung kiri atas
        jarak = min(3, 5 - point[1], point[0])
        for i in range(1, jarak):
            if(
                state.board[point[0] - i][point[1] + i].shape != state.board[point[0]][point[1]].shape and
                state.board[point[0] - i][point[1] + i].color != state.board[point[0]][point[1]].color
            ): break
        hitung_kiri_atas = i

        # Hitung kanan bawah
        jarak = min(3, point[1], 6 - point[0])
        for i in range(1, jarak):
            if(
                state.board[point[0] + i][point[1] + i].shape != state.board[point[0]][point[1]].shape and
                state.board[point[0] + i][point[1] + i].color != state.board[point[0]][point[1]].color
            ): break
        hitung_kanan_bawah = i

        diagonal_kanan_ke_bawah = max(0, hitung_kiri_atas + hitung_kanan_bawah - 2)

        return horizontal + vertikal + diagonal_kiri_ke_atas + diagonal_kanan_ke_bawah

    def tuple_point(self, state: State, n_player: int, point1: Tuple[int, int], point2: Tuple[int, int], point3: Tuple[int, int], point4: Tuple[int, int]):
        point = 0
        check_point = None
        if(
            state.board.__getitem__((point1[0], point1[1])).color == state.board.__getitem__((point2[0], point2[1])).color and
            state.board.__getitem__((point2[0], point2[1])).color == state.board.__getitem__((point3[0], point3[1])).color and
            state.board.__getitem__((point3[0], point3[1])).color == state.board.__getitem__((point4[0], point4[1])).color 
        ):
            if(state.board.__getitem__((point1[0], point1[1])).color == state.players[n_player].color):
                point += 10000
            else:
                point -= 10000
        elif(
            state.board.__getitem__((point1[0], point1[1])).shape == state.board.__getitem__((point2[0], point2[1])).shape and
            state.board.__getitem__((point2[0], point2[1])).shape == state.board.__getitem__((point3[0], point3[1])).shape and
            state.board.__getitem__((point3[0], point3[1])).shape == state.board.__getitem__((point4[0], point4[1])).shape
        ):
            if(state.board.__getitem__((point1[0], point1[1])).shape == state.players[n_player].shape):
                point += 10000
            else:
                point -= 10000
                    
        if(self.is_check4(state, point1, point2, point3, point4)):
            if(state.board.__getitem__((point1[0], point1[1])).color == state.players[n_player].color or
            state.board.__getitem__((point2[0], point2[1])).color == state.players[n_player].color):
                point += 5
                check_point = self.find_check(state, point1, point2, point3, point4) 
            elif(state.board.__getitem__((point1[0], point1[1])).shape == state.players[n_player].shape or
            state.board.__getitem__((point2[0], point2[1])).shape == state.players[n_player].shape):
                point += 5
                check_point = self.find_check(state, point1, point2, point3, point4)
            else:
                point -= 5
        else:
            points = [point1, point2, point3, point4]
            nonempty_points = list(filter(lambda point: state.board.__getitem__((point[0], point[1])).shape != ShapeConstant.BLANK, points))
            if(len(nonempty_points) == 2):
                if(
                    state.board.__getitem__((nonempty_points[0][0], nonempty_points[0][1])).color == state.board.__getitem__((nonempty_points[1][0], nonempty_points[1][1])).color and
                    state.board.__getitem__((nonempty_points[0][0], nonempty_points[0][1])).color == state.players[n_player].color
                ):
                    point += 1
                elif(
                    state.board.__getitem__((nonempty_points[0][0], nonempty_points[0][1])).shape == state.board.__getitem__((nonempty_points[1][0], nonempty_points[1][1])).shape and
                    state.board.__getitem__((nonempty_points[0][0], nonempty_points[0][1])).shape == state.players[n_player].shape
                ):
                    point += 1
            elif(len(nonempty_points) == 1):
                if(
                    state.board.__getitem__((nonempty_points[0][0], nonempty_points[0][1])).color == state.players[n_player].color
                ):
                    point += 1
                elif(
                    state.board.__getitem__((nonempty_points[0][0], nonempty_points[0][1])).shape == state.players[n_player].shape
                ):
                    point += 1
        return (point, check_point)

    def total_point(self, state: State, n_player: int):
        # c1  = checkmate
        # c2 = menutup checkmate
        # c3 = menciptakan double check
        # c4  = menciptakan check
        # c5 = banyak potensial streak pemain
        # c6 = banyak potensial streak musuh
        # c7 = menciptakan streak musuh
        target_points = []
        point = 0

        # Iterate over all possible tuple four points
        for row in range(0, 6):
            for column in range(0, 7):
                
                # Horizontal ke kanan
                if(column < 4):    
                    [point1, point2, point3, point4] = [(row, column + i) for i in range(0, 4)]
                    new_tuple_point = self.tuple_point(state, n_player, point1, point2, point3, point4)
                    point += new_tuple_point[0]
                    if new_tuple_point[1] != None:
                        target_points.append(new_tuple_point[1])
                # Vertikal ke bawah
                if(row < 3):
                    [point1, point2, point3, point4] = [(row + i, column) for i in range(0, 4)]
                    new_tuple_point = self.tuple_point(state, n_player, point1, point2, point3, point4)
                    point += new_tuple_point[0]
                    if new_tuple_point[1] != None:
                        target_points.append(new_tuple_point[1])
                # Diagonal kiri atas ke kanan bawah
                if(row < 3 and column < 4):
                    [point1, point2, point3, point4] = [(row + i, column + i) for i in range(0, 4)]
                    new_tuple_point = self.tuple_point(state, n_player, point1, point2, point3, point4)
                    point += new_tuple_point[0]
                    if new_tuple_point[1] != None:
                        target_points.append(new_tuple_point[1])
                # Diagonal kanan atas ke kiri bawah
                if(row < 3 and column > 2):
                    [point1, point2, point3, point4] = [(row + i, column - i) for i in range(0, 4)]
                    new_tuple_point = self.tuple_point(state, n_player, point1, point2, point3, point4)
                    point += new_tuple_point[0]
                    if new_tuple_point[1] != None:
                        target_points.append(new_tuple_point[1])

        target_point_counter = Counter(target_points)
        for (_, count) in target_point_counter.items():
            if count > 1:
                point += 1000        
        return point
                    
    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:

        self.thinking_time = time() + thinking_time

        best_movement = self.minimax_decision(state, n_player, 0)

        return best_movement
