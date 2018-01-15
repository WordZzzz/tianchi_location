#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-21 16:31:45
# @Author  : WordZzzz (wordzzzz@foxmail.com)
# @Link    : http://blog.csdn.net/u011475210
# @Version : $Id$

import csv
import pymysql

def printVersion():
	# 打开数据库连接
	db = pymysql.connect("localhost","root","092904","tianchi_location" )

	# 使用 cursor() 方法创建一个游标对象 cursor
	cursor = db.cursor()

	# 使用 execute()  方法执行 SQL 查询 
	cursor.execute("SELECT VERSION()")

	# 使用 fetchone() 方法获取单条数据.
	data = cursor.fetchone()

	print ("Database version : %s " % data)

	# 关闭数据库连接
	db.close()

def createList():
	# 打开数据库连接
	db = pymysql.connect("localhost","root","092904","tianchi_location" )
	
	# 使用 cursor() 方法创建一个游标对象 cursor
	cursor = db.cursor()
	
	# 使用 execute() 方法执行 SQL，如果表存在则删除
	cursor.execute("DROP TABLE IF EXISTS COMBINE")
	
	# 使用预处理语句创建表
	sql = """CREATE TABLE COMBINE (
			 USER_ID  CHAR(20),
			 MALL_ID  CHAR(20),
			 SHOP_ID  CHAR(20),
			 WIFI_INFO  CHAR(100))"""
	
	cursor.execute(sql)
	
	# 关闭数据库连接
	db.close()