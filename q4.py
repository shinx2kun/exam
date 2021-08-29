"""
# 概要
試験時間内に完成させられませんでした。
申し訳ありません。
"""


## 設問4
import re
import ipaddress

class Q4:
	def __init__(self, logdata, N, m, t):
		self.format_data = {}
		self.ipsubnet_data = {}
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

	## 同一サブネットの検出
	def network_subnet(self, timeout_result):
		for ip, value in timeout_result.items():
			ipsubnet = ipaddress.ip_interface(ip)
			# print(value[0][0])
			# print(value[0][1])
			starttime = int(value[0][0])
			endtime = int(value[0][1])
			self.ipsubnet_data.setdefault(str(ipsubnet.network),[starttime, endtime])
			if self.ipsubnet_data[str(ipsubnet.network)][0] < starttime:
				self.ipsubnet_data[str(ipsubnet.network)][0] = starttime
			if self.ipsubnet_data[str(ipsubnet.network)][1] > endtime:
				self.ipsubnet_data[str(ipsubnet.network)][1] = endtime
		return self.ipsubnet_data
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
				time = value[i][0]
				status = value[i][1]
				highload_data = self.cal_average_time(ms_data, i, ip, value)
				if status == "-":
					for j in range(i+1, log_len):
						time = value[j][0]
						status = value[j][1]
						highload_data = self.cal_average_time(ms_data, j, ip, value)
				i+=1
		return highload_data
	##

	## 応答平均時間の算出
	def cal_average_time(self, ms_data, i, ip, value):
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
			return None
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

f = open("log.log", "r")
logdata = f.readlines()

## 任意の連続失敗回数を指定
N = 5
m = 3
t = 10

q4 = Q4(logdata, N, m, t)
format_data = q4.data_format()

timeout_result = q4.detect_timeout(format_data)
ipsubnet_data = q4.network_subnet(timeout_result)

print(ipsubnet_data)


# timeout_result = q4.detect_timeout(format_data)

# highload_result = q4.detect_highload(format_data)


