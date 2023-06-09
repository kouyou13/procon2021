#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import pickle
import itertools
import numpy as np
import subprocess
import cv2
from time import time
from skimage.color import rgb2lab
from heapq import heappush, heappop
from collections import defaultdict
from itertools import count


img_data = "./problem.ppm"
# img_data = "./ppm/problem.ppm"
text_file_path = 'solution.txt'
img_info = [] # 画像情報を格納する配列
np.set_printoptions(suppress=True) # numpyの設定 指数表記を無くす
pieces_position_list = [] # ピースの位置情報の2次元配列
text_roll_count = [] # 回転情報の配列
PIXEL = 1 # 何pxおきに数えるか


"""
3x2
"""
# #ハッシュ表呼び出し
# with open("./HashTable32.bin", mode="rb") as f:
# 	STT_32 = pickle.load(f)

# #ハッシュ値を計算する関数
# def Calc_HashValue(board):
# 	HashValue = 1
# 	board_flat = list(itertools.chain.from_iterable(board.tolist()))    
# 	for i in range(len(board_flat)):
# 		count = 0
# 		for j in range(i+1, len(board_flat)):
# 			if board_flat[i] > board_flat[j]:
# 				count+=1
# 		HashValue += count * weight[i]
# 	return HashValue


# def ShiftBySTT32(init_board, goal_board, target):
# 	# 一般化3*2盤面格納用, 初期値-1
# 	now_board = np.ones((3, 2)) * -1
# 	# 盤面から持手座標を検索し，０とおく
# 	y0, x0 = np.where(init_board==target)
# 	now_board[y0, x0] = 0
# 	# goal_boardの1行目の値を1, 2とおく
# 	y1, x1 = np.where(init_board==goal_board[0, 0])
# 	now_board[y1, x1] = 1
# 	y2, x2 = np.where(init_board==goal_board[0, 1])
# 	now_board[y2, x2] = 2
	
	
# 	# 残りの3ピースの配置パターン
# 	num = [[3, 4, 5], [3, 5, 4], [4, 3, 5], [4, 5, 3], [5, 3, 4], [5, 4, 3]]
# 	# 移動文字列格納用
# 	shift = ['','','','','','']
# 	# 最終盤面格納用 (3ピース配置パターン数分)
# 	final_board = np.ones((len(num), 3, 2)) * -1

# 	# 初期値が入っている場所に順に3, 4, 5を入れる
# 	for n in range(len(num)):
# 		now_board_copy = now_board.copy()
# 		count = 0
# 		for i in range(3):
# 			for j in range(2):
# 				# 要素が初期値の場合，順に3, 4, 5をいれる
# 				if now_board_copy[i,j] == -1:
# 					now_board_copy[i,j] = num[n][count]
# 					count += 1

# 		# 一般化盤面からCalc_HashValueでハッシュ値
# 		hashvalue = Calc_HashValue(now_board_copy)
	
# 		# ハッシュ値がテーブルにある場合
# 		if hashvalue in STT_32:
# 			# 盤面を更新
# 			next_board = STT_32[hashvalue]
# 			while True:
# 				# 1, 2が正しい位置にいれば，一般化盤面を元に戻して終了
# 				if next_board[0,0]==1 and next_board[0,1]==2:
# 					for i in range(3):
# 						for j in range(2):
# 							xx, yy = np.where(now_board_copy==next_board[i,j])
# 							final_board[n, i, j] = init_board[xx[0], yy[0]] 
# 					break
# 				# 1, 2が正しい位置にいなければ，盤面を更新
# 				else:
# 					shift[n] = shift[n] + direction[next_board[3,1]]
# 					hashvalue = next_board[3,0]
# 					next_board = STT_32[hashvalue]
	
# 	# リストの中で，最も短い探索経路のものを返り値とする
# 	shift_length = np.array([len(x) for x in shift])
# 	if shift_length.max() != 0:
# 		min_len = np.min(shift_length[np.nonzero(shift_length)])
# 		idx = np.where(shift_length==min_len)
# 		idx = idx[0]
# 		idx = idx[0]
# 		return final_board[idx,:,:], shift[idx]
# 	# ハッシュテーブルにないとき，戻り値-1  
# 	else:
# 		print('この盤面はSTT_32に登録されていません')    
# 		return -1, -1


"""
2x3
"""
# #ハッシュ表呼び出し
# with open("./HashTable23.bin", mode="rb") as f:
# 	STT_23 = pickle.load(f)

# #ハッシュ値を計算する関数
# def Calc_HashValue(board):
# 	HashValue = 1
# 	board_flat = list(itertools.chain.from_iterable(board.tolist()))    
# 	for i in range(len(board_flat)):
# 		count = 0
# 		for j in range(i+1, len(board_flat)):
# 			if board_flat[i] > board_flat[j]:
# 				count+=1
# 		HashValue += count * weight[i]
# 	return HashValue


# def ShiftBySTT23(init_board, goal_board, target):
# 	# 一般化3*2盤面格納用, 初期値-1
# 	now_board = np.ones((2, 3)) * -1
# 	# 盤面から持手座標を検索し，０とおく
# 	y0, x0 = np.where(init_board==target)
# 	now_board[y0, x0] = 0
# 	# goal_boardの1行目の値を1, 2とおく
# 	y1, x1 = np.where(init_board==goal_board[0, 0])
# 	now_board[y1, x1] = 1
# 	y2, x2 = np.where(init_board==goal_board[1, 0])
# 	now_board[y2, x2] = 4
	
# 	# 残りの3ピースの配置パターン
# 	num = [[2, 3, 5], [2, 5, 3], [3, 2, 5], [3, 5, 2], [5, 2, 3], [5, 3, 2]]
# 	# 移動文字列格納用
# 	shift = ['','','','','','']
# 	# 最終盤面格納用 (3ピース配置パターン数分)
# 	final_board = np.ones((len(num), 2, 3)) * -1
	
# 	# 初期値が入っている場所に順に3, 4, 5を入れる
# 	for n in range(len(num)):
# 		now_board_copy = now_board.copy()
# 		count = 0
# 		for i in range(2):
# 			for j in range(3):
# 				# 要素が初期値の場合，順に3, 4, 5をいれる
# 				if now_board_copy[i,j] == -1:
# 					now_board_copy[i,j] = num[n][count]
# 					count += 1

# 		# 一般化盤面からCalc_HashValueでハッシュ値
# 		hashvalue = Calc_HashValue(now_board_copy)
# 		# ハッシュ値がテーブルにある場合
# 		if hashvalue in STT_23:
# 			# 盤面を更新
# 			next_board = STT_23[hashvalue]
# 			while True:
# 				# 1, 4が正しい位置にいれば，一般化盤面を元に戻して終了
# 				if next_board[0,0]==1 and next_board[1,0]==4:
# 					for i in range(2):
# 						for j in range(3):
# 							xx, yy = np.where(now_board_copy==next_board[i,j])
# 							final_board[n, i, j] = init_board[xx[0], yy[0]] 
# 					break
# 				# 1, 4が正しい位置にいなければ，盤面を更新
# 				else:
# 					shift[n] = shift[n] + direction[next_board[2,1]]
# 					hashvalue = next_board[2,0]
# 					next_board = STT_23[hashvalue]
					
# 	# リストの中で，最も短い探索経路のものを返り値とする
# 	shift_length = np.array([len(x) for x in shift])
# 	if shift_length.max() != 0:
# 		min_len = np.min(shift_length[np.nonzero(shift_length)])
# 		idx = np.where(shift_length==min_len)
# 		idx = idx[0]
# 		idx = idx[0]
# 		return final_board[idx,:,:], shift[idx]
# 	# ハッシュテーブルにないとき，戻り値-1  
# 	else:
# 		print('この盤面はSTT_23に登録されていません')    
# 		return -1, -1


"""
2x3 FINAL
"""
#ハッシュ表呼び出し
with open("./HashTable23.bin", mode="rb") as f:
	STT_23f = pickle.load(f)

# def BubbleSort(num):
# 	c = 0
# 	for i in range(len(num)):
# 		for j in range(len(num)-1, i, -1):
# 		   if num[j] < num[j-1]:
# 			  num[j], num[j-1] = num[j-1], num[j]
# 			  c+=1
# 	return c

#ハッシュ値を計算する関数
def Calc_HashValue(board):
	HashValue = 1
	board_flat = list(itertools.chain.from_iterable(board.tolist()))    
	for i in range(len(board_flat)):
		count = 0
		for j in range(i+1, len(board_flat)):
			if board_flat[i] > board_flat[j]:
				count+=1
		HashValue += count * weight[i]
	return HashValue


def ShiftBySTT23_Final(init_board, goal_board, target):
	# 一般化3*2盤面格納用, 初期値-1
	now_board = np.ones((2, 3)) * -1
	final_board = np.ones((2, 3)) * -1
	# 盤面から持手座標を検索し，０とおく
	count = 0
	num = [1, 2, 3, 4, 5, 0]

	for i in range(2):
		for j in range(3):
			y0, x0 = np.where(init_board==goal_board[i,j])
			now_board[y0, x0] = num[count]
			count += 1

	# 一般化盤面からCalc_HashValueでハッシュ値
	hashvalue = Calc_HashValue(now_board)
	# 移動文字列格納用
	shift = ''
	
	# ハッシュ値がテーブルにない場合，持ち手を変えて入れ替え
	if hashvalue in STT_23f:
		
		# 盤面を更新
		next_board = STT_23f[hashvalue]
		while True:
			# 正しい位置にいれば，一般化盤面を元に戻して終了
			if next_board[2,0] == -1:
				for i in range(2):
					for j in range(3):
						xx, yy = np.where(now_board==next_board[i,j])
						final_board[i, j] = init_board[xx[0], yy[0]] 
				return final_board, shift
			# 正しい位置にいなければ，盤面を更新
			else:
				shift += direction[next_board[2,1]]
				hashvalue = next_board[2,0]
				next_board = STT_23f[hashvalue]
	else:
		print('この盤面はSTT_23fに登録されていません')    
		return -1, -1


