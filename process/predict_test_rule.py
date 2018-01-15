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

def predictTest():
	errorCount = 0
	os.chdir('../data')
#	f = open("evaluation_public.csv", 'r')
	f = open("evaluation_public.csv", 'r')
	rows = csv.reader(f)
	next(rows)
	#scan testset
	for row in rows:
		predict = {}
		wifiInfoSort = []
		wifiInfo = {}
		rid = row[0]
		if not rid in predict:
			predict[rid] = {}
		mid = row[2]
		fr = open("dictionary/"+mid+"_wifi.pkl", 'rb')
		sidKey = pickle.load(fr)
		#split wifi_info
		wifi = row[-1].split(';')
		#get the number of wifi
		wifiNum = len(wifi)
		for num in range(wifiNum):
			wifiInfo[wifi[num].split('|')[0]] = wifi[num].split('|')[1]
		wifiInfoSort = sorted(wifiInfo.items(), key=operator.itemgetter(1), reverse=False)
		
		for key in sidKey:
			for num in range(len(wifiInfoSort)):
				try:
					if wifiInfoSort[num][0] in sidKey[key] and sidKey[key][wifiInfoSort[num][0]][0] > 1 and sidKey[key][wifiInfoSort[num][0]][1] > -80:
#						print("wifiinfo: "+wifiInfoSort[num][0])
#						print(sidKey[key][wifiInfoSort[num][0]][0])
						if not key in predict[rid]:
#								predict[rid][key] = sidKey[key][wifiInfoSort[num][0]][2] / abs(int(wifiInfoSort[num][1]) - sidKey[key][wifiInfoSort[num][0]][1]) / (num + 1)
							predict[rid][key] = sidKey[key][wifiInfoSort[num][0]][2] / (num + 1)**2
						else:
#								predict[rid][key] += sidKey[key][wifiInfoSort[num][0]][2] / abs(int(wifiInfoSort[num][1]) - sidKey[key][wifiInfoSort[num][0]][1]) / (num + 1)
							predict[rid][key] += sidKey[key][wifiInfoSort[num][0]][2] / (num + 1)**2
				except:
					print("rid = %s, num = %s, key = %s" % (rid, num, key))
		
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
	print("number of result :%d" % (len(result)))
	print("errorCount : %d" % (errorCount))

if __name__ == "__main__":
	predictTest()