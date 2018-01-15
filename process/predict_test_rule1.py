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

def rules(rid, key, wifiInfoSort, sidKey, predict, index):
	try:
		if sidKey[key][wifiInfoSort[index][0]][0] > 1 and sidKey[key][wifiInfoSort[index][0]][1] > -80:
#					print("wifiinfo: "+wifiInfoSort[index][0])
#					print(sidKey[key][wifiInfoSort[index][0]][0])
			if not key in predict[rid]:
#							predict[rid][key] = sidKey[key][wifiInfoSort[index][0]][2] / abs(int(wifiInfoSort[index][1]) - sidKey[key][wifiInfoSort[index][0]][1]) / (index + 1)
				predict[rid][key] = sidKey[key][wifiInfoSort[index][0]][0] / (index + 1)**2
			else:
#							predict[rid][key] += sidKey[key][wifiInfoSort[index][0]][2] / abs(int(wifiInfoSort[index][1]) - sidKey[key][wifiInfoSort[index][0]][1]) / (index + 1)
				predict[rid][key] += sidKey[key][wifiInfoSort[index][0]][0] / (index + 1)**2
	except:
		if index < 5:
			rules(rid, key, wifiInfoSort, sidKey, predict, index+1)
		else:
			pass

def predictTest():
	errorCount = 0
	trainCount = 0
	os.chdir('../data')
#	os.chdir('../data')
	f = open("evaluation_public.csv", 'r')
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
		mid = row[2]
#		print(mid)
		fr = open("../data/dictionary/"+mid+"_wifi.pkl", 'rb')
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
		fr.close()
	f.close()
	
	fw = open("result.csv", 'w')
	write = csv.writer(fw)
	write.writerow(['row_id', 'shop_id'])
	write.writerows(result.items())
	fw.close()
	
	print("errorCount : %d" % (errorCount))
	print("number of result :%d" % (trainCount))
	print("errorCount : %f" % (errorCount/trainCount))

if __name__ == "__main__":
	predictTest()