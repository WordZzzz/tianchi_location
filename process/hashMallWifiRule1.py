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
		#split wifi_info
		wifi = row[-1].split(';')
		#get the number of wifi
		wifiNum = len(wifi)
		for num in range(wifiNum):
			wifiInfo[wifi[num].split('|')[0]] = wifi[num].split('|')[1]
		wifiInfoSort = sorted(wifiInfo.items(), key=operator.itemgetter(1), reverse=False)

		wifiName = wifi[0].split('|')[0]
		if not wifiName in wifiHash:
			wifiHash[wifiName] = {}
		if not sid in wifiHash[wifiName]:
			wifiHash[wifiName][sid] = 0
		wifiHash[wifiName][sid] += 1
	
	f = open("../data/dictionary_rule1/m_"+mallId+"_wifi.pkl",'wb')
	pickle.dump(wifiHash, f, -1)
	f.close()

def writeMallWifiTest():
	wifiHash = {} #存放最终结果
	#open file
	f = open('test.txt','r')
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
		#split wifi_info
		wifi = row[-1].split(';')
		#get the number of wifi
		wifiNum = len(wifi)
		for num in range(wifiNum):
			wifiInfo[wifi[num].split('|')[0]] = wifi[num].split('|')[1]
		wifiInfoSort = sorted(wifiInfo.items(), key=operator.itemgetter(1), reverse=False)

		wifiName = wifi[0].split('|')[0]
		if not wifiName in wifiHash:
			wifiHash[wifiName] = {}
		if not sid in wifiHash[wifiName]:
			wifiHash[wifiName][sid] = 0
		wifiHash[wifiName][sid] += 1
		print(wifiHash)

def pklCheck():
	f = open("../data/dictionary_rule1/m_1175_wifi.pkl",'rb')
	sidKey = pickle.load(f)
	print(sidKey)
#	for sid in sidKey:
#		print(sorted(sidKey[sid].items(), key=operator.itemgetter(1), reverse=True))
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