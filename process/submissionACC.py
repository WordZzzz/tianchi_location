#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-19 09:44:56
# @Author  : WordZzzz (wordzzzz@foxmail.com)
# @Link    : http://blog.csdn.net/u011475210
# @Version : $Id$

import pandas as pd
import operator

count = 0

if __name__ == '__main__':
	ac_1 = pd.read_csv(u'xgbsklearn_rule1_85_train.csv').to_dict()
	ac_2 = pd.read_csv(u'xgbsklearn_rule1_95_train.csv').to_dict()
	ac_3 = pd.read_csv(u'xgbsklearn_rule1_75_train.csv').to_dict()

	acc_list = {}
	acc = {}

	for key in ac_1:
		acc_list[key] = [ac_1[key][0], ac_2[key][0], ac_3[key][0]]
#		print(ac_1[key], ac_2[key], ac_3[key], acc_list , acc_list[key].index(max(acc_list[key])))
#		acc_list[key].index(max(acc_list[key]))
	print("here1")
	test = pd.read_csv(u'evaluation_public.csv')
	
	for index,row in test.iterrows():
		if row.mall_id in acc_list.keys():
			acc[row.row_id] = acc_list[row.mall_id].index(max(acc_list[row.mall_id]))
#			print(acc)
	print("here2")
	df_1 = pd.read_csv(u'xgbsklearn_rule1_85_B9094.csv')
	df_2 = pd.read_csv(u'xgbsklearn_rule1_95_B9094.csv')
	df_3 = pd.read_csv(u'xgbsklearn_rule1_75_B9093.csv')

	result = {}
	final = {}

	for df_1_line in df_1.values:
		result[str(df_1_line[0])] = [df_1_line[1]]
	for df_2_line in df_2.values:
		result[str(df_2_line[0])].append(df_2_line[1])
	for df_3_line in df_3.values:
		result[str(df_3_line[0])].append(df_3_line[1])
	print("here3")
	for key, value in result.items():
#		print(key, value[acc[key]])
		try:
			final[key] = value[acc[key]]
			print(final[key])
		except:
			final[key] = 'fuck'
			count += 1
	print("here4")
	for key, value in final.items():
		if value == 'fuck':
			for each in df_1.values:
				if each[0] == int(key):
					final[key] = each[1]
	print("here5")
	with open('submissionB_acc1.txt', 'a') as f:
		f.write('row_id,shop_id\n')
		for key, value in final.items():
			f.write(key)
			f.write(',')
			f.write(value)
			f.write('\n')