"""
移動です
"""
def DSolving():
	global _init_board, _goal_board, noda_x, noda_y, catch, udlr_com, udlr_com_list , udlr_com_2, save_catch_x, save_catch_y, sentakukaisu, save_catch_x_2, save_catch_y_2,save_catch_x_3, save_catch_y_3, catch_x, catch_y, coord
	_init_board = init_board.copy()
	# gyou_count = 1
	catch = goal_board[No_Y - 1, No_X - 1]  #持ち手の数字
	catch_x, catch_y = XY_coord(catch, _init_board)  # 持ち手の座標
	save_catch_x = catch_x
	save_catch_y = catch_y

	# 行が入る([0,1,2])
	noda_x = 0    # 行の最後の２列の判定
	noda_y = 0   # 最後の２行目までの判定
	for gyou in goal_board:
		# ゴールするまで
		if np.all(_init_board == goal_board):
			# print(goal_board)
			break
		
		# 最後の２行まで
		if noda_y < No_Y - 2:
			noda_x = 0    # 行の最後の２列の判定
			# 列が入る(0,1,2)
			for retu in gyou:
				# 最後の２列まで
				if noda_x < No_X - 1:
					if noda_x == No_X - 2 and _init_board[noda_y, noda_x + 1] == goal_board[noda_y, noda_x]:
						pass
					else:
						Judgement(retu)
						# if noda_x == No_X - 3 and _init_board[noda_y, noda_x + 1] == goal_board[noda_y, noda_x + 1]:
						# 	print("RRULD")
						# 	print(_init_board)
						# 	_init_board[noda_y + 1, noda_x], _init_board[noda_y + 1, noda_x + 1], _init_board[noda_y + 1, noda_x + 2], _init_board[noda_y, noda_x + 1], _init_board[noda_y, noda_x + 2]\
						# 	= _init_board[noda_y + 1, noda_x + 1], _init_board[noda_y + 1, noda_x], _init_board[noda_y, noda_x + 2], _init_board[noda_y + 1, noda_x + 2], _init_board[noda_y, noda_x + 1]
						# 	udlr_com.append("RRULD")
						# 	"""
						# 	RRULD
						# 	"""
						# 	print(_init_board)
				else:
					# 行の最後の数字が定位置の時 45
					if np.all(_init_board[noda_y : noda_y + 2, No_X - 1] == goal_board[noda_y, No_X - 2 : :]):
						if _init_board[noda_y + 1, No_X - 2] != catch:
							coord = []
							_x_, _y_ = XY_coord(catch, _init_board)
							coord.append([_y_, _x_])
							ma_x = No_X - 2 - _x_
							ma_y = noda_y + 1 - _y_
							# print(ma_x, ma_y)
							for _ in range(abs(ma_x)):
								if ma_x > 0:
									# print(_y_, _x_ + 1)
									# 右に移動
									coord.append([_y_, _x_ + 1])
									_x_ += 1
								if ma_x < 0:
									# 左に移動
									coord.append([_y_, _x_ - 1])
									_x_ -= 1
							for __ in range(abs(ma_y)):
								if ma_y < 0:
									# 上に移動
									coord.append([_y_ - 1, _x_])
									_y_ -= 1
								elif ma_y > 0:
									# 下に移動
									coord.append([_y_ + 1, _x_])
									_y_ += 1
							# print(coord)
							Udlr(coord)
							coord = []
						print("URD")
						print(_init_board)
						_init_board[noda_y + 1, noda_x - 1], _init_board[noda_y, noda_x - 1], _init_board[noda_y, noda_x], _init_board[noda_y + 1, noda_x]\
						 = _init_board[noda_y, noda_x - 1], _init_board[noda_y, noda_x], _init_board[noda_y + 1, noda_x], _init_board[noda_y + 1, noda_x - 1]
						udlr_com.append("URD")
						"""
						URD
						"""
						print(_init_board)
					# 54
					elif _init_board[noda_y, noda_x - 1] == goal_board[noda_y, noda_x]:
						if _init_board[noda_y + 1, No_X - 2] != catch:
							coord = []
							_x_, _y_ = XY_coord(catch, _init_board)
							coord.append([_y_, _x_])
							ma_x = No_X - 2 - _x_
							ma_y = noda_y + 1 - _y_
							# print(ma_x, ma_y)
							for _ in range(abs(ma_x)):
								if ma_x > 0:
									# print(_y_, _x_ + 1)
									# 右に移動
									coord.append([_y_, _x_ + 1])
									_x_ += 1
								if ma_x < 0:
									# 左に移動
									coord.append([_y_, _x_ - 1])
									_x_ -= 1
							for __ in range(abs(ma_y)):
								if ma_y < 0:
									# 上に移動
									coord.append([_y_ - 1, _x_])
									_y_ -= 1
							# print(coord)
							Udlr(coord)
							coord = []
						print("URDDLURULDDRULURD")
						print(_init_board)
						_init_board[noda_y, noda_x - 1], _init_board[noda_y, noda_x], _init_board[noda_y + 1, noda_x - 1], _init_board[noda_y + 1, noda_x], _init_board[noda_y + 2, noda_x]\
						= _init_board[noda_y, noda_x], _init_board[noda_y, noda_x - 1], _init_board[noda_y + 2, noda_x], _init_board[noda_y + 1, noda_x - 1], _init_board[noda_y + 1, noda_x]
						udlr_com.append("URDDLURULDDRULURD")
						"""
						URDDLURULDDRULURD
						"""
						print(_init_board)
					# 5が入ってない時
					else:
						Judgement(retu)
						if _init_board[noda_y + 1, No_X - 2] != catch:
							coord = []
							_x_, _y_ = XY_coord(catch, _init_board)
							coord.append([_y_, _x_])
							ma_x = No_X - 2 - _x_
							ma_y = noda_y + 1 - _y_
							for _ in range(abs(ma_x)):
								if ma_x > 0:
									# 右に移動
									coord.append([_y_, _x_ + 1])
									_x_ += 1
								if ma_x < 0:
									# 左に移動
									coord.append([_y_, _x_ - 1])
									_x_ -= 1
							for __ in range(abs(ma_y)):
								if ma_y < 0:
									# 上に移動
									coord.append([_y_ - 1, _x_])
									_y_ -= 1
							if _init_board[noda_y, No_X - 2] == goal_board[noda_y, No_X - 2] and _init_board[noda_y + 1, No_X - 1] == goal_board[noda_y, No_X - 1]:
								# 下に移動
								coord.append([_y_ + 1, _x_])
								_y_ += 1
								# 右に移動
								coord.append([_y_, _x_ + 1])
								_x_ += 1
								# 上に移動
								coord.append([_y_ - 1, _x_])
								_y_ -= 1
								# 上に移動
								coord.append([_y_ - 1, _x_])
								_y_ -= 1
								# 左に移動
								coord.append([_y_, _x_ - 1])
								_x_ -= 1
								# 下に移動
								coord.append([_y_ + 1, _x_])
								_y_ += 1
								# 右に移動
								coord.append([_y_, _x_ + 1])
								_x_ += 1
								# 下に移動
								coord.append([_y_ + 1, _x_])
								_y_ += 1
								# 左に移動
								coord.append([_y_, _x_ - 1])
								_x_ -= 1
								# 上に移動
								coord.append([_y_ - 1, _x_])
								_y_ -= 1
							Udlr(coord)
							coord = []
						print("URD")
						print(_init_board)
						_init_board[noda_y + 1, noda_x - 1], _init_board[noda_y, noda_x - 1], _init_board[noda_y, noda_x], _init_board[noda_y + 1, noda_x]\
						= _init_board[noda_y, noda_x - 1], _init_board[noda_y, noda_x], _init_board[noda_y + 1, noda_x], _init_board[noda_y + 1, noda_x - 1]
						udlr_com.append("URD")
						"""
						URD
						"""
						print(_init_board)
				noda_x += 1
		else:
			break
		noda_y += 1
	#     # if noda_x == No_X - 1:
	#     #     noda_y == 0
	#     # 下の２行の処理
	noda_x = 0    # 行の最後の２列の判定
	for noda_x in range(No_X - 3):
		if np.all(_init_board[No_Y - 2 : :, noda_x] == goal_board[No_Y - 2 : :, noda_x]):
			pass
		else:
			retu = goal_board[No_Y - 2 : No_Y, noda_x]
			print(retu[0])
			JudgementExtra(retu[0])
			if np.all(_init_board[No_Y - 1, noda_x : noda_x + 2] == goal_board[No_Y - 2::, noda_x]):
				if _init_board[No_Y - 2, noda_x + 1] != catch:
					coord = []
					_x_, _y_ = XY_coord(catch, _init_board)
					coord.append([_y_, _x_])
					ma_x = noda_x + 1 - _x_
					ma_y = No_Y - 2 - _y_
					# print(ma_x, ma_y)
					for _ in range(abs(ma_x)):
						if ma_x > 0:
							# print(_y_, _x_ + 1)
							# 右に移動
							coord.append([_y_, _x_ + 1])
							_x_ += 1
						if ma_x < 0:
							# 左に移動
							coord.append([_y_, _x_ - 1])
							_x_ -= 1
					for __ in range(abs(ma_y)):
						if ma_y < 0:
							# 上に移動
							coord.append([_y_ - 1, _x_])
							_y_ -= 1
						elif ma_y > 0:
							# 下に移動
							coord.append([_y_ + 1, _x_])
							_y_ += 1
					# print(coord)
					Udlr(coord)
					coord = []
				print("LDR")
				print(_init_board)
				_init_board[No_Y - 2, noda_x], _init_board[No_Y - 2, noda_x + 1], _init_board[No_Y - 1, noda_x], _init_board[No_Y - 1, noda_x + 1]\
				= _init_board[No_Y - 1, noda_x], _init_board[No_Y - 2, noda_x], _init_board[No_Y - 1, noda_x + 1], _init_board[No_Y - 2, noda_x + 1]
				udlr_com.append("LDR")
				"""
				LDR
				"""
				print(_init_board)
			
			if np.all(_init_board[No_Y - 1, noda_x] == goal_board[No_Y - 2, noda_x] and _init_board[No_Y - 2, noda_x] == goal_board[No_Y - 1, noda_x]):
				if _init_board[No_Y - 2, noda_x + 1] != catch:
					coord = []
					_x_, _y_ = XY_coord(catch, _init_board)
					coord.append([_y_, _x_])
					ma_x = noda_x + 1 - _x_
					ma_y = No_Y - 2 - _y_
					print(ma_x, ma_y)
					for _ in range(abs(ma_x)):
						if ma_x > 0:
							print(_y_, _x_ + 1)
							# 右に移動
							coord.append([_y_, _x_ + 1])
							_x_ += 1
						if ma_x < 0:
							# 左に移動
							coord.append([_y_, _x_ - 1])
							_x_ -= 1
					for __ in range(abs(ma_y)):
						if ma_y < 0:
							# 上に移動
							coord.append([_y_ - 1, _x_])
							_y_ -= 1
						elif ma_y > 0:
							# 下に移動
							coord.append([_y_ + 1, _x_])
							_y_ += 1
					print(coord)
					Udlr(coord)
					coord = []
				print("LDRRULDLURRDLULDR")
				print(_init_board)
				_init_board[No_Y - 2, noda_x], _init_board[No_Y - 1, noda_x], _init_board[No_Y - 2, noda_x + 1], _init_board[No_Y - 1, noda_x + 1], _init_board[No_Y - 1, noda_x + 2]\
				= _init_board[No_Y - 1, noda_x], _init_board[No_Y - 2, noda_x], _init_board[No_Y - 1, noda_x + 2], _init_board[No_Y - 2, noda_x + 1], _init_board[No_Y - 1, noda_x + 1]
				udlr_com.append("LDRRULDLURRDLULDR")
				"""
				LDRRULDLURRDLULDR
				"""
				print(_init_board)

			# if _init_board[No_Y - 1, noda_x + 1] != goal_board[No_Y - 1, noda_x] and _init_board[No_Y - 1, noda_x + 1] != goal_board[No_Y - 1, noda_x]:
			if _init_board[No_Y - 2, noda_x] != goal_board[No_Y - 2, noda_x] and _init_board[No_Y - 1, noda_x] != goal_board[No_Y - 1, noda_x]:
				print(retu[1])
				JudgementExtra(retu[1])
			if np.all(_init_board[No_Y - 1, noda_x : noda_x + 2] == goal_board[No_Y - 2::, noda_x]):
				if _init_board[No_Y -1, noda_x + 2] != catch:
					coord = []
					_x_, _y_ = XY_coord(catch, _init_board)
					coord.append([_y_, _x_])
					ma_x = noda_x + 2 - _x_
					ma_y = No_Y - 1 - _y_
					for _ in range(abs(ma_x)):
						if ma_x > 0:
							# 右に移動
							coord.append([_y_, _x_ + 1])
							_x_ += 1
						if ma_x < 0:
							# 左に移動
							coord.append([_y_, _x_ - 1])
							_x_ -= 1
					for __ in range(abs(ma_y)):
						if ma_y < 0:
							# 下に移動
							coord.append([_y_ + 1, _x_])
							_y_ += 1
					Udlr(coord)
					coord = []



				print("ULLDR")
				print(_init_board)
				_init_board[No_Y - 2, noda_x], _init_board[No_Y - 2, noda_x + 1], _init_board[No_Y - 2, noda_x + 2], _init_board[No_Y - 1, noda_x + 2], _init_board[No_Y - 1, noda_x + 1], _init_board[No_Y - 1, noda_x]\
				= _init_board[No_Y - 1, noda_x], _init_board[No_Y - 2, noda_x], _init_board[No_Y - 2, noda_x + 1], _init_board[No_Y - 2, noda_x + 2], _init_board[No_Y - 1, noda_x + 2], _init_board[No_Y - 1, noda_x + 1]
				udlr_com.append("ULLDR")
				"""
				ULLDR
				"""
				print(_init_board)

	print("最後の23")
	print(_init_board)
	print("持ち手:" + str(catch))
	board, shift = ShiftBySTT23_Final(_init_board[No_Y -2 : :, No_X - 3 : :], goal_board[No_Y -2 : :, No_X - 3 : :], catch)
	# 持ち手以外の隣り合った数を入れ替えるインデックス
	exchg = [[3,4],[3,4],[3,4],[0,1],[0,1],[0,1]]
	if shift == -1:
		ng = list(_init_board[No_Y -2 : :, No_X - 3 : :].reshape(6))
		ng_idx = ng.index(catch)
		catch_2 = ng[exchg[ng_idx][0]]
		save_catch_x_2, save_catch_y_2 = XY_coord(catch_2, _init_board) # 持ち手を変更
		_init_board[save_catch_y_2, save_catch_x_2], _init_board[save_catch_y_2, save_catch_x_2 + 1] = _init_board[save_catch_y_2, save_catch_x_2 + 1], _init_board[save_catch_y_2, save_catch_x_2]
		udlr_com_3.append("R")
		save_catch_x_3, save_catch_y_3 = XY_coord(catch, _init_board) # 持ち手を変更
		print('解けなかったので持ち手を',catch_2,'に入れ替えます')
		ng[exchg[ng_idx][0]], ng[exchg[ng_idx][1]] = ng[exchg[ng_idx][1]], ng[exchg[ng_idx][0]]
		_init_board[No_Y -2 : :, No_X - 3 : :] = np.array(ng).reshape(2,3)
		board, shift = ShiftBySTT23_Final(_init_board[No_Y -2 : :, No_X - 3 : :], goal_board[No_Y -2 : :, No_X - 3 : :], catch)
		# shift = 'R' + shift
		sentakukaisu += 2 # 選択回数を追加
		udlr_com_2.append(shift)
	else:
		udlr_com.append(shift)
		udlr_com_list = (''.join(udlr_com))
	_init_board[No_Y -2 : :, No_X - 3 : :] = board
	print("ゴールボード")
	print(goal_board)
	print("移動終了")
	print(_init_board)
		





	# for retu in :
	#     if noda_x < No_X - 3:
	#         JudgementExtra(retu)
	#         print("--------------------")
	#         # board, shift = ShiftBySTT23(_init_board[noda_y : noda_y + 3, No_X - 2 : :], goal_board[noda_y : noda_y + 3, No_X - 2 : :], catch)
	#     else:
			# """FINAL"""
	

