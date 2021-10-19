import random
from time import time
from math import inf as infinity

from src.constant import ShapeConstant
from src.model import State
from utility import place

from typing import Tuple, List


class Minimax:
    def __init__(self):
        self.streak_candidates_self = []
        self.streak_candidates_enemy = []

    def all_movements(self, state: State, n_player: int):
        movement_lists = []
        for key in state.board.players[n_player].quota.keys():
            if self.state.board.players[n_player].quota.get(key) > 0:
                for i in range(0, self.state.board.col):
                    if state.board[0][i].shape == ShapeConstant.BLANK:
                        movement_lists.append((i, key))
        return movement_lists

    def minimax_decision(self, state: State, n_player: int, depth: int):
        all_movements = self.all_movements(state)
        next_player = (n_player + 1) % 2
        if len(all_movements) > 0:
            movement_choosed = all_movements[0]
            for movement in all_movements:
                if max_value(apply_movement(state, movement, next_player), depth + 1, next_player) > \
                    max_value(apply_movement(state, movement_choosed, next_player), depth + 1, next_player):
                    movement_choosed = movement       
        return movement_choosed
    
    def apply_movement(self, state: State, movement: Tuple[int, ShapeConstant], n_player: int):
        place(state, n_player, movement[1], str(movement[0]))

    def max_value(self, state: State, depth: int, n_player: int):
        if depth == 4:
            return total_point(state)
        else:
            next_player = (n_player + 1) % 2
            temp = infinity
            for movement in self.all_movements(state, n_player):
                temp = max(temp, min_value(apply_movement(state, movement, next_player), depth + 1, next_player))
            return temp
    
    def min_value(self, state: State, depth: int, n_player: int):
        if depth == 4:
            return total_point(state)
        else:
            next_player = (n_player + 1) % 2
            temp = -infinity
            for movement in self.all_movements(state, n_player):
                temp = min(temp, max_value(apply_movement(state, movement, next_player), depth + 1, next_player))
            return temp

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:

        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement
