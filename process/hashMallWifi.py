#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-18 22:54:27
# @Author  : WordZzzz (wordzzzz@foxmail.com)
# @Link    : http://blog.csdn.net/u011475210
# @Version : $Id$

import os
import operator
import csv
import pickle

#if __name__ == "__main__":
def writeMallWifi(fileName,mallId):
	wifiHash = {}
	wifiTemp = {}
	wifiSum = {}
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
		wifiInfoSort = []
		wifiInfo = {}
		#get sid
		sid = row[1]
		if not sid in wifiTemp:
			wifiTemp[sid] = {}
		#split wifi_info
		wifi = row[-1].split(';')
		#get the number of wifi
		wifiNum = len(wifi)

		for num in range(wifiNum):
			wifiInfo[wifi[num].split('|')[0]] = wifi[num].split('|')[1]
		"""
		wifiInfoSort = sorted(wifiInfo.items(), key=operator.itemgetter(1), reverse=False)[:setIndex]
		for num in range(min(setIndex,len(wifiInfoSort))):
		"""
		wifiInfoSort = sorted(wifiInfo.items(), key=operator.itemgetter(1), reverse=False)

		if not sid in wifiSum:
			wifiSum[sid] = len(wifiInfoSort)
		else:
			wifiSum[sid] += len(wifiInfoSort)

		for num in range(len(wifiInfoSort)):
			try:
				if not wifiInfoSort[num][0] in wifiTemp[sid]:
					wifiTemp[sid][wifiInfoSort[num][0]] = 0
				else:
					wifiTemp[sid][wifiInfoSort[num][0]] += 1.0
					wifiTemp[sid][wifiInfoSort[num][0]] /= wifiSum[sid]
			except:
				print(row,min(setIndex,wifiNum),wifiInfoSort)
	for sid in wifiTemp.keys():
	#	wifiHash[sid] = sorted(wifiTemp[sid].items(), key=operator.itemgetter(1), reverse=True)[:setIndex]
		wifiHash[sid] = wifiTemp[sid]
	f.close()
	
	f = open("../data/dictionary/m_"+mallId+"_wifi.pkl",'wb')
	pickle.dump(wifiHash, f, -1)
	f.close()
	"""
	f = open("../data/dictionary/m_"+mallId+"_wifi.pkl",'rb')
	sidKey = pickle.load(f)
	for key in sidKey:
		print(sidKey[key])
	f.close()
	"""

if __name__ == "__main__":
#def hashMallWifi():
	
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
	f = open("../data/dictionary/m_623_wifi.pkl",'rb')
	sidKey = pickle.load(f)
	print(sidKey)
	f.close()
	"""