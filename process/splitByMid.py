#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-18 20:10:57
# @Author  : WordZzzz (wordzzzz@foxmail.com)
# @Link    : http://blog.csdn.net/u011475210
# @Version : $Id$

import csv
import os
import time

midDictionary = {}

def writeByMid(mid, words):
	file_name = mid + ".txt"
	os.chdir('../data/mid/')

	if not midDictionary.has_key(mid):
		midDictionary[mid] = True
		f = open(file_name, 'a')
		write = csv.writer(f)
		write.writerow(['shop_id', 'catagory_id', 'longitude', 'latitude', 'price'])
		write.writerow(words)
		f.close()
	else:
		f = open(file_name, 'a')
		write = csv.writer(f)
		write.writerow(words)
		f.close()
	os.chdir('../../process/')

def splitByMid():
	os.mkdir('../data/mid')
	f = open("../data/ccf_first_round_shop_info.csv")
	rows = csv.reader(f)
	rows.next()
	for row in rows:
		mid = row[-1]
		words = row[0:-1]
		writeByMid(mid, words)