"""
# 実行コマンド
python q2.py

# パラメーター
73行目のNにて任意の値を指定

# テストデータ
Log/q2log.log

# 出力結果
Result/q2.txt
"""

import pprint

## 設問2
class Q2:
	def __init__(self, logdata, N):
		self.format_data = {}
		self.timeout_data = {}
		self.logdata = logdata
		self.num = N

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
##

f = open("Log/q2.log", "r")
logdata = f.readlines()

## 任意の値を指定
N = 3

q2 = Q2(logdata, N)
format_data = q2.data_format()

timeout_result = q2.detect_timeout(format_data)

pprint.pprint(timeout_result)