def Judgement(retu):
	global init_num, coord
	""" 計算 """
	udlr_com = []
	init_num = retu # 対象の数字
	catch_x, catch_y = XY_coord(catch, _init_board)  # 持ち手の座標
	goal_x, goal_y = XY_coord(init_num, goal_board)  # 対象のゴール座標
	flag = True
	""" judge """
	while(flag):
		catch_x, catch_y = XY_coord(catch, _init_board)  # 持ち手の座標
		init_x, init_y = XY_coord(init_num, _init_board)  # 対象の座標
		# 対象と持ち手の座標の差
		manhattan_x = init_x - catch_x # xのマンハッタン 対象 - 持ち手
		manhattan_y = init_y - catch_y # yのマンハッタン 対象 - 持ち手
		# 対象のゴールまでのマンハッタン
		manhattan_goal_x = goal_x - init_x # ゴール - 対象
		manhattan_goal_y = goal_y - init_y # ゴール - 対象　
		coord = []
		coord.append([catch_y, catch_x])

		if goal_x == init_x and goal_y == init_y:
			break

		# 同じ列（ゴールが上）
		if manhattan_goal_x == 0:
			# ゴールが上(念の為)
			if manhattan_goal_y < 0:
				# 対象が持ち手の真上の時（同じ列）
				if manhattan_x == 0 and manhattan_y < 0:
					# 右に1マスずらす
					coord.append([catch_y, catch_x + 1])
					catch_x += 1
					# 対象の1マス上に移動
					for _y in range(abs(manhattan_y - 1)):
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
					# 左に1マスずらす
					coord.append([catch_y, catch_x - 1])
					catch_x -= 1
				# 持ち手が対象の左にあって，対象がゴールの１個下
				elif manhattan_x > 0 and abs(manhattan_goal_y) == 1:
					# 持ち手が対象の１個左にある
					if manhattan_x >= 1:
						coord.append([catch_y + 1, catch_x])
						catch_y += 1
					# 通り越して右に移動
					for _x in range(manhattan_x + 1):
						coord.append([catch_y, catch_x + 1])
						catch_x += 1
					# ゴールの位置まで移動
					for _y in range(manhattan_y + 1):
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
					if manhattan_x == 1:
						coord.append([catch_y + 1, catch_x])
						catch_y += 1
					coord.append([catch_y, catch_x - 1])
					catch_x -= 1
					
				# 他の箇所
				else:
					# 持ち手が対象の右にあって，対象がゴールの１個下
					if manhattan_x < 0 and abs(manhattan_goal_y) == 1 and manhattan_goal_x > 0:
						# 対象が持ち手より下
						coord.append([catch_y + 1, catch_x])
						catch_y += 1
						# 持ち手を対象の1マス上に移動(横移動)
						for _x in range(abs(manhattan_x) - 1):
							# 対象が持ち手より右
							if manhattan_x > 0:
								coord.append([catch_y, catch_x + 1])
								catch_x += 1
							# 対象が持ち手より左
							if manhattan_x < 0:
								coord.append([catch_y, catch_x - 1])
								catch_x -= 1
					else:
						# 持ち手を対象の1マス上のy軸に移動(縦移動)
						for _y in range(abs(manhattan_y - 1)):
							# 対象が持ち手より下
							if manhattan_y - 1 > 0:
								coord.append([catch_y + 1, catch_x])
								catch_y += 1
							# 対象が持ち手より上
							if manhattan_y - 1 < 0:
								coord.append([catch_y - 1, catch_x])
								catch_y -= 1
						
						# 持ち手を対象の1マス上に移動(横移動)
						for _x in range(abs(manhattan_x)):
							# 対象が持ち手より右
							if manhattan_x > 0:
								coord.append([catch_y, catch_x + 1])
								catch_x += 1
							# 対象が持ち手より左
							if manhattan_x < 0:
								coord.append([catch_y, catch_x - 1])
								catch_x -= 1
		
		# ゴールが右
		elif manhattan_goal_x > 0:
			# 対象が持ち手の真右の時（同じ行）
			if manhattan_y == 0 and manhattan_x > 0:
				# 下がない時
				if No_Y - 1 == init_y:
					# 上に１移動
					coord.append([catch_y - 1, catch_x])
					catch_y -= 1
				# 下がある時
				else:
					# 下に移動
					coord.append([catch_y + 1, catch_x])
					catch_y += 1
				# 対象の1マス右に移動
				for _x in range(abs(manhattan_x + 1)):
					coord.append([catch_y, catch_x + 1])
					catch_x += 1
				# 下がない時
				if No_Y - 1 == init_y:
					# 下に移動
					coord.append([catch_y + 1, catch_x])
					catch_y += 1
				# 下がある時
				else:
					# 上に１移動
					coord.append([catch_y - 1, catch_x])
					catch_y -= 1


			# その他
			else:
				# # # 持ち手が対象の右にあって，対象がゴールの１個下
				if manhattan_x < 0 and abs(manhattan_goal_y) == 1 and manhattan_y == 1:
					# print("noda_error")
					coord.append([catch_y + 1, catch_x])
					catch_y += 1
				#     # 対象が持ち手より下
				#     # coord.append([catch_y + 1, catch_x])
				#     # catch_y += 1
				#     # 持ち手を対象の1マス上に移動(横移動)
				#     for _x in range(abs(manhattan_x) - 1):
				#         # 対象が持ち手より右
				#         if manhattan_x > 0:
				#             coord.append([catch_y, catch_x + 1])
				#             catch_x += 1
				#         # 対象が持ち手より左
				#         if manhattan_x < 0:
				#             coord.append([catch_y, catch_x - 1])
				#             catch_x -= 1
				# else:
				# if catch_y == goal_y:
				#     print("noda_error")
				# 持ち手を対象の1マス右に移動(縦移動)
				for _y in range(abs(manhattan_y) - 1):
					# 対象が持ち手より上
					if manhattan_y < 0:
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
					# 対象が持ち手より下
					elif manhattan_y > 0:
						coord.append([catch_y + 1, catch_x])
						catch_y += 1

				# 持ち手を対象の1マス右のx軸に移動(横移動)
				for _x in range(abs(manhattan_x + 1)):
					# 対象が持ち手より左
					if manhattan_x + 1 < 0:
						coord.append([catch_y, catch_x - 1])
						catch_x -= 1
					# 対象が持ち手より右
					elif manhattan_x + 1 > 0:
						coord.append([catch_y, catch_x + 1])
						catch_x += 1

				# 対象が持ち手より上
				if manhattan_y < 0:
					coord.append([catch_y - 1, catch_x])
					catch_y -= 1
				# 対象が持ち手より下
				elif manhattan_y > 0:
					coord.append([catch_y + 1, catch_x])
					catch_y += 1

		# ゴールが左
		elif manhattan_goal_x < 0:
			# 対象が持ち手の真左
			if manhattan_y == 0 and manhattan_x < 0:
				# 下がない時
				if No_Y - 1 == init_y:
					# 上に１移動
					coord.append([catch_y - 1, catch_x])
					catch_y -= 1
				# 下がある時
				else:
					# 下に移動
					coord.append([catch_y + 1, catch_x])
					catch_y += 1
				# 持ち手を対象の1マス左のx軸に移動(横移動)
				for _x in range(abs(manhattan_x - 1)):
					coord.append([catch_y, catch_x - 1])
					catch_x -= 1
				# 下がない時
				if No_Y - 1 == init_y:
					# 下に移動
					coord.append([catch_y + 1, catch_x])
					catch_y += 1
				# 下がある時
				else:
					# 上に１移動
					coord.append([catch_y - 1, catch_x])
					catch_y -= 1

			# その他
			else:
				if manhattan_y < 0:
					# 持ち手を対象の1マス左のx軸に移動(横移動)
					for _x in range(abs(manhattan_x - 1)):
						# 対象が持ち手より左
						if manhattan_x - 1 < 0:
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
						# 対象が持ち手より右
						elif manhattan_x - 1 > 0:
							coord.append([catch_y, catch_x + 1])
							catch_x += 1
					# 縦移動
					for _y in range(abs(manhattan_y)):
						# 対象が持ち手より上
						if manhattan_y < 0:
							coord.append([catch_y - 1, catch_x])
							catch_y -= 1
						# 対象が持ち手より下
						elif manhattan_y > 0:
							coord.append([catch_y + 1, catch_x])
							catch_y += 1
				else:
					# 縦移動
					for _y in range(abs(manhattan_y)):
						# 対象が持ち手より上
						if manhattan_y < 0:
							coord.append([catch_y - 1, catch_x])
							catch_y -= 1
						# 対象が持ち手より下
						elif manhattan_y > 0:
							coord.append([catch_y + 1, catch_x])
							catch_y += 1
					# 持ち手を対象の1マス左のx軸に移動(横移動)
					for _x in range(abs(manhattan_x - 1)):
						# 対象が持ち手より左
						if manhattan_x - 1 < 0:
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
						# 対象が持ち手より右
						elif manhattan_x - 1 > 0:
							coord.append([catch_y, catch_x + 1])
							catch_x += 1
		# ゴールが下の時
		elif manhattan_goal_y > 0:
			# 縦移動
			for _y in range(abs(manhattan_y) + 1):
				# 対象が持ち手と同じ行
				if manhattan_y == 0:
					coord.append([catch_y + 1, catch_x])
					catch_y += 1
			# 持ち手を対象の1マス左のx軸に移動(横移動)
			for _x in range(abs(manhattan_x)):
				# 対象が持ち手より左
				if manhattan_x - 1 < 0:
					coord.append([catch_y, catch_x - 1])
					catch_x -= 1
				# 対象が持ち手より右
				elif manhattan_x - 1 > 0:
					coord.append([catch_y, catch_x + 1])
					catch_x += 1



		""" テンプレ移動 """
		# 対象と持ち手が同じ行
		if init_y == catch_y:
			# 対象が持ち手の右
			if (init_x - catch_x) == 1:
				# ゴールの真下に対象を移動（横移動）
				for _x in range(abs(manhattan_goal_x)):
					# 右に１移動
					coord.append([catch_y, catch_x + 1])
					catch_x += 1
					# 最後以外
					if abs(manhattan_goal_x) - 1 != _x:
						# 下がない時
						if No_Y - 1 == init_y:
							# 上に移動
							coord.append([catch_y - 1, catch_x])
							catch_y -= 1
						# 下がある時
						else:
							# 下に１移動
							coord.append([catch_y + 1, catch_x])
							catch_y += 1
						# 左に２移動
						for _ in range(2):
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
						# 下がない時
						if No_Y - 1 == init_y:
							# 下に移動
							coord.append([catch_y + 1, catch_x])
							catch_y += 1
						# 下がある時
						else:
							# 上に１移動
							coord.append([catch_y - 1, catch_x])
							catch_y -= 1
			# 対象が持ち手の左
			if (init_x - catch_x) == -1:
				# ゴールの真下に対象を移動（横移動）
				for i, _x in enumerate(range(abs(manhattan_goal_x))):
					# 左に１移動
					coord.append([catch_y, catch_x - 1])
					catch_x -= 1
					# 最後以外
					if init_x + i + 1 == No_X - 1:
						if abs(manhattan_goal_y) == 1:
							flag = False
						break
					elif abs(manhattan_goal_x) - 1 != _x:
						# 下がない時
						if No_Y - 1 == init_y:
							# 上に移動
							coord.append([catch_y - 1, catch_x])
							catch_y -= 1
						# 下がある時
						else:
							# 下に１移動
							coord.append([catch_y + 1, catch_x])
							catch_y += 1
						# 右に２移動
						for _ in range(2):
							coord.append([catch_y, catch_x + 1])
							catch_x += 1
						# 下がない時
						if No_Y - 1 == init_y:
							# 下に移動
							coord.append([catch_y + 1, catch_x])
							catch_y += 1
						# 下がある時
						else:
							# 上に１移動
							coord.append([catch_y - 1, catch_x])
							catch_y -= 1
		# 対象と持ち手が同じ列
		elif (init_y - catch_y) == 1 and init_x == catch_x:
			# ゴールに対象を移動（縦移動）
			for i, _y in enumerate(range(abs(manhattan_goal_y))):
				# 下に１移動
				coord.append([catch_y + 1, catch_x])
				catch_y += 1
				# 最後以外
				if init_x == No_X - 1 and i == abs(manhattan_goal_y) - 2:
					flag = False
					break
				elif abs(manhattan_goal_y) - 1 != _y:
					if No_X - 1 == init_x:
						# 左に１移動
						coord.append([catch_y, catch_x - 1])
						catch_x -= 1
					else:
						# 右に１移動
						coord.append([catch_y, catch_x + 1])
						catch_x += 1
					# 上に２移動
					for _ in range(2):
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
					if No_X - 1 == init_x:
						# 右に１移動
						coord.append([catch_y, catch_x + 1])
						catch_x += 1
					else:
						# 左に１移動
						coord.append([catch_y, catch_x - 1])
						catch_x -= 1
			# 行の最後の１個前の時
			if goal_x == No_X -2:
				# 右に１移動
				coord.append([catch_y, catch_x + 1])
				catch_x += 1
				# 上に１移動
				coord.append([catch_y - 1, catch_x])
				catch_y -= 1
				# 左に１移動
				coord.append([catch_y, catch_x - 1])
				catch_x -= 1
				# 下に１移動
				coord.append([catch_y + 1, catch_x])
				catch_y += 1
				flag = False
		Udlr(coord)
	return

