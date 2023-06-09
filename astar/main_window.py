#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import cv2
import sys
import numpy as np
from time import time
from skimage.color import rgb2lab

from heapq import heappush, heappop
from collections import defaultdict
from itertools import count
import itertools
import datetime
img_data = "problem.ppm"
# img_data = "ppm/problemA.ppm"
text_file_path = 'solution2.txt'
img_info = [] # 画像情報を格納する配列
np.set_printoptions(suppress=True) # numpyの設定 指数表記を無くす
pieces_position_list = [] # ピースの位置情報の2次元配列
text_roll_count = [] # 回転情報の配列
limit_time=300 #秒 #時間短く
n=40
PIXEL = 1 # 何pxおきに数えるか
# end_time = datetime.datetime.now()+datetime.timedelta( minutes = int(limit_time))#終了時間 分
end_time = datetime.datetime.now()+datetime.timedelta( seconds = int(limit_time))#終了時間 秒
# サーバーから画像をダウンロード
def download():
    subprocess.run(["python3","procon32.py","download","--token=37a76c1de6d25f4b30d248f44062166811c9d0d4df361d7cad32336ed712ef73"])

# サーバーに結果をアップロード
def submit():
    subprocess.run(["python3","procon32.py","submit","--token=37a76c1de6d25f4b30d248f44062166811c9d0d4df361d7cad32336ed712ef73","-f","solution2.txt"])

# 改行変換
def change():
    subprocess.run(["nkf","-Lw","--overwrite","solution2.txt"])

# ppm画像のヘッダ情報取得
def ImgInfo():
	infile = open(img_data, 'r', encoding='utf-8', errors='ignore')
	img_info_append=img_info.append #高速化
	for _ in range(6):
		num = infile.readline().split()
		img_info_append(num)
		# print(img_info[i])
	return img_info


# ピースの位置と回転を出すときに使う関数
# L*a*b*色空間から色差を計算する関数
# def calc_colordiff(i, j, color_data1, color_data2):
#   color_data1 = rgb2lab(color_data1)
#   color_data2 = rgb2lab(color_data2)
#   if ((i == 0 or i == 1) and (j == 0 or j == 1)) or ((i == 2 or i == 3) and (j == 2 or j == 3)):
#     color_data2 = color_data2[::-1]
#   sum_temp = 0
#   colordiff = 0
#   PIXEL = 2 # 何pxおきに数えるか
#   for k in range(int(piece_size / PIXEL)): # 何ピクセル目か
#     for l in range(3): # labのどれか
#       sum_temp += (float( color_data1[k * PIXEL][l] ) - float( color_data2[k * PIXEL][l] )) ** 2
#     colordiff += np.lib.scimath.sqrt(sum_temp)
#     sum_temp = 0
#   return(colordiff / int(piece_size / PIXEL)) 
# L*a*b*色空間から色差を計算する関数
def calc_colordiff(i, j, color_data1, color_data2):
	color_data1 = rgb2lab(color_data1)
	color_data2 = rgb2lab(color_data2)
	# print(color_data2)
	if ((i == 0 or i == 1) and (j == 0 or j == 1)) or ((i == 2 or i == 3) and (j == 2 or j == 3)):
		color_data2 = color_data2[::-1]
	# PIXEL = 7 # グローバル変数にする！
	c_diff = np.sum((color_data1[::PIXEL,:] - color_data2[::PIXEL,:]) ** 2, axis=1) # l,a,bそれぞれの差を2乗した和
	c_diff = np.sqrt(c_diff) # 平方根

	return np.mean(c_diff)

