#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-23 19:42:53
# @Author  : WordZzzz (wordzzzz@foxmail.com)
# @Link    : http://blog.csdn.net/u011475210
# @Version : $Id$

import os
import operator
import csv
import pickle

def writeMallWifi(fileName,mallId):
	wifiHash = {} #存放最终结果
	wifiSum = {} #存放每个店铺wifi记录总量
#	os.chdir('../data/msid/')
	f = open(fileName, 'r')
	#open file
#	f = open('test.txt','r')
	#read file
	rows = csv.reader(f)
	#strat from the next line
	next(rows)
#	setIndex = 4
	#scan rows
	for row in rows:
		#get sid
		sid = row[1]
		if not sid in wifiHash:
			wifiHash[sid] = {}
		if not sid in wifiSum:
			wifiSum[sid] = 0
		#split wifi_info
		wifi = row[-1].split(';')

		#get the number of wifi
		wifiNum = len(wifi)

		for num in range(wifiNum):
			wifiSum[sid] += 1
			wifiName = wifi[num].split('|')[0]
			if wifiName not in wifiHash[sid]:
				wifiHash[sid][wifiName] = [0, 0, 0]
			wifiHash[sid][wifiName][0] += 1
			wifiHash[sid][wifiName][1] = (wifiHash[sid][wifiName][1] * (wifiHash[sid][wifiName][0] - 1) + int(wifi[num].split('|')[1])) / wifiHash[sid][wifiName][0]
			wifiHash[sid][wifiName][2] = wifiHash[sid][wifiName][0] / wifiSum[sid]
	
	f = open("../data/dictionary/m_"+mallId+"_wifi.pkl",'wb')
	pickle.dump(wifiHash, f, -1)
	f.close()

def writeMallWifiTest():
	wifiHash = {} #存放最终结果
	wifiSum = {} #存放每个店铺wifi记录总量
	#open file
	f = open('test.txt','r')
	#read file
	rows = csv.reader(f)
	#strat from the next line
	next(rows)
#	setIndex = 4
	#scan rows
	for row in rows:
		#get sid
		sid = row[1]
		if not sid in wifiHash:
			wifiHash[sid] = {}
		if not sid in wifiSum:
			wifiSum[sid] = 0
		#split wifi_info
		wifi = row[-1].split(';')

		#get the number of wifi
		wifiNum = len(wifi)

		for num in range(wifiNum):
			wifiSum[sid] += 1
			wifiName = wifi[num].split('|')[0]
			if wifiName not in wifiHash[sid]:
				wifiHash[sid][wifiName] = [0, 0, 0]
			wifiHash[sid][wifiName][0] += 1
			wifiHash[sid][wifiName][1] = (wifiHash[sid][wifiName][1] * (wifiHash[sid][wifiName][0] - 1) + int(wifi[num].split('|')[1])) / wifiHash[sid][wifiName][0]
			wifiHash[sid][wifiName][2] = wifiHash[sid][wifiName][0] / wifiSum[sid]
		print(wifiHash)

def pklCheck():
	f = open("../data/dictionary/m_7800_wifi.pkl",'rb')
	sidKey = pickle.load(f)
	print(sidKey)
	for sid in sidKey:
		print(sid, len(sidKey[sid]))
		result = sorted(sidKey[sid].items(), key=operator.itemgetter(1), reverse=True)[:max(10, len(sidKey[sid]) // 3)]
		print(result)
		for i in result:
			print(i[0])
	f.close()
	return

if __name__ == "__main__":
	pklCheck()
#	writeMallWifiTest()
	"""
	directory = "../data/msid/"
	dirList = os.listdir(directory)
	dirList.sort()

	for eachtxt in dirList:
		fileName = directory+eachtxt
		mallId = eachtxt.split('_')[1]
		print("write from m_%s" % mallId)
		writeMallWifi(fileName, mallId)
		print("write down m_%s" % mallId)
	"""