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
import numpy as np
from random import choice
from sklearn.neighbors import KNeighborsClassifier

result = {}
resultError = {}

def cos(vector1,vector2):
	dot_product = 0.0
	normA = 0.0
	normB = 0.0
	for a,b in zip(vector1,vector2):
		dot_product += a*b
		normA += a**2
		normB += b**2
	if normA == 0.0 or normB==0.0:
		return None
	else:
		return dot_product / ((normA*normB)**0.5)

def loadDataSet(mid):
	wifiList = []
	wifiListSet = []
	featureSet = []
	classSet = []
	fr = open("../data/dictionary_top8/"+mid+"_wifi.pkl", 'rb')
	sidKey = pickle.load(fr)
	#split wifi_info
	for sid in sidKey:
		wifiList.extend(list(sidKey[sid].keys()))
	wifiListSet = list(set(wifiList))

	for sid in sidKey:
		feature = [0 for i in range(len(wifiListSet))]
		for wifiId in sidKey[sid]:
			if wifiId in wifiListSet:
				feature[wifiListSet.index(wifiId)] = sidKey[sid][wifiId][1]
		classSet.append(sid)
		featureSet.append(feature)
	fr.close()
#	print(wifiListSet, np.shape(wifiListSet), featureSet, np.shape(featureSet), classSet, np.shape(classSet))
	return wifiListSet, featureSet, classSet

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
		neigh = KNeighborsClassifier(n_neighbors=1, metric='canberra')
		trainSet = []
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
		wifiListSet, featureSet, classSet = loadDataSet(mid)
		#split wifi_info
		wifi = row[-1].split(';')
		#get the number of wifi
		wifiNum = len(wifi)
		for num in range(wifiNum):
			wifiInfo[wifi[num].split('|')[0]] = int(wifi[num].split('|')[1])

		feature = [0 for i in range(len(wifiListSet))]
		for wifiId in wifiInfo:
			if wifiId in wifiListSet:
				feature[wifiListSet.index(wifiId)] = wifiInfo[wifiId]

#		print(feature)
		neigh.fit(featureSet, classSet)
		print(neigh.predict([feature]))
		try:
			result[rid] = neigh.predict([feature])
		except:
			print("rid = %s" % (rid))
			result[rid] = choice(classSet)
			errorCount += 1
#		print(result)
#		print(predict)
		if result[rid] != row[1]:
			print(result[rid],row[1])
			errorTrainCount += 1
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
#	loadDataSet("m_2058")
#	predictTrain("../data/msid/m_615_user_behavior.txt", "615")
#	predictTrain("../data/msid/m_622_user_behavior.txt", "622")b
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