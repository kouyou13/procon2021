# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 20:00:14 2021

@author: nakak
"""
import numpy as np

def shiftBoard(init_board, shift, catch, grid):
    # 盤面のコピー
    now_board = init_board.copy()
    
    for cmd in shift:
        # i方向に0を移動させる(移動先に値があるか？)
        d = direction[URLD.index(cmd)]
        # 持ち手の位置を検索
        y, x = np.where(now_board==catch)
        # i方向へ移動させたときの座標
        new_y = y[0] + d[1]
        new_x = x[0] + d[0]
        # 横が超えるときは，横端同士交換
        if (0 > new_x) or (new_x > grid[1]-1):
            now_board[y, grid[1]-1], now_board[y, 0] = now_board[y, 0], now_board[y, grid[1]-1]
        # 縦が越えるときは，縦端同士交換    
        elif (0 > new_y) or (new_y > grid[0]-1):
            now_board[0, x], now_board[grid[0]-1, x] = now_board[grid[0]-1, x], now_board[0, x]
        # それ以外は通常の交換
        else:
            now_board[y, x], now_board[new_y, new_x] = now_board[new_y, new_x], now_board[y, x]
            
    return now_board
            
    

if __name__ == '__main__':
    
    global URLD, direction
    
    URLD = ['U','R','D','L']
    # 上，右，下，左
    direction = np.array([
    [0, -1],
    [1, 0],
    [0, 1],
    [-1, 0]
    ])
    
    No_X = 10                        # xの分割数
    No_Y = 4                        # yの分割数
    No_Sum = No_X * No_Y # ピース数
    init_board = np.arange(0, No_Sum, 1).reshape(No_Y, No_X)
    
    grid = init_board.shape
    
    #txt読み込み
    f = open('solution1.txt', 'r')
    data = f.read().split()
    f.close()

    #2行目の数字分繰返し
    num = [j for j in range(2, 3*int(data[1])+1, 3)]
    result = init_board.copy()
    for i in num:
        #1行目から持ち手の座標取得 1文字ずつ16→10進数してinit_boardのその座標を持ち手に
        y = int(data[i][1],16)
        x = int(data[i][0],16)
        catch = init_board[y,x]

        # 移動経路
        shift = data[i+2]

        result = shiftBoard(result, shift, catch, grid)
 #    goal_board = [[ 28, 115, 232,  75,   3, 138 , 93 , 25 , 61 , 88 , 36, 207  ,81 , 24, 250,   4],
 # [205, 107,  91 , 26 , 46, 177, 241, 106, 143 ,251,  51 ,242, 223 ,249 ,248 , 56],
 # [122 ,123 , 52, 224 , 49, 101,  41, 240 , 77 ,  7 ,165,  59 ,200 ,116,  55 ,206],
 # [158 ,255 , 90 ,131 ,162,  43, 214,   0 ,216, 136 , 22 ,202 , 95 ,110 ,146 , 89],
 # [245 , 54 ,155,  78, 196, 100, 129,  48 ,174 ,184, 188 ,246 , 11 ,193, 176 ,237],
 # [209  ,69 ,194 , 74 , 18 ,  5 ,  9 ,228 , 17 ,199, 157 ,186, 126, 142,  79 , 27],
 # [124 , 20 ,121 ,105 , 84, 215 , 23 , 76, 225, 247 ,239, 150,  39 ,222, 161, 191],
 # [  6, 187 , 96 , 98,  97, 219, 160 ,189 , 80 ,163, 164, 147, 230, 170 , 12 , 21],
 # [119,  44 ,137, 204 ,212 ,168, 252 ,183 , 57 ,120 ,203 ,153 , 31 , 45 ,211 ,109],
 # [117, 148, 195,  33,  35 ,201, 210, 217, 127 , 29, 159,  65 ,208 ,236 ,140 ,144],
 # [133, 156 ,179 , 30 ,175 ,213 ,181 ,220, 132 , 40, 254 ,149 , 71 , 47 , 72 ,233],
 # [ 83,  13 ,190 ,235 ,112 ,135,  10 ,198 , 66 ,  2 , 14 ,114 ,108 ,166 ,227 , 85],
 # [180, 111 ,172 ,167  ,68 ,102 , 50,  63,  99,  16, 139 ,113  , 1 ,152 , 92 ,154],
 # [226,  15,  42, 145, 231, 130,  32, 185, 218, 118 ,244 , 87 ,103, 182, 238, 221],
 # [173,   8, 178 , 70,  60, 243, 151 , 58 , 53, 128 , 73 ,253 , 19 ,141 ,192 , 94],
 # [229, 134 ,234 , 82 , 38 ,197 ,125 ,104 , 34 , 62 , 86 , 67 , 64 ,169 , 37 ,171]]
 
    goal_board = [[8,18,16,37,17,24,9,12,39,2],
                   [1,32,34,29,23,38,21,10,15,22],
                   [0,28,20,30,27,25,14,13,19,6],
                   [7,5,11,4,3,36,26,35,31,33]]

    print(result)
    print(No_Sum - sum(sum(result==goal_board)))