def JudgementExtra(retu):
	global coord
	""" 計算 """
	# udlr_com = []
	init_num = retu # 対象の数字
	catch_x, catch_y = XY_coord(catch, _init_board)  # 持ち手の座標
	goal_x, goal_y = XY_coord(init_num, goal_board)  # 対象のゴール座標
	flag = True
	""" judge """
	while(flag):
		catch_x, catch_y = XY_coord(catch, _init_board)  # 持ち手の座標
		init_x, init_y = XY_coord(init_num, _init_board)  # 対象の座標
		# 対象と持ち手の座標の差
		manhattan_x = init_x - catch_x # xのマンハッタン 対象 - 持ち手
		manhattan_y = init_y - catch_y # yのマンハッタン 対象 - 持ち手
		# 対象のゴールまでのマンハッタン
		manhattan_goal_x = goal_x - init_x # ゴール - 対象
		manhattan_goal_y = goal_y - init_y # ゴール - 対象　
		coord = []
		coord.append([catch_y, catch_x])
		#ゴールするまで
		# if goal_x == init_x and goal_y == init_y:
		#     break
		# # ゴールが上の行
		# if goal_y == No_Y -2:
		#     # 対象がゴールと同じ行
		#     if manhattan_goal_y == 0:
		#         # 対象が持ち手の左
		#         if manhattan_x < 0:
		#             # 持ち手が対象と同じ行
		#             if manhattan_y == 0:
		#                 # 下に１移動
		#                 coord.append([catch_y + 1, catch_x])
		#                 catch_y += 1   
		#             for _x in range(abs(manhattan_x - 1)):
		#                 # 左に１移動
		#                 coord.append([catch_y, catch_x - 1])
		#                 catch_x -= 1
		#             # 上に１移動
		#             coord.append([catch_y - 1, catch_x])
		#             catch_y -= 1   
		#         # 対象が持ち手の右
		#         else:
		#             for _x in range(abs(manhattan_x - 1)):
		#                 # 右に１移動
		#                 coord.append([catch_y, catch_x + 1])
		#                 catch_x += 1
		#             # 持ち手が下
		#             if catch_y == No_Y - 1:
		#                 # 上に１移動
		#                 coord.append([catch_y - 1, catch_x])
		#                 catch_y -= 1
		#     # 対象がゴールと違う行
		#     elif manhattan_goal_y != 0:
		#         # 対象がゴールの真下なら
		#         if manhattan_goal_x == 0:
		#             # 同じ行
		#             if manhattan_y == 0:
		#                 # 上に１移動
		#                 coord.append([catch_y - 1, catch_x])
		#                 catch_y -= 1 
		#             for _x in range(abs(manhattan_x) - 1):
		#                 # 左に１移動
		#                 coord.append([catch_y, catch_x - 1])
		#                 catch_x -= 1
		#             flag = False
		#             break
		#         # 対象が持ち手の左
		#         if manhattan_x <= 0:
		#             # 持ち手が対象と同じ行
		#             if manhattan_y == 0:
		#                 # 上に１移動
		#                 coord.append([catch_y - 1, catch_x])
		#                 catch_y -= 1 
		#             for _x in range(abs(manhattan_x - 1)):
		#                 # 左に１移動
		#                 coord.append([catch_y, catch_x - 1])
		#                 catch_x -= 1
		#             # 下に１移動
		#             coord.append([catch_y + 1, catch_x])
		#             catch_y += 1  
		#         # 対象が持ち手の右
		#         else:
		#             for _x in range(abs(manhattan_x - 1)):
		#                 # 右に１移動
		#                 coord.append([catch_y, catch_x + 1])
		#                 catch_x += 1
		#             # 持ち手が下
		#             if catch_y == No_Y - 1:
		#                 # 上に１移動
		#                 coord.append([catch_y - 1, catch_x])
		#                 catch_y -= 1
				
		# # ゴールが下の行
		# elif goal_y == No_Y - 1:
		#     # 対象がゴールと同じ行
		#     if manhattan_goal_y == 0:
		#         # 対象が持ち手の左
		#         if manhattan_x < 0:
		#             # 対象が持ち手と同じ行
		#             if manhattan_y == 0:
		#                 # 上に１移動
		#                 coord.append([catch_y - 1, catch_x])
		#                 catch_y -= 1
		#             for _x in range(abs(manhattan_x - 1)):
		#                 # 左に１移動
		#                 coord.append([catch_y, catch_x - 1])
		#                 catch_x -= 1
		#             # 下に１移動
		#             coord.append([catch_y + 1, catch_x])
		#             catch_y += 1
		#         # 対象が持ち手の右
		#         else:
		#             for _x in range(abs(manhattan_x - 1)):
		#                 # 右に１移動
		#                 coord.append([catch_y, catch_x + 1])
		#                 catch_x += 1
		#             # 持ち手が下
		#             if catch_y == No_Y - 2:
		#                 # 下に１移動
		#                 coord.append([catch_y + 1, catch_x])
		#                 catch_y += 1
		#     # 対象がゴールと違う行
		#     elif manhattan_goal_y == 0:
		#         # 対象が持ち手の左
		#         if manhattan_x < 0:
		#             # 持ち手が対象と同じ行
		#             if manhattan_y == 0:
		#                 # 下に１移動
		#                 coord.append([catch_y + 1, catch_x])
		#                 catch_y += 1 
		#             for _x in range(abs(manhattan_x - 1)):
		#                 # 左に１移動
		#                 coord.append([catch_y, catch_x - 1])
		#                 catch_x -= 1
		#             # 上に１移動
		#             coord.append([catch_y - 1, catch_x])
		#             catch_y -= 1  
		#         # 対象が持ち手の右
		#         else:
		#             for _x in range(abs(manhattan_x - 1)):
		#                 # 右に１移動
		#                 coord.append([catch_y, catch_x + 1])
		#                 catch_x += 1
		#             # 持ち手が下
		#             if catch_y == No_Y - 1:
		#                 # 下に１移動
		#                 coord.append([catch_y + 1, catch_x])
		#                 catch_y += 1

		# """ テンプレ移動 """
		# if init_x - catch_x == 1:
		#     # ゴールが上の時
		#     if goal_y == No_Y - 2:
		#         # 対象がゴールと同じ行
		#         if manhattan_goal_y == 0:
		#             for _x in range(abs(manhattan_goal_x)):
		#                 # 右に１移動
		#                 coord.append([catch_y, catch_x + 1])
		#                 catch_x += 1
		#                 # 最後以外
		#                 if abs(manhattan_goal_x) - 1 != _x:
		#                     # 下に１移動
		#                     coord.append([catch_y + 1, catch_x])
		#                     catch_y += 1
		#                     for _x in range(2):
		#                         # 左に2移動
		#                         coord.append([catch_y, catch_x - 1])
		#                         catch_x -= 1
		#                     # 上に１移動
		#                     coord.append([catch_y - 1, catch_x])
		#                     catch_y -= 1
		#             # 最後   
		#             # 下に１移動
		#             coord.append([catch_y + 1, catch_x])
		#             catch_y += 1
		#             # 左に１移動
		#             coord.append([catch_y, catch_x - 1])
		#             catch_x -= 1
		#             # 上に１移動
		#             coord.append([catch_y - 1, catch_x])
		#             catch_y -= 1
		#             # 右に１移動
		#             coord.append([catch_y, catch_x + 1])
		#             catch_x += 1
		#             flag = False
		#             # break

		#         # 対象がゴールと違う行
		#         else:
		#             for _x in range(abs(manhattan_goal_x)):
		#                 # 右に１移動
		#                 coord.append([catch_y, catch_x + 1])
		#                 catch_x += 1
		#                 # 最後以外
		#                 if abs(manhattan_goal_x) - 1 != _x:
		#                     # 上に１移動
		#                     coord.append([catch_y - 1, catch_x])
		#                     catch_y -= 1
		#                     for _x in range(2):
		#                         # 左に2移動
		#                         coord.append([catch_y, catch_x - 1])
		#                         catch_x -= 1
		#                     # 下に１移動
		#                     coord.append([catch_y + 1, catch_x])
		#                     catch_y += 1
		#             # 最後
		#             # 右に１移動
		#             coord.append([catch_y, catch_x + 1])
		#             catch_x += 1
		#             # 上に１移動
		#             coord.append([catch_y - 1, catch_x])
		#             catch_y -= 1

		#     # ゴールが下の時
		#     elif goal_y == No_Y - 1:
		#         # 対象がゴールと同じ行
		#         if manhattan_goal_y == 0:
		#             for _x in range(abs(manhattan_goal_x) - 1):
		#                 # 右に１移動
		#                 coord.append([catch_y, catch_x + 1])
		#                 catch_x += 1
		#                 # 最後以外
		#                 if abs(manhattan_goal_x) - 1 != _x:
		#                     # 上に１移動
		#                     coord.append([catch_y - 1, catch_x])
		#                     catch_y -= 1
		#                     for _x in range(2):
		#                         # 左に2移動
		#                         coord.append([catch_y, catch_x - 1])
		#                         catch_x -= 1
		#                     # 下に１移動
		#                     coord.append([catch_y + 1, catch_x])
		#                     catch_y += 1
		#         # 対象がゴールと違う行
		#         else:
		#             # 下に１移動
		#             coord.append([catch_y + 1, catch_x])
		#             catch_y += 1
		#             # 右に１移動
		#             coord.append([catch_y, catch_x + 1])
		#             catch_x += 1
		#             # 上に１移動
		#             coord.append([catch_y - 1, catch_x])
		#             catch_y -= 1
		#             # 左に1移動
		#             coord.append([catch_y, catch_x - 1])
		#             catch_x -= 1
		#             # 下に１移動
		#             coord.append([catch_y + 1, catch_x])
		#             catch_y += 1
		#             for _x in range(abs(manhattan_goal_x) - 1):
		#                 # 右に１移動
		#                 coord.append([catch_y, catch_x + 1])
		#                 catch_x += 1
		#                 # 最後以外
		#                 if abs(manhattan_goal_x) - 1 != _x:
		#                     # 上に１移動
		#                     coord.append([catch_y - 1, catch_x])
		#                     catch_y -= 1
		#                     for _x in range(2):
		#                         # 左に2移動
		#                         coord.append([catch_y, catch_x - 1])
		#                         catch_x -= 1
		#                     # 下に１移動
		#                     coord.append([catch_y + 1, catch_x])
		#                     catch_y += 1
		
		if manhattan_goal_x == 0 and manhattan_goal_y == 0:
			ma_x = goal_x - catch_x
			# ma_y = goal_y + 1 - catch_y
			# 下に１移動
			if catch_y == No_Y - 2:
				coord.append([catch_y + 1, catch_x])
				catch_y += 1
			for _x in range(abs(ma_x)):
				# 持ち手を左に移動
				coord.append([catch_y, catch_x - 1])
				catch_x -= 1
			# 持ち手を上に移動
			coord.append([catch_y - 1, catch_x])
			catch_y -= 1
			# 持ち手を右に移動
			coord.append([catch_y, catch_x + 1])
			catch_x += 1
			flag = False

		# ゴールが上
		elif goal_y == No_Y - 2:
			# 対象が持ち手の左
			if manhattan_x < 0:
				# ゴールと対象が同じ行
				if manhattan_goal_y == 0:
					# 対象と持ち手が同じ行
					if manhattan_y == 0:
						# 持ち手を下に移動
						coord.append([catch_y + 1, catch_x])
						catch_y += 1
						# 対象の数字の１こ左に持ち手を移動
						for _x in range(abs(manhattan_x - 1)):
							# 持ち手を左に移動
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
						# 持ち手を上に移動
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
					# 対象が持ち手の上
					elif manhattan_y < 0:
						# 対象の数字の１こ左に持ち手を移動
						for _x in range(abs(manhattan_x - 1)):
							# 持ち手を左に移動
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
						# 持ち手を上に移動
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
				# ゴールと対象が違う行
				elif manhattan_goal_y < 0:
					# 対象と持ち手が同じ行
					if manhattan_y == 0:
						# 持ち手を上に移動
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
						# 対象の数字の１こ上に持ち手を移動
						for _x in range(abs(manhattan_x)):
							# 持ち手を左に移動
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
						# 持ち手を下に移動
						coord.append([catch_y + 1, catch_x])
						catch_y += 1
						manhattan_goal_y = 0
						manhattan_y = 0
					# 対象が持ち手の下
					elif manhattan_y > 0:
						# 対象の数字の１こ上に持ち手を移動
						for _x in range(abs(manhattan_x)):
							# 持ち手を左に移動
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
						# 持ち手を下に移動
						coord.append([catch_y + 1, catch_x])
						catch_y += 1
						manhattan_goal_y = 0
						manhattan_y = 0



			# 対象が持ち手の左以外
			elif manhattan_x >= 0:
				# ゴールと対象が同じ行
				if manhattan_goal_y == 0:
					# 対象と持ち手が同じ行
					if manhattan_y == 0:
						# 対象の数字の１こ左に持ち手を移動
						for _x in range(abs(manhattan_x - 1)):
							# 持ち手を右に移動
							coord.append([catch_y, catch_x + 1])
							catch_x += 1
					# 対象が持ち手の上
					elif manhattan_y < 0:
						# 対象と持ち手が同じ列
						if manhattan_x == 0:
							# 持ち手を左に移動
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
							# 持ち手を上に移動
							coord.append([catch_y - 1, catch_x])
							catch_y -= 1
						# 対象より持ち手が左
						elif manhattan_x > 0:
							# 対象の数字の１こ左に持ち手を移動
							for _x in range(abs(manhattan_x - 1)):
								# 持ち手を右に移動
								coord.append([catch_y, catch_x + 1])
								catch_x += 1
							# 持ち手を上に移動
							coord.append([catch_y - 1, catch_x])
							catch_y -= 1
				# ゴールと対象が違う行
				elif manhattan_goal_y < 0:
					# 対象と持ち手が同じ行
					if manhattan_y == 0:
						# 持ち手を上に移動
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
						# 対象の数字の１こ上に持ち手を移動
						for _x in range(abs(manhattan_x)):
							# 持ち手を右に移動
							coord.append([catch_y, catch_x + 1])
							catch_x += 1
						# 持ち手を下に移動
						coord.append([catch_y + 1, catch_x])
						catch_y += 1
						manhattan_goal_y = 0
						manhattan_y = 0
					# 対象が持ち手の下
					elif manhattan_y > 0:
						# 対象と持ち手が同じ列の時
						if manhattan_x == 0:
							# 持ち手を下に移動
							coord.append([catch_y + 1, catch_x])
							catch_y += 1
							manhattan_goal_y = 0
							manhattan_y = 0
						# 対象が持ち手の右
						elif manhattan_x > 0:
							# 対象の数字の１こ上に持ち手を移動
							for _x in range(abs(manhattan_x)):
								# 持ち手を右に移動
								coord.append([catch_y, catch_x + 1])
								catch_x += 1
							# 持ち手を下に移動
							coord.append([catch_y + 1, catch_x])
							catch_y += 1
							manhattan_goal_y = 0
							manhattan_y = 0
		# ゴールが下
		elif goal_y == No_Y - 1:
			# 対象が持ち手の左
			if manhattan_x < 0:
				# ゴールと対象が同じ行
				if manhattan_goal_y == 0:
					# 対象と持ち手が同じ行
					if manhattan_y == 0:
						# 持ち手を上に移動
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
						# 対象の数字の１こ左に持ち手を移動
						for _x in range(abs(manhattan_x - 1)):
							# 持ち手を左に移動
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
						# 持ち手を下に移動
						coord.append([catch_y + 1, catch_x])
						catch_y += 1
					# 対象が持ち手の下
					elif manhattan_y > 0:
						# 対象の数字の１こ上に持ち手を移動
						for _x in range(abs(manhattan_x)):
							# 持ち手を左に移動
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
						# 持ち手を下に移動
						coord.append([catch_y + 1, catch_x])
						catch_y += 1
				# ゴールと対象が違う行
				elif manhattan_goal_y > 0:
					# 対象と持ち手が同じ行
					if manhattan_y == 0:
						# 持ち手を下に移動
						coord.append([catch_y + 1, catch_x])
						catch_y += 1
						# 対象の数字の１こ左に持ち手を移動
						for _x in range(abs(manhattan_x - 1)):
							# 持ち手を左に移動
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
						# 持ち手を上に移動
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
						manhattan_goal_y = 0
						manhattan_y = 0
					# 対象が持ち手の上
					elif manhattan_y < 0:
						# 対象の数字の１こ下に持ち手を移動
						for _x in range(abs(manhattan_x)):
							# 持ち手を左に移動
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
						# 持ち手を上に移動
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
						manhattan_goal_y = 0
						manhattan_y = 0
			# 対象が持ち手の左以外
			elif manhattan_x >= 0: 
				# ゴールと対象が同じ行
				if manhattan_goal_y == 0:
					# 対象と持ち手が同じ行
					if manhattan_y == 0:
						# 対象の数字の１こ左に持ち手を移動
						for _x in range(abs(manhattan_x - 1)):
							# 持ち手を右に移動
							coord.append([catch_y, catch_x + 1])
							catch_x += 1
					# 対象が持ち手の下
					elif manhattan_y > 0:
						# 対象と持ち手が同じ列なら
						if manhattan_x == 0:
							# 持ち手を左に移動
							coord.append([catch_y, catch_x - 1])
							catch_x -= 1
							# 持ち手を下に移動
							coord.append([catch_y + 1, catch_x])
							catch_y += 1
						# 持ち手が対象より左
						elif manhattan_x > 0:
							# 対象の数字の１こ左に持ち手を移動
							for _x in range(abs(manhattan_x - 1)):
								# 持ち手を右に移動
								coord.append([catch_y, catch_x + 1])
								catch_x += 1
							# 持ち手を下に移動
							coord.append([catch_y + 1, catch_x])
							catch_y += 1 
				# ゴールと対象が違う行
				elif manhattan_goal_y > 0:
					# 対象と持ち手が同じ行
					if manhattan_y == 0:
						# 持ち手を下に移動
						coord.append([catch_y + 1, catch_x])
						catch_y += 1
						# 対象の数字の１こ下に持ち手を移動
						for _x in range(abs(manhattan_x)):
							# 持ち手を右に移動
							coord.append([catch_y, catch_x + 1])
							catch_x += 1
						# 持ち手を上に移動
						coord.append([catch_y - 1, catch_x])
						catch_y -= 1
						manhattan_goal_y = 0
						manhattan_y = 0
					# 対象が持ち手の上
					elif manhattan_y < 0:
						# 対象と持ち手が同じ列なら
						if manhattan_x == 0:
							# 持ち手を上に移動
							coord.append([catch_y - 1, catch_x])
							catch_y -= 1
						# 持ち手が対象より左
						elif manhattan_x > 0:
							# 対象の数字の１こ下に持ち手を移動
							for _x in range(abs(manhattan_x)):
								# 持ち手を右に移動
								coord.append([catch_y, catch_x + 1])
								catch_x += 1
							# 持ち手を上に移動
							coord.append([catch_y - 1, catch_x])
							catch_y -= 1
							manhattan_goal_y = 0
							manhattan_y = 0
		""" テンプレ移動 """
		# ゴールが上で
		if goal_y == No_Y - 2 and init_x - catch_x == 1 and init_y - catch_y == 0:
			# ゴールまで移動
			for _x in range(abs(manhattan_goal_x)):
				# 持ち手を右に移動
				coord.append([catch_y, catch_x + 1])
				catch_x += 1
				# 持ち手を下に移動
				coord.append([catch_y + 1, catch_x])
				catch_y += 1
				# 持ち手を左に移動
				coord.append([catch_y, catch_x - 1])
				catch_x -= 1
				# 最後の時
				if _x == abs(manhattan_goal_x) - 1:
					# 持ち手を上に移動
					coord.append([catch_y - 1, catch_x])
					catch_y -= 1
					# 持ち手を右に移動
					coord.append([catch_y, catch_x + 1])
					catch_x += 1
				else:
					# 持ち手を左に移動
					coord.append([catch_y, catch_x - 1])
					catch_x -= 1
					# 持ち手を上に移動
					coord.append([catch_y - 1, catch_x])
					catch_y -= 1
					
			flag = False
			
			# break

		# 
		# if goal_y == No_Y - 2 and init_x - catch_x == 0 and init_y - catch_y == -1:
		#     初めなら
		#     if:
		#         # 持ち手を左に移動
		#         coord.append([catch_y, catch_x - 1])
		#         catch_x -= 1
		#         # 持ち手を上に移動
		#         coord.append([catch_y - 1, catch_x])
		#         catch_y -= 1
		#     # 持ち手を右に移動
		#     coord.append([catch_y, catch_x + 1])
		#     catch_x += 1
		#     falg = False
		# ゴールが下で
		if goal_y == No_Y - 1 and init_x - catch_x == 1 and init_y - catch_y == 0:
			for _y in range(abs(manhattan_goal_x)-1):
				# 持ち手を右に移動
				coord.append([catch_y, catch_x + 1])
				catch_x += 1
				# 最後の時
				if _y == abs(manhattan_goal_x)-2:
					pass
				else:
					# 持ち手を上に移動
					coord.append([catch_y - 1, catch_x])
					catch_y -= 1
					# 持ち手を左に移動
					coord.append([catch_y, catch_x - 1])
					catch_x -= 1
					# 持ち手を左に移動
					coord.append([catch_y, catch_x - 1])
					catch_x -= 1
					# 持ち手を下に移動
					coord.append([catch_y + 1, catch_x])
					catch_y += 1
			flag = False
			# break
		# 
		# if goal_y == No_Y - 1 and init_x - catch_x == 0 and init_y - catch_y == 1:
		#     falg = False
				



		Udlr(coord)
		if flag == False:
			break
	return


