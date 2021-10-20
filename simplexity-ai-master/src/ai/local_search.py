import random
import copy
from time import time
from math import inf as infinity

from src.constant import ShapeConstant
from src.model import State
from src.utility import place
from typing import Tuple, List
from collections import Counter


class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        best_movement = self.localsearch(state, n_player)
        return best_movement
    
    def localsearch(self, state: State, n_player):
        all_movements = self.all_movements(state, n_player)
        next_player= (n_player+1)%2
        if len(all_movements) > 0:
            movement_choosed = all_movements[0]
            for movement in all_movements:
                if (self.total_point(self.apply_movement(state, movement, n_player), next_player) <\
                    self.total_point(self.apply_movement(state, movement_choosed, n_player), next_player)):
                    movement_choosed = movement       
            return movement_choosed
    
    def apply_movement(self, state: State, movement: Tuple[int, ShapeConstant], n_player: int):
        new_state = copy.deepcopy(state)
        place(new_state, n_player, movement[1], movement[0])
        return new_state

    
    def all_movements(self, state: State, n_player: int):
        movement_lists = []
        for key in state.players[n_player].quota.keys():
            if state.players[n_player].quota.get(key) > 0:
                for i in range(0, state.board.col):
                    if state.board.__getitem__((0,i)).shape == ShapeConstant.BLANK:
                        movement_lists.append((i, key))
        return movement_lists
    
    def semua(self, state: State):
        result = []
        #mendatar
        for i in range(0, state.board.row):
            for j in range(0, state.board.col-3):
                segaris = ['' for i in range(4)]
                for k in range(4):
                    segaris[k] = state.board[i, j+k]
                result.append(segaris)
        #vertikal
        for i in range (state.board.row-3):
            for j in range(state.board.col):
                segaris = ['' for i in range(4)]
                for k in range(4):
                    segaris[k] = state.board[i+k, j]
                result.append(segaris)
        # kemiringan 1
        for i in range (state.board.row-3):
            for j in range(state.board.col-3):
                segaris = ['' for i in range(4)]
                for k in range(4):
                    segaris[k] = state.board[i+k, j+k]
                result.append(segaris)
        
        for i in range (state.board.row-3):
            for j in range(3, state.board.col):
                segaris = ['' for i in range(4)]
                for k in range(4):
                    segaris[k] = state.board[i+k, j-k]
                result.append(segaris)
        return result

    def total_point(self, state: State, n_player: int):
        poin = 0
        warna = state.players[n_player].color
        bentuk = state.players[n_player].shape
        segaris = self.semua(state)
        for i in range(len(segaris) -1, -1, -1):
            bidak = segaris[i]
            banyak_blank = 0
            #hitung poin dari bentuk
            banyak_bentuk_kita = 0
            for k in range(3, -1, -1):
                if (bidak[k].shape == bentuk):
                    banyak_bentuk_kita += 1
                elif (bidak[k].shape == ShapeConstant.BLANK):
                    banyak_blank += 1
            banyak_bentuk_musuh = 4 - banyak_bentuk_kita - banyak_blank
            if(banyak_bentuk_musuh == 0):
                if(banyak_blank != 0):
                    if (banyak_bentuk_kita == 4):
                        poin += 1000000 #Menang
                    elif (banyak_bentuk_kita == 3):
                        poin += 10
                    else:
                        poin += 1

            elif (banyak_bentuk_kita == 0):
                if(banyak_blank != 4):
                    if(banyak_blank == 0):
                        poin -= 1000000 #kalah
                    elif(banyak_blank == 1):
                        poin -= 10
                    else:
                        poin -= 1
            
            #hitung poin dari warna
            banyak_warna_kita = 0
            for j in range(4):
                if (bidak[k].color == warna):
                    banyak_warna_kita += 1

            banyak_warna_musuh = 4 - banyak_blank - banyak_warna_kita
            if(banyak_warna_musuh == 0): #potential streak
                if(banyak_bentuk_kita != banyak_warna_kita): #agar tidak terhitung 2 kali
                    if(banyak_blank != 0):
                        if(banyak_warna_kita == 4): #menang
                            poin += 1000000
                        elif (banyak_warna_kita == 3):
                            poin += 10
                        else:
                            poin += 1
            if (banyak_warna_kita == 0):
                if (banyak_bentuk_musuh != banyak_warna_musuh):
                    if(banyak_blank != 4):
                        if(banyak_warna_musuh == 4):
                            poin -= 1000000
                        elif(banyak_warna_musuh == 3):
                            poin -= 10
                        else:
                            poin -= 1
        return poin