# pieceの枚数から正解パズルの座標(x,y)を取得
def get_x_y(piece_num):
	row_count = line_count = 0
	for row in pieces_position_list:
		if piece_num in row:
			line_count = row.tolist().index(piece_num)
			return line_count, row_count
		else:
			row_count += 1
	# x = line_count
	# y = row_count
	# return x, y
	return row_count, line_count


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
	for i in itertools.count():
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

	# while(True):
	for i in itertools.count():
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
		x, y = get_x_y(piece_num)
		piece_num, x, y, best_buddies_log, rotation_temp, rotation_temp_list = change_pieces_result(piece_num, edge, max_edge, best_buddies_log, x, y, r_edges, rotation_temp, rotation_temp_list)

		# while(True):
		for i in itertools.count():
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
				# click_point_position_temp = np.copy(pieces_bgr_result[int(click_point[0][1] * piece_size) : int((click_point[0][1]+1) * piece_size), int(click_point[0][0] * piece_size) : int((click_point[0][0]+1) * piece_size)]) # 交換する1枚目を保存
				# pieces_bgr_result[int(click_point[0][1] * piece_size) : int((click_point[0][1]+1) * piece_size), int(click_point[0][0] * piece_size) : int((click_point[0][0]+1) * piece_size)] = np.copy(pieces_bgr_result[int(click_point[1][1] * piece_size) : int((click_point[1][1]+1) * piece_size), int(click_point[1][0] * piece_size) : int((click_point[1][0]+1) * piece_size)])
				# pieces_bgr_result[int(click_point[1][1] * piece_size) : int((click_point[1][1]+1) * piece_size), int(click_point[1][0] * piece_size) : int((click_point[1][0]+1) * piece_size)] = np.copy(click_point_position_temp)
				pieces_bgr_result[int(click_point[0][1] * piece_size) : int((click_point[0][1]+1) * piece_size), int(click_point[0][0] * piece_size) : int((click_point[0][0]+1) * piece_size)], pieces_bgr_result[int(click_point[1][1] * piece_size) : int((click_point[1][1]+1) * piece_size), int(click_point[1][0] * piece_size) : int((click_point[1][0]+1) * piece_size)]\
									= pieces_bgr_result[int(click_point[1][1] * piece_size) : int((click_point[1][1]+1) * piece_size), int(click_point[1][0] * piece_size) : int((click_point[1][0]+1) * piece_size)], pieces_bgr_result[int(click_point[0][1] * piece_size) : int((click_point[0][1]+1) * piece_size), int(click_point[0][0] * piece_size) : int((click_point[0][0]+1) * piece_size)]
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

# 移動を求めるときに使うクラス、関数
class sBoard():
	# 
	def __init__(self, board_list, distance, parent, select, udlr):
		self._array = board_list
		self.heuristic = calc_heuristic(self._array)
		self.distance = distance
		self.cost = self.distance + self.heuristic
		self.select = select
		self.udlr = udlr
		self.parent = parent
		self.hashvalue = hash(tuple([tuple(e) for e in self._array]))
     
	def _getsBoard(self):
		return self._array
	
	def _getsSelect(self):
		return self.select
	
	def _getsUdlr(self):
		return self.udlr
    
	def __hash__(self):
		return self.hashvalue

	def __eq__(self, other):
		return (print("None") if other is None else np.all(self._array == other._array))
    
	def __lt__(self, other):
		return self._array < other._array
	