def Udlr(coord):
	global _init_board, udlr_com
	""" 移動処理 """
	for i, _coord in enumerate(coord):
		# ２回目以降
		if i > 0:
			# 座標交換
			print(_coord)
			_init_board[_coord_old[0], _coord_old[1]], _init_board[_coord[0], _coord[1]] = _init_board[_coord[0], _coord[1]], _init_board[_coord_old[0], _coord_old[1]]
			print(_init_board)
			if _coord_old[0] - 1 == _coord[0] and _coord_old[1] == _coord[1]:
				udlr_com.append("U")
			elif _coord_old[0] + 1 == _coord[0] and _coord_old[1] == _coord[1]:
				udlr_com.append("D")
			elif _coord_old[0] == _coord[0] and _coord_old[1] - 1 == _coord[1]:
				udlr_com.append("L")
			elif _coord_old[0] == _coord[0] and _coord_old[1] + 1 == _coord[1]:
				udlr_com.append("R")
		_coord_old = _coord
	return




def XY_coord(num, board):
	""" 盤面配列のインデックスからXY座標を返す """
	y, x = np.where(board == num)
	return x[0], y[0]


def main():
	global init_board, goal_board, No_X, No_Y, select_tile, weight, direction, udlr_com, udlr_com_2, udlr_com_3, udlr_com_list, select_tile, sentakukaisu
	# tiebreaker = count()
	# Table = STT
	sentakukaisu = 1
	udlr_com = []
	udlr_com_2 = []
	udlr_com_3 = []
	udlr_com_list = ""
	save_catch_xy = []
	select_tile = {}                # key:持ち手　value:座標(xy)
	No_X = w_grid_size                      # xの分割数
	No_Y = h_grid_size               # yの分割数
	# _select_num = 10                  # 選択上限
	weight = [120, 24, 6, 2, 1, 1]
	direction = ['U','R','D','L']
	No_Sum = No_X * No_Y # ピース数
	init_board = np.arange(0, No_Sum, 1).reshape(No_Y, No_X)
	# [練習用]goal_boardランダム
	# init_board = np.arange(No_Sum)
	# np.random.shuffle(init_board)
	# init_board = np.reshape(init_board, [No_Y, No_X])
	goal_board = pieces_position_list
	# select_tile.setdefault(catch, (str(np.base_repr(x, base=16)) + str(np.base_repr(y + gyou, base=16))))
	print(goal_board)
	print("init_board")
	print(init_board)
	print("=============================")
	DSolving()
	save_catch_xy = (str(np.base_repr(save_catch_x, base=16)) + str(np.base_repr(save_catch_y, base=16)))
	udlr_com_list = (''.join(udlr_com))
	with open(text_file_path, 'a', encoding='utf-8')as f:
		f.write(str(sentakukaisu)+'\r\n') # 選択回数
		f.write(save_catch_xy+'\r\n') #持ち手の座標
		f.write(str(len(udlr_com_list))+'\r\n') # 交換回数
		f.write(udlr_com_list+'\r\n') # 移動経路
	if len(udlr_com_2) != 0:
		with open(text_file_path, 'a', encoding='utf-8')as f:
			save_catch_xy = (str(np.base_repr(save_catch_x_2, base=16)) + str(np.base_repr(save_catch_y_2, base=16)))
			udlr_com_list = (''.join(udlr_com_3))
			f.write(save_catch_xy+'\r\n')
			f.write(str(len(udlr_com_list))+'\r\n')
			f.write(udlr_com_list+'\r\n')
			save_catch_xy = (str(np.base_repr(save_catch_x_3, base=16)) + str(np.base_repr(save_catch_y_3, base=16)))
			udlr_com_list = (''.join(udlr_com_2))
			f.write(save_catch_xy+'\r\n')
			f.write(str(len(udlr_com_list))+'\r\n')
			f.write(udlr_com_list+'\r\n')

	return


