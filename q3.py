"""
# 概要
pingの応答にタイムアウトが含まれている場合、無条件で過負荷状態であると言う判定となります
連続して過負荷状態がある場合、直近m回の一番手前の時間から、最後の時間までを高負荷状態の扱いとしています

# 実行コマンド
python q3.py

# パラメーター
151,2行目のm,tにて任意の値を指定

# テストデータ
Log/q3log.log

# 出力結果
Result/q3.txt
"""

import pprint
import re

## 設問3
class Q3:
	def __init__(self, logdata, N, m, t):
		self.format_data = {}
		self.timeout_data = {}
		self.highload_data = {}
		self.logdata = logdata
		self.num = N
		self.m = m
		self.t = t

	## ログファイルの整形
	def data_format(self):
		for onedata in self.logdata:
			listdata = onedata.split(",")
			time = listdata[0]
			ip = listdata[1]
			status = listdata[2].replace("\n","")
			self.format_data.setdefault(ip,[])
			self.format_data[ip].append([time,status])
		return self.format_data
	##

	## 通信断の検知
	def detect_timeout(self, format_data):
		for ip, value in format_data.items():
			ms_data = ["None"]*self.m
			log_len = len(value)
			i = 0
			while i < log_len:
				count = 0
				time = value[i][0]
				status = value[i][1]
				if status == "-":
					count += 1
					err_starttime = time
					for j in range(i+1, log_len):
						time = value[j][0]
						status = value[j][1]
						i = j
						if status == "-":
							count += 1
						else:
							err_endtime = time
							if count >= self.num:
								self.timeout_data.setdefault(ip,[])
								self.timeout_data[ip].append([err_starttime, err_endtime])
							break
				i+=1
			if status == "-" and count >= self.num:
				self.timeout_data.setdefault(ip,[])
				self.timeout_data[ip].append([err_starttime, time])
		return self.timeout_data
	##

	## 過負荷の検知
	def detect_highload(self, format_data):
		for ip, value in format_data.items():
			ms_data = ["None"]*self.m
			log_len = len(value)
			i = 0
			while i < log_len:
				count = 0
				time = value[i][0]
				status = value[i][1]
				highload_data = self.cal_average_time(ms_data, i, ip, value)
				if status == "-":
					count += 1
					for j in range(i+1, log_len):
						time = value[j][0]
						status = value[j][1]
						highload_data = self.cal_average_time(ms_data, j, ip, value)
						i = j
						if status == "-":
							count += 1
						else:
							break
				i+=1
		return highload_data
	##

	## 応答平均時間の算出
	def cal_average_time(self, ms_data, i, ip, value):
		highload_data = self.highload_data
		ms_data.pop(0)
		ms_data.append(value[i][1])
		if "-" in ms_data:
			tf = True
		else:
			ms_data = [int(ms) for ms in ms_data if re.match('^[0-9]+$', ms)]
			average_ms = sum(ms_data)/len(ms_data)
			if average_ms >= self.t:
				tf = True
			else:
				tf = False

		if tf == True:
			startnum = i+1-self.m
			if startnum < 0:
				startnum = 0
			high_starttime = value[startnum][0]
			high_endtime = value[i][0]
			highload_data = self.format_highload_data(ip, high_starttime, high_endtime)
			return highload_data
		else:
			return highload_data
	##

	## 過負荷時間の整形
	def format_highload_data(self, ip, high_starttime, high_endtime):
		self.highload_data.setdefault(ip,[])
		try:
			last_endtime = int(self.highload_data[ip][-1][-1])
			if int(high_starttime) < last_endtime:
				self.highload_data[ip][-1][-1] = high_endtime
			else:
				self.highload_data[ip].append([high_starttime, high_endtime])
			return self.highload_data
		except:
			self.highload_data[ip].append([high_starttime, high_endtime])
			return self.highload_data
	##
##

f = open("Log/q3.log", "r")
logdata = f.readlines()

## 任意の連続失敗回数を指定
N = 2
m = 3
t = 15

q3 = Q3(logdata, N, m, t)
format_data = q3.data_format()

# timeout_result = q3.detect_timeout(format_data)

highload_result = q3.detect_highload(format_data)

pprint.pprint(highload_result)
