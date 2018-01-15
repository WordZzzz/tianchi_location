#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-16 09:26:44
# @Author  : WordZzzz (wordzzzz@foxmail.com)
# @Link    : http://blog.csdn.net/u011475210
# @Version : $Id$

import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn import cross_validation, metrics, preprocessing   #Additional scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid search
import re

#加载数据
path = '../data/'
df = pd.read_csv(path + u'ccf_first_round_user_shop_behavior.csv')
shop = pd.read_csv(path + u'ccf_first_round_shop_info.csv')
test = pd.read_csv(path + u'evaluation_public.csv')
df = pd.merge(df,shop[['shop_id','mall_id']], how = 'left', on = 'shop_id')
train = pd.concat([df,test])
train['time_stamp'] = pd.to_datetime(train['time_stamp'])
train['week_date'] = train['time_stamp'].dt.dayofweek
mall_list = list(set(list(shop.mall_id)))
result = pd.DataFrame()
report = pd.DataFrame()
df_report = {}

mall_num = 97
mall_count = 0
n_estimators = 500
max_depth = 9
min_child_weight = 1
subsample = 0.8
colsample_bytree = 0.5

def modelfit(mall, alg, dtrain, dtest, feature, num_class, useTrainCV = True, cv_folds = 5, early_stopping_rounds = 20):
	"""
	function：交叉验证（Cross Validation）

	parameter：mall：商场ID
			   alg：参数
			   dtrain：训练数据
			   dtest：测试数据集
			   feature：特征
			   num_class：分类个数
			   useTrainCV：是否使用CV
			   cv_folds：训练、测试占比
			   early_stopping_rounds：early_stopping次数
	
	return：dtest_predictions：预测结果
	"""

	#默认使用交叉验证
	if useTrainCV:
		xgb_param = alg.get_xgb_params()
		xgb_param['num_class'] = num_class
		xgtrain = xgb.DMatrix(dtrain[feature], label=dtrain['label'])
		xgtest = xgb.DMatrix(dtest[feature])
		cvresult = xgb.cv(xgb_param,
						  xgtrain,
						  num_boost_round = alg.get_params()['n_estimators'],
						  nfold = cv_folds,
						  metrics = 'merror',
						  early_stopping_rounds = early_stopping_rounds,
						  verbose_eval = True)
		alg.set_params(n_estimators = cvresult.shape[0])
		print("n_estimators : %s" % cvresult.shape[0])
	  
	#在数据上拟合算法
	alg.fit(dtrain[feature], dtrain['label'], eval_metric = 'merror')
	
	#预测
	dtrain_predictions = alg.predict(dtrain[feature])
	dtest_predictions = alg.predict(dtest[feature])

	#打印结果
	print ("\nModel Report")
	df_report[mall] = metrics.accuracy_score(dtrain['label'].values, dtrain_predictions)
	print ("Accuracy : %.4g" % df_report[mall])
	#返回预测结果
	return dtest_predictions