# サーバーから画像をダウンロード
def download():
	subprocess.run(["python3","procon32.py","download","--token=37a76c1de6d25f4b30d248f44062166811c9d0d4df361d7cad32336ed712ef73"])

# サーバーに結果をアップロード
def submit():
	subprocess.run(["python3","procon32.py","submit","--token=37a76c1de6d25f4b30d248f44062166811c9d0d4df361d7cad32336ed712ef73","-f","solution.txt"])


# ppm画像のヘッダ情報取得
def ImgInfo():
	infile = open(img_data, 'r', encoding='utf-8', errors='ignore')
	for _ in range(6):
		num = infile.readline().split()
		img_info.append(num)
		# print(img_info[i])
	return img_info


# ピースの位置と回転を出すときに使う関数
# L*a*b*色空間から色差を計算する関数
def calc_colordiff(i, j, color_data1, color_data2):
	color_data1 = rgb2lab(color_data1)
	color_data2 = rgb2lab(color_data2)
	# print(color_data2)
	if ((i == 0 or i == 1) and (j == 0 or j == 1)) or ((i == 2 or i == 3) and (j == 2 or j == 3)):
		color_data2 = color_data2[::-1]
	c_diff = np.sum((color_data1[::PIXEL,:] - color_data2[::PIXEL,:]) ** 2, axis=1) # l,a,bそれぞれの差を2乗した和
	c_diff = np.sqrt(c_diff) # 平方根

	return np.mean(c_diff)


# 盤面配列のインデックスからXY座標を返す
def XY_coord(num, board):
	"""盤面配列のインデックスからXY座標を返す"""
	y, x = np.where(board == num)
	return x[0], y[0]


# 回転情報を返す
def turning_info(piece_num, edge, max_edge, r_edges, rotation_temp, rotation_temp_list):
	rotation_base = [0, 1, 2, 3]
	# print("edgeのあるとこ")
	# print(rotation_temp.tolist().index(edge))
	if abs(rotation_temp.tolist().index(edge) - max_edge[1]) == 2:
		text_roll_count[int(max_edge[0])] = 0

	elif rotation_temp.tolist().index(edge) == max_edge[1]:
		# r_edges[int(max_edge[0])] = np.roll(r_edges[int(max_edge[0])], 2, axis=1)# 配列の中の列をスライド
		text_roll_count[int(max_edge[0])] = 2

	elif rotation_temp.tolist().index(edge) == 0:
		# r_edges[int(max_edge[0])] = np.roll(r_edges[int(max_edge[0])], int(max_edge[1]), axis=1)
		text_roll_count[int(max_edge[0])] = int(max_edge[1])

	elif rotation_temp.tolist().index(edge) == 1:
		temp = rotation_temp.tolist().index(edge) * 3 - max_edge[1]
		# r_edges[int(max_edge[0])] = np.roll(r_edges[int(max_edge[0])], int(temp), axis=1)
		text_roll_count[int(max_edge[0])] = int(temp)

	elif rotation_temp.tolist().index(edge) == 2:
		temp = rotation_temp.tolist().index(edge) * 2 - max_edge[1]
		# r_edges[int(max_edge[0])] = np.roll(r_edges[int(max_edge[0])], int(temp), axis=1)
		text_roll_count[int(max_edge[0])] = int(temp)

	elif rotation_temp.tolist().index(edge) == 3:
		temp = rotation_temp.tolist().index(edge) / 3 + max_edge[1]
		# r_edges[int(max_edge[0])] = np.roll(r_edges[int(max_edge[0])], int(temp + rotation_temp[0]), axis=1)
		text_roll_count[int(max_edge[0])] = int(temp)

	if abs(rotation_temp.tolist().index(edge) - max_edge[1]) != 2:
		rotation_temp = np.roll(rotation_base, text_roll_count[int(max_edge[0])])
	elif abs(rotation_temp.tolist().index(edge) - max_edge[1]) == 2:
		rotation_temp = np.array(rotation_base)
	rotation_temp_list.reshape((num_of_pieces, 4))[piece_num] = rotation_temp
	return rotation_temp, rotation_temp_list


