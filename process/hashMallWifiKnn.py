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
	wifiTemp = {} #存放最终结果
	wifiHash = {} #存放最终结果
	wifiSum = {} #存放每个店铺wifi记录总量
#	os.chdir('../data/msid/')
	#open file
	f = open(fileName, 'r')
	#read file
	rows = csv.reader(f)
	#strat from the next line
	next(rows)
#	setIndex = 4
	#scan rows
	for row in rows:
		#get sid
		sid = row[1]
		if not sid in wifiTemp:
			wifiTemp[sid] = {}
		if not sid in wifiSum:
			wifiSum[sid] = 0
		#split wifi_info
		wifi = row[-1].split(';')

		#get the number of wifi
		wifiNum = len(wifi)

		for num in range(wifiNum):
			wifiSum[sid] += 1
			wifiName = wifi[num].split('|')[0]
			if wifiName not in wifiTemp[sid]:
				wifiTemp[sid][wifiName] = [0, 0, 0]
			wifiTemp[sid][wifiName][0] += 1
			wifiTemp[sid][wifiName][1] = (wifiTemp[sid][wifiName][1] * (wifiTemp[sid][wifiName][0] - 1) + int(wifi[num].split('|')[1])) / wifiTemp[sid][wifiName][0]
			wifiTemp[sid][wifiName][2] = wifiTemp[sid][wifiName][0] / wifiSum[sid]

	for sid in wifiTemp:
		index = 0
		"""
		for wifiInfo in list(wifiTemp[sid]):
			if wifiTemp[sid][wifiInfo][0] < 2:
				del wifiTemp[sid][wifiInfo]
		"""
		wifiSortfNum = {}
		wifiSortDb = {}
		wifiHash[sid] = {}
		while len(wifiHash[sid]) < 8:
			if (8+index) >= len(wifiTemp[sid]): break
			wifiSortfNum[sid] = sorted(wifiTemp[sid].items(), key=lambda s:s[1][0], reverse=True)[:(8+index)]
			wifiSortDb[sid] = sorted(wifiTemp[sid].items(), key=lambda s:s[1][1], reverse=True)[:(8+index)]
			for num in range(len(wifiSortfNum[sid])):
				for db in range(len(wifiSortDb[sid])):
					if wifiSortfNum[sid][num][0] == wifiSortDb[sid][db][0]:
						if not wifiSortfNum[sid][num][0] in wifiHash[sid]:
							wifiHash[sid][wifiSortfNum[sid][num][0]] = [0,0,0]
						wifiHash[sid][wifiSortfNum[sid][num][0]] = wifiSortfNum[sid][num][1]
			index += 1

		if wifiHash[sid] == {}:
			del wifiHash[sid]
	
	f = open("../data/dictionary_top8/m_"+mallId+"_wifi.pkl",'wb')
	pickle.dump(wifiHash, f, -1)
	f.close()

def writeMallWifiTest():
	wifiTemp = {} #存放最终结果
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
		if not sid in wifiTemp:
			wifiTemp[sid] = {}
		if not sid in wifiSum:
			wifiSum[sid] = 0
		#split wifi_info
		wifi = row[-1].split(';')

		#get the number of wifi
		wifiNum = len(wifi)

		for num in range(wifiNum):
			wifiSum[sid] += 1
			wifiName = wifi[num].split('|')[0]
			if wifiName not in wifiTemp[sid]:
				wifiTemp[sid][wifiName] = [0, 0, 0]
			wifiTemp[sid][wifiName][0] += 1
			wifiTemp[sid][wifiName][1] = (wifiTemp[sid][wifiName][1] * (wifiTemp[sid][wifiName][0] - 1) + int(wifi[num].split('|')[1])) / wifiTemp[sid][wifiName][0]
			wifiTemp[sid][wifiName][2] = wifiTemp[sid][wifiName][0] / wifiSum[sid]
		print(wifiTemp)
	for sid in wifiTemp:
		index = 0
		"""
		for wifiInfo in list(wifiTemp[sid]):
			if wifiTemp[sid][wifiInfo][0] < 2:
				del wifiTemp[sid][wifiInfo]
		"""
		wifiSortfNum = {}
		wifiSortDb = {}
		wifiHash[sid] = {}
		while not wifiHash[sid]:
			print(sid)
			print(sorted(wifiTemp[sid].items(), key=lambda s:s[1][0], reverse=True))
			wifiSortfNum[sid] = sorted(wifiTemp[sid].items(), key=lambda s:s[1][0], reverse=True)[:(9+index)]
			print(sorted(wifiTemp[sid].items(), key=lambda s:s[1][1], reverse=True))
			wifiSortDb[sid] = sorted(wifiTemp[sid].items(), key=lambda s:s[1][1], reverse=True)[:(9+index)]
			print(wifiSortfNum)
			#		print(wifiSortDb)
			for num in range(len(wifiSortfNum[sid])):
			#			print(wifiSortfNum[sid][num][0])
				for db in range(len(wifiSortDb[sid])):
			#				print(wifiSortDb[sid][db][0])
					if wifiSortfNum[sid][num][0] == wifiSortDb[sid][db][0]:
						if not wifiSortfNum[sid][num][0] in wifiHash[sid]:
							wifiHash[sid][wifiSortfNum[sid][num][0]] = [0,0,0]
						wifiHash[sid][wifiSortfNum[sid][num][0]] = wifiSortfNum[sid][num][1]
			index += 1
			print(wifiHash)

def pklCheck():
	f = open("../data/dictionary_top8/m_6803_wifi.pkl",'rb')
	sidKey = pickle.load(f)
	print(sidKey)
	f.close()
	return

if __name__ == "__main__":
#	pklCheck()
#	writeMallWifiTest()

	directory = "../data/msid/"
	dirList = os.listdir(directory)
	dirList.sort()

	for eachtxt in dirList:
		fileName = directory+eachtxt
		mallId = eachtxt.split('_')[1]
		print("write from m_%s" % mallId)
		writeMallWifi(fileName, mallId)
		print("write down m_%s" % mallId)