# 選択可能数に基づいて座標を分割した並べ替え処理
# def astar(_select_num):
def astar(_select_num,end_time):
	global bunkatu, gyou_count, gyou, _No_Y
	_init_board = init_board.copy()  # 削除していく問題配列
	queue = []          # 待ち行列
	gyou_count = 1      # 何回「行」処理が完了したか
	select_num = _select_num  # 残りの選択回数
	_No_Y = No_Y   # 残りの行数
	bunkatu = _No_Y // select_num    # 分割数
	gyou = 0   # 削除した行数
	catch = goal_board[bunkatu - 1, No_X - 1]          # 初めの持ち手
	No = 0
	while(gyou < No_Y):

		# print(end_time)
		# print("-------------------------------------------------------------")
		# print("bunkatu")
		# print(bunkatu)
		dist_dic = {}       # 初期盤面からの手数
		visited = {}        # 訪問済みnode；過去の盤面
		# インスタンス化
		start = sBoard(_init_board, 0, None, None, None)
		end = sBoard(goal_board, 99, None, None, None)
		# open-listのstart-node（コストとインスタンスを登録）
		heappush(queue, (start.cost, next(tiebreaker), start))
		# ゴールに到達するまで新しい盤面を探索する
		while len(queue) > 0:
			No += 1                                        
			udlr = 0
			# open-listからコスト最小の探索済みnode（盤面）を取り出す
			now_tuple = heappop(queue)
			now_board = now_tuple[2]

			""" 行の処理が完了したか """
			if np.all(now_board._array[0:bunkatu] == goal_board[0 + gyou: gyou + bunkatu]):
				end = now_board
				gyou_count += 1
				_init_board = np.delete(now_board._array, np.s_[0: bunkatu], 0)
				queue.clear()

				break
			if datetime.datetime.now() > end_time:
				end = now_board
				gyou_count += 1
				_init_board = np.delete(now_board._array, np.s_[0: bunkatu], 0)
				queue.clear()

				break
			x, y = XY_coord(catch, now_board._array)  # 持ち手の２次元での場所
			select_tile.setdefault(
				catch, (str(np.base_repr(x, base=16)) + str(np.base_repr(y + gyou, base=16))))
			coord_next_OK = coord_next(x, y)
			# 次のnodeを探索；ピースのない位置へスライドを試行
			for coord in coord_next_OK:
				# print("hello")
				if(udlr > 0 and x == coord[0] and y == coord[1]):
					pass
				else:
					next_board = now_board._array.copy()  # 今の配列が入る
					next_board[y, x], next_board[coord[1], coord[0]] = next_board[coord[1], coord[0]], next_board[y, x]  # 持ち手と入れ替え
					# インスタンス化
					new_sboard = sBoard(
						next_board, now_board.distance+1, now_board, catch, udlr)
					new_distance = new_sboard.cost
					# print("next_board_after")  
					# print(next_board)  
					# print("===================================") 
					if tuple([tuple(n) for n in new_sboard._array]) not in visited or \
							new_distance < dist_dic[new_sboard]:
						# 未訪問ならばor訪問済みで今回のコストのほうが小さいならば
						# start nodeからの距離（コスト）を登録
						dist_dic[new_sboard] = new_distance
						# 訪問済みリストに登録
						visited[tuple([tuple(n)
										for n in new_sboard._array])] = new_sboard
						# 親nodeを登録
						new_sboard.parent = now_board
						# 待ち行列に登録
						heappush(queue, (new_sboard.cost,
								next(tiebreaker), new_sboard))
				udlr += 1
				

		gyou += bunkatu
		select_num -= 1
		_No_Y -= bunkatu
		if (gyou < No_Y):
			bunkatu = _No_Y // select_num
			catch = goal_board[gyou + bunkatu - 1, No_X - 1]
		var = end                                             
		sol = []
		select = []
		udlr = []
		while var != start:
			# print([var._getsBoard()])
			sol = sol + [var._getsBoard()]
			select = select + [var._getsSelect()]
			udlr = udlr + [var._getsUdlr()]
			var = var.parent
		sol = sol + [var._getsBoard()]
		sol.reverse()
		select.reverse()
		udlr.reverse()
		#######################################
		#書き出し
		#######################################
		count_udlr = 0
		for u in udlr:
			if u == 1:
				udlr[count_udlr] = "R"
			elif u == 2:
				udlr[count_udlr] = "L"
			elif u == 3:
				udlr[count_udlr] = "U"
			elif u == 4:
				udlr[count_udlr] = "D"
			count_udlr += 1
		com = defaultdict(list)
		_count = 0
		for i in select:
			com[i].append(udlr[_count])
			_count += 1
		# print(sol)
		if(gyou_count == 2):
			# if datetime.datetime.now()>end_time:
			# 	break
			with open(text_file_path, 'a', encoding='utf-8')as f:
			# print("選択回数")
				f.write(str(gyou_count - 1))
				# print(gyou_count - 1)
				for c in com:
					# print("選択tile いらないやつ")
					# print(c)
					# print("選択座標")
					f.write('\r\n'+select_tile[c])
					# print(select_tile[c])
					# print("移動回数")
					f.write('\r\n'+str(len(com[c])))
					# print(len(com[c]))
					udlr_com = ""
					for cu in com[c]:
						udlr_com += cu
					# print("移動経路")
					f.write('\r\n'+udlr_com)	
			# 		print(udlr_com)
			# print("盤面数:{0}, 試行回数:{1}".format(len(sol), No))
		elif(gyou_count >= 3):
			if not com:
				pass
			else:
				with open(text_file_path) as fi:
					li = []
					li = fi.readlines()
			# 何か余分に選択回数出してたから無理やり調整させるために-2してる
				li[1] = str(gyou_count - 2)
				
				with open(text_file_path, mode="w", encoding='utf-8') as file:
					# file.write('\r\n')
					file.writelines(li)
					# file.write('\r\n')
				with open(text_file_path, 'a', encoding='utf-8')as h:
					# print("選択回数")
					# print(gyou_count - 1)
					for c in com:
						# print("選択tile いらないやつ")
						# print(c)
						# print("選択座標")
						h.write('\r\n'+select_tile[c])
						# print(select_tile[c])
						# print("移動回数")
						h.write('\r\n'+str(len(com[c])))
						# print(len(com[c]))
						udlr_com = ""
						for cu in com[c]:
							udlr_com += cu
						# print("移動経路")
						h.write('\r\n'+udlr_com)
				# 		print(udlr_com)
				# print("盤面数:{0}, 試行回数:{1}".format(len(sol), No))
		# if datetime.datetime.now()>end_time:
		# 	break
	return