# ピースの位置を保存関数
def set_piece_poition(edge, max_edge, x, y, best_buddies_log, rotation_temp):
	global pieces_position_list
	# print("x:" + str(x))
	# print("y:" + str(y))
	if list(rotation_temp).index(int(edge)) == 0:
		y -= 1
		if y < 0 and pieces_position_list[-1][x] == -1:
			pieces_position_list = np.array(np.roll(pieces_position_list, 1, axis=0))
			y += 1
	elif list(rotation_temp).index(int(edge)) == 1:
		x += 1
	elif list(rotation_temp).index(int(edge)) == 2:
		y += 1
	elif list(rotation_temp).index(int(edge)) == 3:
		x -= 1
		if x < 0 and pieces_position_list[y][-1] == -1:
			pieces_position_list = np.array(np.roll(pieces_position_list, 1, axis=1))
			x += 1

	if pieces_position_list[y][x] == -1: # ピースが登録されていなかったら
		pieces_position_list[y][x] = int(max_edge[0])
		best_buddies_log.append(max_edge[0])
	else: # 登録されていたら
		print("中断")
		print("位置情報")
		print(pieces_position_list)
		print("回転情報")
		print(text_roll_count_result)

	return x, y, best_buddies_log


# ピースを交換した時の結果
def change_pieces_result(piece_num, edge, max_edge, best_buddies_log, x, y, r_edges, rotation_temp, rotation_temp_list):
	# print("rotation_temp")
	# print(rotation_temp)
	# print(str(piece_num) + "ピースの" + str(int(edge)) + "と")
	piece_num = int(max_edge[0])
	if piece_num != -1:

		x, y, best_buddies_log = set_piece_poition(edge, max_edge, x, y, best_buddies_log, rotation_temp) # 位置
		rotation_temp, rotation_temp_list = turning_info(piece_num, edge, max_edge, r_edges, rotation_temp, rotation_temp_list) # 回転
		# print(str(max_edge[0]) + "ピースの" + str(max_edge[1]))
		# print("ログ")
		# print(best_buddies_log)
		# print("位置")
		# print(pieces_position_list)
		# print("\n")
	return piece_num, x, y, best_buddies_log, rotation_temp, rotation_temp_list


# 評価値を使って隣接するピースを探す
def compare_values(edges):
	r_edges = [] # 残した値を格納する配列
	list_temp = []
	for i in range(num_of_pieces):
		for j in range(4):
			list_temp.append([])
		r_edges.append(list_temp)
		list_temp = []
	best_buddies_log = [] # 参照済みの辺の履歴（対象先のピースの対象に対象元を含めないため）
	for i in range(num_of_pieces):
		for j in range(4):

			# 第一候補のみ-----------------------------
			r_edges[i][j] = np.copy(edges[i][j][0])
			r_edges[i][j][2] = round(1 - edges[i][j][0][2] / edges[i][j][1][2], 5)
			#----------------------------------------

	piece_num = 0 # 何番目のピースか
	best_buddies_log = [0.0]
	max_edge = [-1, -1, -1]
	text_roll_count[0] = 0
	rotation_temp = np.array([0, 1, 2, 3]) # 基準が回転しているか（はじめの数がどれだけ回転しているか）
	rotation_temp_list = np.ones((num_of_pieces, 4)) * -1 # rotation_tempをピースごとにまとめた配列
	rotation_temp_list.reshape((num_of_pieces, 4))[0] = np.array(rotation_temp)
	x = 0
	y = 0
	# print(np.array(r_edges))
	pieces_position_list[y][x] = 0 # はじめのピースをセット
	# while(True):
	for _ in range(1000000000000000000): # ほぼ無限
		if len(best_buddies_log) == num_of_pieces:
			break
		max_edge[2] = -1
		edge = -1
		# temp = [x[0] for x in r_edges[piece_num]]
		# print(temp)
		# if len(set(temp)) != 0: # 1ピースに同じピースが含まれてたら終了
		#   break
		for i in range(4):
			# 評価値が最大の辺を探す and 参照したことのないピースから探す
			if max_edge[2] < r_edges[piece_num][i][2] and (r_edges[piece_num][i][0] in best_buddies_log) == False:
				max_edge = np.copy(r_edges[piece_num][i])
				edge = i
		if max_edge[2] < 0.4:
			break
		piece_num, x, y, best_buddies_log, rotation_temp, rotation_temp_list = change_pieces_result(piece_num, edge, max_edge, best_buddies_log, x, y, r_edges, rotation_temp, rotation_temp_list)

	for _ in range(1000000000000000000):
		if len(best_buddies_log) == num_of_pieces:
			break
		# print("--------------------")
		max_edge[2] = -1
		for piece_num_temp in range(num_of_pieces):
			if piece_num_temp in best_buddies_log:
				for i in range(4):
					# 評価値が最大の辺を探す and 参照したことのないピースから探す
					if (max_edge[2] == -1 or max_edge[2] < r_edges[piece_num_temp][i][2]) and (r_edges[piece_num_temp][i][0] in best_buddies_log) == False:
						max_edge = np.copy(r_edges[piece_num_temp][i])
						edge = i
						piece_num = piece_num_temp
						rotation_temp = rotation_temp_list.reshape((num_of_pieces, 4))[piece_num] # 回転情報を更新
		x, y = XY_coord(piece_num, pieces_position_list)
		piece_num, x, y, best_buddies_log, rotation_temp, rotation_temp_list = change_pieces_result(piece_num, edge, max_edge, best_buddies_log, x, y, r_edges, rotation_temp, rotation_temp_list)

		for _ in range(1000000000000000000):
			# if len(best_buddies_log) == num_of_pieces:
			#   break
			# temp = [x[0] for x in r_edges[piece_num]]
			# print("temp")
			# print(temp)
			# if len(set(temp)) != 0: # 1ピースに同じピースが含まれてたら終了
			#   break
			max_edge[2] = -1
			edge = -1
			for i in range(4):
				# 評価値が最大の辺を探す and 参照したことのないピースから探す
				if max_edge[2] < r_edges[piece_num][i][2] and (r_edges[piece_num][i][0] in best_buddies_log) == False:
					max_edge = np.copy(r_edges[piece_num][i])
					edge = i
			if max_edge[2] < 0.4:
				break
			piece_num, x, y, best_buddies_log, rotation_temp, rotation_temp_list = change_pieces_result(piece_num, edge, max_edge, best_buddies_log, x, y, r_edges, rotation_temp, rotation_temp_list)


# 色の違いを出す
def deff_color(color_data):
	# edges[num_of_pieces][4]の多次元配列生成 要素empty
	edges = [] # ピースごとの類似度情報を格納する配列
	list_temp = []
	for i in range(num_of_pieces):
		for j in range(4):
			list_temp.append([])
		edges.append(list_temp)
		list_temp = []

	for index1 in range(num_of_pieces): # 1枚目のピース
		for index2 in range(index1+1, num_of_pieces): # 2枚目のピース

		#if index1 != index2: # 1枚目と2枚目の重複を無くす
			for i in range(4): # 1枚目がどの向きか
				# ヒストグラムをつなげたベクトルを作る
				# histvec1 = img2hist(cv2.cvtColor(color_data[index1][i], cv2.COLOR_BGR2RGB))
				for j in range(4): # 2枚目がどの向きか
					# ヒストグラムをつなげたベクトルを作る
					# histvec2 = img2hist(cv2.cvtColor(color_data[index2][j], cv2.COLOR_BGR2RGB))
					###### どちらかを選択 ######
					# ベクトル同士の類似度を計算
					# deff_color_num = round(cv2.compareHist(histvec1, histvec2, 0), 2)

					# labに変換して色差の平均を計算
					deff_color_num = calc_colordiff(i, j, color_data[index1][i], color_data[index2][j])
					#########################
					if len(edges[index1][i]) == 0:
						edges[index1][i] = np.empty((0,3), float)
					edges[index1][i] = np.append(edges[index1][i], np.array([[index2, j, deff_color_num]]), axis=0)

					if len(edges[index2][j]) == 0:
						edges[index2][j] = np.empty((0,3), float)
					edges[index2][j] = np.append(edges[index2][j], np.array([[index1, i, deff_color_num]]), axis=0)

					deff_color_num = 0

		# 色差を基準にソート
		for i in range(4): # 1枚目がどの向きか
			temp = edges[index1][i]
			temp = temp[np.argsort(temp[:,2])] #昇順 labの時
			# temp = temp[np.argsort(-temp[:,2])] #降順 ヒストグラムの時
			edges[index1][i] = temp

	return edges
	# 小さい値ほど色が近い


def split_into_pieces():
	# 形の統一
	for i in range(num_of_pieces):
		color_data_temp = []

		# print("上辺")
		# print(pieces_bgr[i][0].shape)
		color_data_temp.append(pieces_bgr[i][0])

		color_data_temp_r = []
		for j in  range(piece_size):
			# print("右辺")
			# print(pieces_bgr[i][:, -1][j])
			color_data_temp_r.append(pieces_bgr[i][:, -1][j])
		color_data_temp.append(np.array(color_data_temp_r))

		# print("下辺")
		# print(pieces_bgr[i][-1])
		color_data_temp.append(pieces_bgr[i][-1])

		color_data_temp_l = []
		for j in  range(piece_size):
			# print("左辺")
			# print(pieces_bgr[i][:, 0][j])
			color_data_temp_l.append(pieces_bgr[i][:, 0][j])
		color_data_temp.append(color_data_temp_l)
		color_data.append(np.array(color_data_temp))
	# print(color_data[0][0][0][0]) # color_data[何ピース目][向き][何px][l, a, b]
	# [何ピース目 0~(num_of_pieces-1)] [向き 0:上,1:下,2:左,3:右] [px 0~(piece_size-1)][lab 0:l. 1:a, 2:b]


