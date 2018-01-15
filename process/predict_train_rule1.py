#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-19 20:15:39
# @Author  : WordZzzz (wordzzzz@foxmail.com)
# @Link    : http://blog.csdn.net/u011475210
# @Version : $Id$

import os
import operator
import csv
import pickle
from random import choice

result = {}
resultError = {}

def rules(rid, key, wifiInfoSort, sidKey, predict, index):
	try:
		if wifiInfoSort[index][0] in sidKey[key]:
#					print("wifiinfo: "+wifiInfoSort[index][0])
#					print(sidKey[key][wifiInfoSort[index][0]][0])
			if not key in predict[rid]:
#							predict[rid][key] = sidKey[key][wifiInfoSort[index][0]][2] / abs(int(wifiInfoSort[index][1]) - sidKey[key][wifiInfoSort[index][0]][1]) / (index + 1)
				predict[rid][key] = sidKey[key][wifiInfoSort[index][0]][0] / abs(int(wifiInfoSort[index][1]) - sidKey[key][wifiInfoSort[index][0]][1]) / (index + 1)**2
			else:
#							predict[rid][key] += sidKey[key][wifiInfoSort[index][0]][2] / abs(int(wifiInfoSort[index][1]) - sidKey[key][wifiInfoSort[index][0]][1]) / (index + 1)
				predict[rid][key] += sidKey[key][wifiInfoSort[index][0]][0] / abs(int(wifiInfoSort[index][1]) - sidKey[key][wifiInfoSort[index][0]][1]) / (index + 1)**2
	except:
		if index < len(wifiInfoSort):
			rules(rid, key, wifiInfoSort, sidKey, predict, index+1)
		else:
			pass

def predictTrain(fileName, mallId):
	errorCount = 0
	errorTrainCount = 0
	trainCount = 0
#	os.chdir('../data')
#	f = open("ccf_first_round_shop_info_combine.csv", 'r')
	f = open(fileName, 'r')
	rows = csv.reader(f)
	next(rows)
	for row in rows:
		index = 0
		trainCount +=1
#		print(row)
		predict = {}
		wifiInfoSort = []
		wifiInfo = {}
		rid = row[0]
		if not rid in predict:
			predict[rid] = {}
		mid = "m_"+mallId
#		print(mid)
		fr = open("../data/dictionary_top8/"+mid+"_wifi.pkl", 'rb')
		sidKey = pickle.load(fr)
		#split wifi_info
		wifi = row[-1].split(';')
		#get the number of wifi
		wifiNum = len(wifi)
		for num in range(wifiNum):
			wifiInfo[wifi[num].split('|')[0]] = wifi[num].split('|')[1]
		wifiInfoSort = sorted(wifiInfo.items(), key=operator.itemgetter(1), reverse=False)
#		print(wifiInfoSort)
		for key in sidKey:
			rules(rid, key, wifiInfoSort, sidKey, predict, index)
		try:
			result[rid] = sorted(predict[rid].items(), key=operator.itemgetter(1), reverse=True)[0][0]
		except:
			print("rid = %s" % (rid))
			result[rid] = choice(list(sidKey.keys()))
			errorCount += 1
#		print(result)
#		print(predict)
		if result[rid] != row[1]:
#			print("aaa:" + result[rid],row[1],predict[rid])
			errorTrainCount += 1
		fr.close()
	f.close()
	"""
	fw = open("../data/result_train_rule1/"+mid+"result_train.csv", 'w')
	write = csv.writer(fw)
	write.writerow(['row_id', 'shop_id'])
	write.writerows(result.items())
	fw.close()
	"""
	print("errorCount : %d" % (errorCount))
	print("errorTrainCount : %d" % (errorTrainCount))
	print("number of result :%d" % (trainCount))
	print("errorCount : %f" % (errorCount/trainCount))
	print("errorTrainCount : %f" % (errorTrainCount/trainCount))
	
	resultError[mid] = errorTrainCount/trainCount

if __name__ == "__main__":
#	predictTrain("../data/msid/m_615_user_behavior.txt", "615")
#	predictTrain("../data/msid/m_622_user_behavior.txt", "622")
	predictTrain("../data/msid/m_7800_user_behavior.txt", "7800")
	"""
	directory = "../data/msid/"
	dirList = os.listdir(directory)
	dirList.sort()

	for eachtxt in dirList:
		fileName = directory+eachtxt
		mallId = eachtxt.split('_')[1]
		print("test from m_%s" % mallId)
		predictTrain(fileName, mallId)
		print("test down m_%s" % mallId)
		
	fw = open("../data/dictionary/result_train.csv", 'w')
	write = csv.writer(fw)
	write.writerow(['mall_id', 'error_rate'])
	write.writerows(resultError.items())
	fw.close()
	"""