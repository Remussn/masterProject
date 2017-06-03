# 2-27-2017
# Propagation Kernel
# All functions related to propagation kernel
import matlab.engine
import numpy
import random
import math
from sklearn import svm
from sklearn.metrics import accuracy_score
from util import *

def propKernel(path_to_dataset, dataset_name, label_transform_model):
	print 'engine starts'
	eng = matlab.engine.start_matlab()
	K 	= eng.PropagationKernel(path_to_dataset, dataset_name, label_transform_model)
	print 'engine ends'
	eng.quit()
	return numpy.array(K)
	
# def getStats(path_to_dataset, dataset_name):
# 	pass

	# input: a ordered list of labels & K (matrix) & blocks(test data indices)
	# return: Ytri, Ktri, Ytst, Ktst
def splitKernel(Y, K, block):
	index_Y = range(len(Y))
	# test
	Ytst_index = block
	Ytst = Y[numpy.array(Ytst_index)]
	# train
	Ytri_index = [ind for ind in index_Y if ind not in Ytst_index]
	Ytri = Y[numpy.array(Ytri_index)]
	# get Ktri
	K_temp = K[:,Ytri_index] # take off all Ytri columns
	Ktri = K_temp[Ytri_index,:] # take off all Ytri raws
	# get Ktst
	Ktst = K_temp[Ytst_index,:]
	return Ytri, Ktri, Ytst, Ktst

	# X should be numpy array
def splitData(Y, X, block):
	index_Y = range(len(Y))
	# index
	Ytst_index = block
	Ytri_index = [ind for ind in index_Y if ind not in Ytst_index]
	# training
	Xtri = X[Ytri_index,:]
	Ytri = Y[numpy.array(Ytri_index)]
	# testing 
	Xtst = X[Ytst_index]
	Ytst = Y[numpy.array(Ytst_index)]

	return Ytri, Xtri, Ytst, Xtst

	# L is list of labels
def generateFolds(L, fold, seed):
	l = len(L)
	Y = range(l)
	#-- get folds --#
	blocks = []  # list of indices of test data
	ind_h  = 0 	 # head fence
	ind_t  = 0    # tail fence
	random.seed(seed)
	random.shuffle(Y)
	for i in xrange(fold):
		ind_t = ind_h + l/fold
		try:
			block = Y[ind_h:ind_t]
		except:
			block = Y[ind_h:end]
		blocks.append(block)
		ind_h = ind_t
	return blocks

def crossValidate(Y, K, kernel_type, seeds, fold = 10, times = 10):
	#-- select kernel --#
	clf 		= svm.SVC(kernel = kernel_type)
	accus_total = []
	for i in xrange(times):
		# generate folds
		accus_each_time = []
		seed = seeds[i]
		blocks = generateFolds(Y, fold, seed)
		for block in blocks:
			if kernel_type == 'precomputed':
				Ytri, Ktri, Ytst, Ktst = splitKernel(Y, K, block)
			else:
				Ytri, Ktri, Ytst, Ktst = splitData(Y, K, block)
			clf.fit(Ktri,Ytri)
			Ypre = clf.predict(Ktst)
			accu = accuracy_score(Ytst,Ypre)
			accus_total.append(accu)
			accus_each_time.append(accu)

		avg_accu_each = sum(accus_each_time) / len(accus_each_time)
		print '{}th {}-fold cross validation: '.format(i+1,fold) + str(avg_accu_each)

	avg_accu_total = sum(accus_total) / len(accus_total)
	print '{}*{} fold cross validation avg_accu: '.format(times, fold) + str(avg_accu_total)






