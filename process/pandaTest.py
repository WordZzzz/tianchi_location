#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-06 20:13:57
# @Author  : WordZzzz (wordzzzz@foxmail.com)
# @Link    : http://blog.csdn.net/u011475210
# @Version : $Id$

import pandas as pd
import numpy as np
from sklearn import preprocessing

path = '../data/'
usb = pd.read_csv(path + u'ccf_first_round_user_shop_behavior.csv')
si = pd.read_csv(path + u'ccf_first_round_shop_info.csv')

us = pd.merge(usb, si[['shop_id', 'mall_id', 'category_id', 'price']], how = 'left', on = 'shop_id')
us['time_stamp'] = pd.to_datetime(us['time_stamp'])
us.to_csv(path+'us.csv', index = False)

mall_list = list(set(list(us.mall_id)))
for mall in mall_list:
	print("begin with :" + mall)
	data = us[us.mall_id == mall].reset_index(drop = True)
	rows = []
	wifi_dict = {}
	for index, row in data.iterrows():
		cur = {}
		wifi_list = [wifi.split('|') for wifi in row['wifi_infos'].split(';')]
		for i in wifi_list:
			cur[i[0]] = int(i[1])
			if i[0] not in wifi_dict:
				wifi_dict[i[0]] = 1
			else:
				wifi_dict[i[0]] += 1
		rows.append(cur)

	delete_wifi = []
	for i in wifi_dict:
		if wifi_dict[i] < 2:
			delete_wifi.append(i)

	m = []
	for row in rows:
		cur = {}
		for n in row.keys():
			if n not in delete_wifi:
				cur[n] = row[n]
		m.append(cur)

	data = pd.concat([data, pd.DataFrame(m)], axis=1)
	data.to_csv(path+'us/'+mall+'.csv', index = False)