#マウスイベント処理
def mouse_event(event, x, y, flags, param):
	global click_point
	if event == cv2.EVENT_LBUTTONUP: # クリックしたら
		if mode_num == 1: # 位置の変更
			if len(click_point) == 0: # 1回目のクリック
				click_point.append(list([x // (w_image_size / w_grid_size), y // (h_image_size / h_grid_size)]))
				print("1回目")
				print("x:" + str(click_point[0][0]))
				print("y:" + str(click_point[0][1]))
			else: # 2回目のクリック
				click_point.append(list([x // (w_image_size / w_grid_size), y // (h_image_size / h_grid_size)]))
				print("2回目")
				print("x:" + str(click_point[1][0]))
				print("y:" + str(click_point[1][1]))
				# 位置情報を交換
				# change_piece_temp = np.copy(pieces_position_list[int (click_point[0][1]), int(click_point[0][0])]) # 交換する1枚目を保存（位置情報）
				# pieces_position_list[int(click_point[0][1]), int(click_point[0][0])] = pieces_position_list[int (click_point[1][1]), int(click_point[1][0])]
				# pieces_position_list[int(click_point[1][1]), int(click_point[1][0])] = change_piece_temp
				pieces_position_list[int(click_point[0][1]), int(click_point[0][0])], pieces_position_list[int(click_point[1][1]), int(click_point[1][0])]\
									= pieces_position_list[int(click_point[1][1]), int(click_point[1][0])], pieces_position_list[int(click_point[0][1]), int(click_point[0][0])]
				# 回転情報の交換
				# text_roll_count_temp = text_roll_count_result[int(h_grid_size * click_point[0][1] + click_point[0][0])] # 交換する1枚目を保存（回転情報）
				# text_roll_count_result[int(h_grid_size * click_point[0][1] + click_point[0][0])] = text_roll_count_result[int(h_grid_size * click_point[1][1] + click_point[1][0])]
				# text_roll_count_result[int(h_grid_size * click_point[1][1] + click_point[1][0])] = text_roll_count_temp
				text_roll_count_result[int(h_grid_size * click_point[0][1] + click_point[0][0])], text_roll_count_result[int(h_grid_size * click_point[1][1] + click_point[1][0])]\
									= text_roll_count_result[int(h_grid_size * click_point[1][1] + click_point[1][0])], text_roll_count_result[int(h_grid_size * click_point[0][1] + click_point[0][0])]
				# 画像の座標を交換
				click_point_position_temp = np.copy(pieces_bgr_result[int(click_point[0][1] * piece_size) : int((click_point[0][1]+1) * piece_size), int(click_point[0][0] * piece_size) : int((click_point[0][0]+1) * piece_size)]) # 交換する1枚目を保存
				pieces_bgr_result[int(click_point[0][1] * piece_size) : int((click_point[0][1]+1) * piece_size), int(click_point[0][0] * piece_size) : int((click_point[0][0]+1) * piece_size)] = np.copy(pieces_bgr_result[int(click_point[1][1] * piece_size) : int((click_point[1][1]+1) * piece_size), int(click_point[1][0] * piece_size) : int((click_point[1][0]+1) * piece_size)])
				pieces_bgr_result[int(click_point[1][1] * piece_size) : int((click_point[1][1]+1) * piece_size), int(click_point[1][0] * piece_size) : int((click_point[1][0]+1) * piece_size)] = np.copy(click_point_position_temp)
				# pieces_bgr_result[int(click_point[0][1] * piece_size) : int((click_point[0][1]+1) * piece_size), int(click_point[0][0] * piece_size) : int((click_point[0][0]+1) * piece_size)], pieces_bgr_result[int(click_point[1][1] * piece_size) : int((click_point[1][1]+1) * piece_size), int(click_point[1][0] * piece_size) : int((click_point[1][0]+1) * piece_size)]\
				# 					= pieces_bgr_result[int(click_point[1][1] * piece_size) : int((click_point[1][1]+1) * piece_size), int(click_point[1][0] * piece_size) : int((click_point[1][0]+1) * piece_size)], pieces_bgr_result[int(click_point[0][1] * piece_size) : int((click_point[0][1]+1) * piece_size), int(click_point[0][0] * piece_size) : int((click_point[0][0]+1) * piece_size)]
				print("位置変更")
				print("位置情報")
				print(pieces_position_list)
				print("回転情報")
				print(text_roll_count_result)
				click_point = []
		elif mode_num == 2: # 回転の変更
			x = x // (w_image_size / w_grid_size)
			y = y // (h_image_size / h_grid_size)
			print("x:" + str(x))
			print("y:" + str(y))
			piece_num = int(h_grid_size * y + x)
			# 回転情報の変更
			if text_roll_count_result[piece_num] != 3:
				text_roll_count_result[piece_num] += 1
			elif text_roll_count_result[piece_num] == 3:
				text_roll_count_result[piece_num] = 0

			# 画像の回転
			# 90°回転
			pieces_bgr_result[int(y * piece_size) : int((y+1) * piece_size), int(x * piece_size) : int((x+1) * piece_size)] = cv2.rotate(pieces_bgr_result[int(y * piece_size) : int((y+1) * piece_size), int(x * piece_size) : int((x+1) * piece_size)], cv2.ROTATE_90_CLOCKWISE)
			print("回転変更")
			print("位置情報")
			print(pieces_position_list)
			print("回転情報")
			print(text_roll_count_result)


# 結果を表示する関数
def puzzle_result():
	pieces_bgr_result = np.copy(image_bgr) # 画像を並べ替えた結果
	piece_size = h_image_size / h_grid_size
	for h in range(h_grid_size):
		for w in range(w_grid_size):
			piece_num = w_grid_size * h + w # ピースの番号
			x, y = XY_coord(piece_num, pieces_position_list) # 
			# pieces_bgr_result[int(y * piece_size) : int((y+1) * piece_size), int(x * piece_size) : int((x+1) * piece_size)] = image_bgr[int(y_ * piece_size) : int((y_+1) * piece_size), int(x_ * piece_size) : int((x_+1) * piece_size)]
			if text_roll_count[piece_num] == 0: # 無回転時
				pieces_bgr_result[int(y * piece_size) : int((y+1) * piece_size), int(x * piece_size) : int((x+1) * piece_size)] = image_bgr[int(h * piece_size) : int((h+1) * piece_size), int(w * piece_size) : int((w+1) * piece_size)]
			elif text_roll_count[piece_num] == 1: # 90°回転時
				pieces_bgr_result[int(y * piece_size) : int((y+1) * piece_size), int(x * piece_size) : int((x+1) * piece_size)] = cv2.rotate(image_bgr[int(h * piece_size) : int((h+1) * piece_size), int(w * piece_size) : int((w+1) * piece_size)], cv2.ROTATE_90_CLOCKWISE)
			elif text_roll_count[piece_num] == 2: # 180°回転時
				pieces_bgr_result[int(y * piece_size) : int((y+1) * piece_size), int(x * piece_size) : int((x+1) * piece_size)] = cv2.rotate(image_bgr[int(h * piece_size) : int((h+1) * piece_size), int(w * piece_size) : int((w+1) * piece_size)], cv2.ROTATE_180)
			elif text_roll_count[piece_num] == 3: # 270°回転時
				pieces_bgr_result[int(y * piece_size) : int((y+1) * piece_size), int(x * piece_size) : int((x+1) * piece_size)] = cv2.rotate(image_bgr[int(h * piece_size) : int((h+1) * piece_size), int(w * piece_size) : int((w+1) * piece_size)], cv2.ROTATE_90_COUNTERCLOCKWISE)
	return pieces_bgr_result


# 画像表示する関数
def print_image():
	global click_point, pieces_bgr_result, mode_num
	click_point = []
	pieces_bgr_result = puzzle_result()
	# cv2.imwrite("./result_img.jpg", pieces_bgr_result)
	click_point = [] # クリックした座標
	# result_img_window = cv2.imread("./result_img.jpg")
	cv2.namedWindow("result_img_window", cv2.WINDOW_KEEPRATIO) # ウィンドウ生成
	cv2.setMouseCallback("result_img_window", mouse_event)  # マウスイベント時に関数mouse_eventの処理を行う
	mode_num = 1 # 1:移動 2:回転
	print("1:位置変更, 2:回転変更, esc:終了")
	print("移動の変更")
	# while True:
	for i in range(1000000000000):
		#画像の表示
		cv2.imshow("result_img_window", pieces_bgr_result)
		#キー入力
		if cv2.waitKey(1) & 0xFF == 27: # escを押した時
			print("esc：終了")
			break # ループ終了
		if cv2.waitKey(1) & 0xFF == 49: # 1を押した時
			print("1：移動の変更")
			mode_num = 1
			continue
		if cv2.waitKey(1) & 0xFF == 50: # 2を押した時
			print("2：回転の変更")
			mode_num = 2
			continue
	cv2.destroyAllWindows()

# 改行変換
def change():
	subprocess.run(["nkf","-Lw","--overwrite","solution.txt"])


if __name__ == '__main__':
	# start = time.time()
	# file_path = 'solution.txt'

	# print(_init_board)
	# time = time.time() - start
	# print ("time:{0}".format(time) + "[sec]")




	# start = time()
	# print("開始：" + str(start))
	download() # 画像をダウンロード
	# ピースの位置、回転を求める
	ImgInfo() # 画像情報の取得

	# jpg画像
	# w_image_size = 640
	# h_image_size = 640
	# w_grid_size = 4
	# h_grid_size = 4
	# ppm画像
	choise_count=int(img_info[2][1]) #選択回数
	w_image_size = int(img_info[4][0]) #元画像の幅
	h_image_size = int(img_info[4][1]) #元画像の高さ
	w_grid_size = int(img_info[1][1]) #横の1辺が何ピースか
	h_grid_size = int(img_info[1][2]) #縦の1辺が何ピースか

	piece_size = int( w_image_size / w_grid_size ) #1ピースの幅
	num_of_pieces =  w_grid_size * h_grid_size #全部で何ピースか
	image_bgr = cv2.imread(img_data)
	# image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
	# image_lab = rgb2lab(image_bgr)
	color_data = [] # ピースごとの色情報
	# print(image_lab)
	pieces_bgr = [] # bgrに変換した値

	pieces_position_list = np.array([[-1.0] * w_grid_size for i in range(h_grid_size)], dtype='int64') # ピースの位置情報の2次元配列
	text_roll_count= [-1] * num_of_pieces # 回転情報の配列
	text_roll_count_result= [-1] * num_of_pieces
	# 全体のbgrをピースごとのbgrに分ける
	# for i in range(h_grid_size):
	# 	for j in range(w_grid_size):
	# 		pieces_bgr.append(image_bgr[i*piece_size: (i+1)*piece_size, j*piece_size: (j+1)*piece_size])
	pieces_bgr = [ image_bgr[i*piece_size: (i+1)*piece_size, j*piece_size: (j+1)*piece_size] for i in range(h_grid_size) for j in range(w_grid_size)]

	split_into_pieces() # ピースごとに分割
	edges = [] 
	edges = deff_color(color_data) # 色差を計算
	compare_values(edges) # 評価値からピースの位置を求める
	# text_roll_count = [str(s) for s in text_roll_count] # 文字列に変換
	count_roll = 0
	# 回転情報を最終位置に変える
	for i in range(h_grid_size):
		for j in range(w_grid_size):
			text_roll_count_result[count_roll] = text_roll_count[int(pieces_position_list[i][j])]
			count_roll += 1
		# print(text_roll_count)
	
	# middle = time() - start
	# print("配置：" + str(middle))
	print("結果")
	print("位置情報")
	print(pieces_position_list)
	print("回転情報")
	print(text_roll_count_result)

	print_image()

	print("最終結果")
	print("位置情報")
	print(pieces_position_list)
	print("回転情報")
	print(text_roll_count_result)

	# 回転情報の書き出し
	text_roll_count_result = list(map(str, text_roll_count_result)) # 文字列に変換
	with open(text_file_path, 'w', encoding='utf-8')as f:
		f.write(''.join(text_roll_count_result)+'\r\n')

	# ピースの移動を求める
	# print("向き探索終了")
	# main()
	# print(goal_board)
	main()
	# time = time() - start
	# print("time:{0}".format(time) + "[sec]")
	change()
	submit() # 結果をアップロード