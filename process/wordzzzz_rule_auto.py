#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-13 21:05:02
# @Author  : WordZzzz (wordzzzz@foxmail.com)
# @Link    : http://blog.csdn.net/u011475210
# @Version : $Id$

import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn import cross_validation, metrics, preprocessing   #Additional scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid search

#加载数据
path = '../data/'
df = pd.read_csv(path + u'ccf_first_round_user_shop_behavior.csv')
shop = pd.read_csv(path + u'ccf_first_round_shop_info.csv')
test = pd.read_csv(path + u'evaluation_public.csv')
df = pd.merge(df,shop[['shop_id','mall_id']], how = 'left', on = 'shop_id')
df['time_stamp']=pd.to_datetime(df['time_stamp'])
train = pd.concat([df,test])
mall_list = list(set(list(shop.mall_id)))
result = pd.DataFrame()
report = pd.DataFrame()
df_report = {}
df_param = {}

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

def modelfit1(dtrain, feature):
	#网格搜索筛选最优参数
	print("Begin GridSearchCV1")
	global n_estimators, max_depth, min_child_weight, subsample, colsample_bytree
	xgb1 = XGBClassifier( learning_rate = 0.1,
						  n_estimators = n_estimators,
						  max_depth = max_depth,
						  min_child_weight = min_child_weight,
						  subsample = subsample,
						  colsample_bytree = colsample_bytree,
						  objective = 'multi:softmax',
						  scale_pos_weight = 1,
						  seed = 0)
	param_test1 = {
	'max_depth':[8, 9],
	'min_child_weight':[1, 2]
	}
	gsearch1 = GridSearchCV(estimator = xgb1, 
							param_grid = param_test1,
							n_jobs = 1,
							iid = False,
							cv = 5)
	gsearch1.fit(dtrain[feature], dtrain['label'])
	gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_

	max_depth = gsearch1.best_params_['max_depth']
	print(max_depth)
	min_child_weight = gsearch1.best_params_['min_child_weight']
	print(min_child_weight)
	print("End GridSearchCV1")

def modelfit2(dtrain, feature):
	#网格搜索筛选最优参数
	print("Begin GridSearchCV2")
	global n_estimators, max_depth, min_child_weight, subsample, colsample_bytree
	xgb2 = XGBClassifier( learning_rate = 0.1,
						  n_estimators = n_estimators,
						  max_depth = max_depth,
						  min_child_weight = min_child_weight,
						  subsample = subsample,
						  colsample_bytree = colsample_bytree,
						  objective = 'multi:softmax',
						  scale_pos_weight = 1,
						  seed = 0)
	param_test2 = {
	'subsample':[0.6, 0.7, 0.8, 0.9]
	}
	gsearch2 = GridSearchCV(estimator = xgb2, 
							param_grid = param_test2,
							n_jobs = 1,
							iid = False,
							cv = 5)
	gsearch2.fit(dtrain[feature],dtrain['label'])
	gsearch2.grid_scores_, gsearch2.best_params_, gsearch2.best_score_

	subsample = gsearch2.best_params_['subsample']
	print(subsample)
	print("Begin GridSearchCV2")

#遍历所有的商场
for mall in mall_list:
	mall_count += 1
	print("mall_id: %s, The current percentage is %f." % (mall, mall_count / mall_num))

	#加载数据
	train1 = train[train.mall_id == mall].reset_index(drop = True)
	l = []
	wifi_dict = {}
	#对每个wifi计数
	for index,row in train1.iterrows():
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
	train1 = pd.concat([train1,pd.DataFrame(m)], axis = 1)

	#提取训练数据集和测试数据集
	df_train = train1[train1.shop_id.notnull()]
	df_test = train1[train1.shop_id.isnull()]
	#制作标签
	lbl = preprocessing.LabelEncoder()
	lbl.fit(list(df_train['shop_id'].values))
	df_train['label'] = lbl.transform(list(df_train['shop_id'].values))
	#类别个数
	num_class = df_train['label'].max()+1
	#特征
	feature = [x for x in train1.columns if x not in ['user_id',
													  'row_id',
													  'label',
													  'shop_id',
													  'time_stamp',
													  'mall_id',
													  'wifi_infos']]
	
	#自动调参第一步，确定最优评估器个数。
	xgb0 = XGBClassifier( learning_rate = 0.1,
						  n_estimators = n_estimators,
						  max_depth = max_depth,
						  min_child_weight = min_child_weight,
						  subsample = subsample,
						  colsample_bytree = colsample_bytree,
						  objective = 'multi:softmax',
						  scale_pos_weight = 1,
						  seed = 0)

	xgb_param = xgb0.get_xgb_params()
	xgb_param['num_class'] = num_class
	xgtrain = xgb.DMatrix(df_train[feature], label = df_train['label'])
	cvresult = xgb.cv(xgb_param,
					  xgtrain,
					  num_boost_round = xgb0.get_params()['n_estimators'],
					  nfold = 5,
					  metrics = 'merror',
					  early_stopping_rounds = 20,
					  verbose_eval = True)
	n_estimators = cvresult.shape[0]
	print("n_estimators : %s" % n_estimators)

	#自动调参第二步，确定最优max_depth，min_child_weight。
	modelfit1(df_train, feature)
	#自动调参第三步，确定最优subsample，colsample_bytree。
	modelfit2(df_train, feature)

	##自动调参第四步，使用所有最优参数
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
	df_param[mall] = [max_depth, min_child_weight, subsample]
	df_test['label'] = modelfit(mall, xgb3, df_train, df_test, feature, num_class)
	df_test['shop_id'] = df_test['label'].apply(lambda x:lbl.inverse_transform(int(x)))
	r = df_test[['row_id', 'shop_id']]
	result = pd.concat([result,r])
	result['row_id'] = result['row_id'].astype('int')
	result.to_csv(path + 'xgbsklearn_rule_test.csv', index = False)
	print("End modelfit")

	df_param = pd.DataFrame.from_records([df_param])
	df_param.to_csv(path + 'xgbsklearn_rule_param.csv', index = False)

	report = pd.DataFrame.from_records([df_report])
	report.to_csv(path + 'xgbsklearn_rule_test_train.csv', index = False)