# ヒューリスティック探索を用いたコストの予測値を算出
def calc_heuristic(array):
	"""現局面からゴールまでのコスト予測値"""
	board_list = array
	same = 0
	same_ = 0
	same_all = 0
	manhattan = 0
	manhattan_ = 0
	manhattan_all = 0

	for var_1 in goal_board[gyou:gyou + bunkatu]:
		for var_2 in var_1:
			"""ゴール盤面と一致しないピースの数"""
			if np.where(goal_board[gyou:No_Y+1] == var_2) != np.where(board_list == var_2):
				same += 1
			"""ゴール盤面へ移動するときのマンハッタン距離"""
			goal_board_y, goal_board_x = np.where(
				goal_board[gyou:No_Y+1] == var_2)
			y, x = np.where(board_list == var_2)
			# print(goal_board_x)
			abs_x = abs(x - goal_board_x[0])
			abs_y = abs(y - goal_board_y[0])
			if abs_x > No_X / 2:
				abs_x = No_X - abs_x
			if abs_y > No_Y / 2 and gyou_count == 1:
				abs_y = No_Y - abs_y
			manhattan += abs_x + abs_y

	heuristic = manhattan[0]                  


	return n * heuristic

# ピースの移動処理
def coord_next(x, y):
	""" ピースのない位置へスライドできる隣接マスのXY座標のリストを返す """
	coord_next_OK = [[x, y]]
	if gyou_count == 1:
		# right
		if(x+1 < No_X):
			coord_next_OK.append([x+1, y])
		else:
			coord_next_OK.append([0, y])
		# left
		if(x-1 >= 0):
			coord_next_OK.append([x-1, y])
		else:
			coord_next_OK.append([No_X - 1, y])
		# up
		if(y-1 >= 0):
			coord_next_OK.append([x, y-1])
		else:
			coord_next_OK.append([x, No_Y - 1])
		# down
		if(y+1 < No_Y):
			coord_next_OK.append([x, y+1])
		else:
			coord_next_OK.append([x, 0])
	elif(gyou_count >= 2):
		# right
		if(x+1 < No_X):
			coord_next_OK.append([x+1, y])
		else:
			coord_next_OK.append([0, y])
		# left
		if(x-1 >= 0):
			coord_next_OK.append([x-1, y])
		else:
			coord_next_OK.append([No_X - 1, y])
		# up
		if(y-1 >= 0):
			coord_next_OK.append([x, y-1])
		else:
			coord_next_OK.append([x, y])
		# down
		if(y+1 < _No_Y):
			coord_next_OK.append([x, y+1])
		else:
			coord_next_OK.append([x, y])

	return coord_next_OK

