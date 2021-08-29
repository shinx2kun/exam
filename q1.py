"""
# 実行コマンド
python q1.py

# パラメーター
なし

# テストデータ
Log/q1.log

# 出力結果
Result/q1.txt
"""

import pprint

## 設問1
class Q1:
	def __init__(self, logdata):
		self.format_data = {}
		self.err_data = {}
		self.logdata = logdata

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
				time = value[i][0]
				status = value[i][1]
				if status == "-":
					err_starttime = time
					for j in range(i+1, log_len):
						time = value[j][0]
						status = value[j][1]
						i = j
						if status == "-":
							continue
						else:
							err_endtime = time
							self.err_data.setdefault(ip,[])
							self.err_data[ip].append([err_starttime, err_endtime])
							break
				i+=1
			if status == "-":
				self.err_data.setdefault(ip,[])
				self.err_data[ip].append([err_starttime, time])
		return self.err_data
	##
##

f = open("Log/q1.log", "r")
logdata = f.readlines()

q1 = Q1(logdata)
format_data = q1.data_format()

timeout_result = q1.detect_timeout(format_data)

pprint.pprint(timeout_result, indent=4)
