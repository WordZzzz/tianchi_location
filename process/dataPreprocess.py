#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-18 20:03:00
# @Author  : WordZzzz (wordzzzz@foxmail.com)
# @Link    : http://blog.csdn.net/u011475210
# @Version : $Id$

import time
from splitByMid import splitByMid

if __name__ == "__main__":
	"""
	Function：	主函数

	Iuput：		两个数据集

	Output：	数据预处理之后另存为的文件
	"""
	print("->->->->->->->->->->->->->->->")
	t0 = time.time()
	#运行splitByDate.py，在data目录下生成date文件夹以及文件
	splitByMid()
	t1 = time.time()
	print("It takes %f s to split by mid,generate 'data/mid/*.csv'" %(t1-t0))
	print("->->->->->->->->->->->->->->->")