# 盤面配列のインデックスからXY座標を返す
def XY_coord(num, board):
	"""盤面配列のインデックスからXY座標を返す"""
	y, x = np.where(board == num)
	return x[0], y[0]
# 改行変換
# def change():
#     subprocess.run(["nkf","-Lw","--overwrite","solution2.txt"])
# 終了位置を決定
def main():
	global init_board, goal_board, No_X, No_Y, tiebreaker, select_tile
	tiebreaker = count()
	select_tile = {}                # key:持ち手　value:座標(xy)
	No_X = w_grid_size                   # xの分割数
	No_Y = h_grid_size                        # yの分割数
	#_select_num = choise_count                 # 選択上限
	_select_num = 1                 # 選択上限
	if _select_num >= No_Y:
		_select_num = -(-No_Y//2)
	No_Sum = No_X * No_Y
	goal_board = pieces_position_list # 終了時のピースの位置
	init_board = np.arange(0, No_Sum, 1).reshape(No_Y, No_X) # 開始時のピースの位置

	# print(goal_board)
	# print("init_board")
	# print(init_board)
	# print("=============================")
	astar(_select_num,end_time)
	# astar(_select_num)

# プログラム全体の流れ
if __name__ == '__main__':
	start = time()
	print(start)
	download() # 画像をダウンロード
	# ピースの位置、回転を求める
	ImgInfo() # 画像情報の取得

	# ppm画像
	choise_count=int(img_info[2][1]) #選択回数
	w_image_size = int(img_info[4][0]) #元画像の幅
	h_image_size = int(img_info[4][1]) #元画像の高さ
	w_grid_size = int(img_info[1][1]) #横の1辺が何ピースか
	h_grid_size = int(img_info[1][2]) #縦の1辺が何ピースか

	piece_size = int( w_image_size / w_grid_size ) #1ピースの幅
	num_of_pieces =  w_grid_size * h_grid_size #全部で何ピースか
	image_bgr = cv2.imread(img_data)
	# PIXEL = 1 # 何pxおきに数えるか
	#image_lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
	# image_lab = rgb2lab(image_bgr)
	color_data = [] # ピースごとの色情報
	# print(image_lab)
	pieces_bgr = [] # bgrに変換した値

	pieces_position_list = np.array([[-1.0] * w_grid_size for i in range(h_grid_size)]) # ピースの位置情報の2次元配列
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
	
	print_image()

	# 回転情報の書き出し
	text_roll_count_result = list(map(str, text_roll_count_result)) # 文字列に変換
	with open(text_file_path, 'w', encoding='utf-8')as f:
		f.write(''.join(text_roll_count_result)+'\r\n')

	# ピースの移動を求める
	print("向き探索終了")
	main()
	# print("最終結果")
	# print("位置情報")
	# print(pieces_position_list)
	# print("回転情報")
	# print(text_roll_count_temp)
	
	# print(goal_board)
	time = time() - start
	print("time:{0}".format(time) + "[sec]")
	change() 
	submit() # 結果をアップロード