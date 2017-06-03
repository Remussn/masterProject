# 2017-4-21
# Yu Sun

from representations import *
from propagationKernel import *
import random
import re
import os
import numpy

#### Reuters ####
# dataset_name = 'r8_reuters_small'

#### Amazon ####
# dataset_name = 'rate_reviews_Amazon_Instant_Video_small'
# dataset_name = 'rate_reviews_Amazon_Musical_Instruments_small'
# dataset_name = 'rate_reviews_Amazon_Merged_MusicalInstruments&InstantVideo'


##### Wikipeida #####
# dataset_name = '5_classes'
# dataset_name = '5_classes_small'
# dataset_name = '10_classes_small'
# dataset_name = '15_classes_small'
# dataset_name = '20_classes_small'
# dataset_name = 'eduIns_horRdr'
dataset_name = 'jane_test_type'

# **********  Fixed  **********
punc_tf = True
stpw_tf = True
vec_win_size = 10
vec_model = 0

# ********** Hyperparameters **********
graph_win_size = 5
vec_dim = 10
node_attr_type = 'word2vec' # word2vec
bow_model = 'tfidf'
kernel_type = 'linear' # rbf

################ Representations ################

#-- graph --#
g = graph('{}.txt'.format(dataset_name), dataset_name, 
						punc = punc_tf, stpw = stpw_tf)
K_g1, Y_g1 = g.toGraph(graph_win_size, 		# vec_win_size
					   node_attr_type, vec_dim, 10, vec_model, 
					   'naive', 'diffusion',
					   pos_model = 1.0, ner_model = '7classes')
K_g2, Y_g2 = g.toGraph(graph_win_size, 
					   node_attr_type, vec_dim, 10, vec_model, 
					   'ner', 'diffusion', 
					   pos_model = 1.0, ner_model = '7classes')
K_g3, Y_g3 = g.toGraph(graph_win_size, 
					   node_attr_type, vec_dim, 10, vec_model,
					   'pos', 'diffusion', 
					   pos_model = 1.0, ner_model = '7classes')

#-- bag of wrods --#
b = bagOfWords('{}.txt'.format(dataset_name), dataset_name, 
							punc = punc_tf, stpw = stpw_tf)

X_b, Y_b = b.toBagOfWords(bow_model = bow_model)

#-- doc2vec --#
v = vector('{}.txt'.format(dataset_name), dataset_name, 
						punc = punc_tf, stpw = stpw_tf)

X_v, Y_v = v.toVector(vec_dim, vec_win_size, vec_model)

############### Validation ##############
times_num = 10
folds_num = 10
# seeds = random.sample(range(1,100),10)
seeds = [1,2,3,4,5,6,7,8,9,10] # fix the seed
print ''
print '******** graph of words (ner+pos+naive) ********'
crossValidate(Y_g1, K_g1 + K_g3 + K_g2, 'precomputed', seeds, fold = folds_num, times = times_num)
print ''
print '******** graph of words (pos+naive) ********'
crossValidate(Y_g1, K_g1 + K_g3, 'precomputed', seeds, fold = folds_num, times = times_num)
print ''
print '******** graph of words (pos+ner) ********'
crossValidate(Y_g1, K_g2 + K_g3, 'precomputed', seeds, fold = folds_num, times = times_num)
print ''
print '******** graph of words (pos) ********'
crossValidate(Y_g3, K_g3, 'precomputed', seeds, fold = folds_num, times = times_num)
print ''
print '******** graph of words (ner) ********'
crossValidate(Y_g2, K_g2, 'precomputed', seeds, fold = folds_num, times = times_num)
print ''
print '******** graph of words (naive) ********'
crossValidate(Y_g1, K_g1, 'precomputed', seeds, fold = folds_num, times = times_num) 
print ''
print '******** bag of words ({},{}) ********'.format(bow_model, kernel_type)
crossValidate(Y_b, X_b, kernel_type, seeds, fold = folds_num, times = times_num)
print ''
print '******** doc2vec ({}) ********'.format(kernel_type)
crossValidate(Y_v, X_v, kernel_type, seeds, fold = folds_num, times = times_num)