#遍历所有的商场
for mall in mall_list:
	mall_count += 1
	print("mall_id: %s, The current percentage >>>>>>%f>>>>>>" % (mall, mall_count / mall_num))
	#加载数据
	train1 = train[train.mall_id == mall].reset_index(drop = True)
	train_weekend = train1[train1.week_date >= 5].reset_index(drop = True)
	train_weekday = train1[train1.week_date < 5].reset_index(drop = True)

	###周末开始
	l = []
	wifi_dict = {}
	#对每个wifi计数
	for index,row in train_weekend.iterrows():
		r = {}
		wifi_list = [wifi.split('|') for wifi in row['wifi_infos'].split(';')]
		for i in wifi_list:
			r[i[0]] = int(i[1])
			if i[0] not in wifi_dict:
				wifi_dict[i[0]] = 1
			else:
				wifi_dict[i[0]] += 1
		l.append(r)
	#如果wifi对应统计次数只有1个就记录下来
	delate_wifi = []
	for i in wifi_dict:
		if wifi_dict[i] < 2:
			delate_wifi.append(i)
	#数据copy，剔除delate_wifi中记录的wifi
	m = []
	for row in l:
		new = {}
		for n in row.keys():
			if n not in delate_wifi:
				new[n] = row[n]
		m.append(new)
	train_weekend = pd.concat([train_weekend,pd.DataFrame(m)], axis = 1)

	#提取训练数据集和测试数据集
	df_train_we = train_weekend[train_weekend.shop_id.notnull()]
	df_test_we = train_weekend[train_weekend.shop_id.isnull()]
	#制作标签
	lbl = preprocessing.LabelEncoder()
	lbl.fit(list(df_train_we['shop_id'].values))
	df_train_we['label'] = lbl.transform(list(df_train_we['shop_id'].values))
	#类别个数
	num_class = df_train_we['label'].max()+1
	#特征
	feature = [x for x in train_weekend.columns if x not in ['user_id',
													  'row_id',
													  'week_date',
													  'label',
													  'shop_id',
													  'time_stamp',
													  'mall_id',
													  'wifi_infos']]

	#初始化参数
	xgb3 = XGBClassifier(learning_rate = 0.1,
						  n_estimators = 500,
						  max_depth = max_depth,
						  min_child_weight = min_child_weight,
						  subsample = subsample,
						  colsample_bytree = colsample_bytree,
						  objective = 'multi:softmax',
						  scale_pos_weight = 1,
						  seed = 0)
	print(xgb3)
	print("Begin modelfit")
	df_test_we['label'] = modelfit(mall, xgb3, df_train_we, df_test_we, feature, num_class)
	df_test_we['shop_id'] = df_test_we['label'].apply(lambda x:lbl.inverse_transform(int(x)))
	r = df_test_we[['row_id', 'shop_id']]
	###周末结束
	result = pd.concat([result,r])
	result['row_id'] = result['row_id'].astype('int')
	result.to_csv(path + 'xgbsklearn_rule_week.csv', index = False)

	###工作日开始
	l = []
	wifi_dict = {}
	#对每个wifi计数
	for index,row in train_weekday.iterrows():
		r = {}
		wifi_list = [wifi.split('|') for wifi in row['wifi_infos'].split(';')]
		for i in wifi_list:
			r[i[0]] = int(i[1])
			if i[0] not in wifi_dict:
				wifi_dict[i[0]] = 1
			else:
				wifi_dict[i[0]] += 1
		l.append(r)
	#如果wifi对应统计次数只有1个就记录下来
	delate_wifi = []
	for i in wifi_dict:
		if wifi_dict[i] < 2:
			delate_wifi.append(i)
	#数据copy，剔除delate_wifi中记录的wifi
	m = []
	for row in l:
		new = {}
		for n in row.keys():
			if n not in delate_wifi:
				new[n] = row[n]
		m.append(new)
	train_weekday = pd.concat([train_weekday,pd.DataFrame(m)], axis = 1)

	#提取训练数据集和测试数据集
	df_train_wd = train_weekday[train_weekday.shop_id.notnull()]
	df_test_wd = train_weekday[train_weekday.shop_id.isnull()]
	#制作标签
	lbl = preprocessing.LabelEncoder()
	lbl.fit(list(df_train_wd['shop_id'].values))
	df_train_wd['label'] = lbl.transform(list(df_train_wd['shop_id'].values))
	#类别个数
	num_class = df_train_wd['label'].max()+1
	#特征
	feature = [x for x in train_weekday.columns if x not in ['user_id',
													  'row_id',
													  'week_date'
													  'label',
													  'shop_id',
													  'time_stamp',
													  'mall_id',
													  'wifi_infos']]
	
	#初始化参数
	xgb3 = XGBClassifier(learning_rate = 0.1,
						  n_estimators = 500,
						  max_depth = max_depth,
						  min_child_weight = min_child_weight,
						  subsample = subsample,
						  colsample_bytree = colsample_bytree,
						  objective = 'multi:softmax',
						  scale_pos_weight = 1,
						  seed = 0)
	print(xgb3)
	print("Begin modelfit")
	df_test_wd['label'] = modelfit(mall, xgb3, df_train_wd, df_test_wd, feature, num_class)
	df_test_wd['shop_id'] = df_test_wd['label'].apply(lambda x:lbl.inverse_transform(int(x)))
	r = df_test_wd[['row_id', 'shop_id']]
	###工作日结束
	result = pd.concat([result,r])
	result['row_id'] = result['row_id'].astype('int')
	result.to_csv(path + 'xgbsklearn_rule_week1.csv', index = False)
	print("End modelfit")

report = pd.DataFrame.from_records([df_report])
report.to_csv(path + 'xgbsklearn_rule_week1_train.csv', index = False)