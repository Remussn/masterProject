# 2017-4-21
# Yu Sun

import os
import re
import numpy
from util import *
from sortedcontainers import SortedSet
from collections import OrderedDict
from nltk.tokenize import word_tokenize

	
#######################################################################
#######                                                         #######
#######                    ALL REPRESENTATIONS                  #######
#######                                                         #######
#######################################################################

# input format:
#	label + '\t' + text

class representations(object):

	# how to pass the parameter to children class, one thought: import parse() in the father class.
	# preprocessing with father class
	def __init__(self, in_path, corpus_name):
		# initialize parameters
		self.labels 	 = [] # list of label of each datapoint (lowercased)
		self.contents 	 = [] # list of contents of each datapoints (original raw data)
		self.labelToID   = OrderedDict() # dic mapping label to unique id, keep in order
		self.in_path 	 = in_path
		self.corpus_name = corpus_name
		self.parse()

		# parse
	def parse(self):
		labels = []
		labels_set = OrderedSet()  # a list that store all different labels. keep order!
		data = open(self.in_path,'r')
		for l in data:
			sections = l.split('\t')
			label 	 = sections[0].lower() 	   # label in lower case.
			content  = sections[1].rstrip()	   # need to be case-sensitive
			tokens   = word_tokenize(content)  # content in lower case.
			self.contents.append(content) 	   # no preprocessing excution on contents
			self.labels.append(label)
			labels_set.add(label)
		data.close() # close file

		#-- give id to each label --#
		label_id = 1
		for ele in labels_set:
			self.labelToID[ele] = label_id
			label_id = label_id + 1		

	# order of labels is kept in labels
	def getLabelList(self):
		return self.labelToID.keys()

	def getLabelIdxList(self):
		return [self.labelToID[label] for label in self.labels]
		# labelIdxList = []
		# for label in self.labels:
		# 	labelIdxList.append(self.labelToID[label])
		# return labelIdxList

	# order of contents is kept in self.contents
	def getContentList(self):
		return self.contents


###############################################################
#####                         GRAPH                       #####
###############################################################

from window import window
from nodeLabel import nodeLabels
from nodeAttributes import nodeAttributes
from propagationKernel import propKernel

class graph(representations):
	
	'class Graph, represent text as graph, successor of class representation.'
	
	def __init__(self, in_path, corpus_name, min_wl = 2, punc = True, stpw = True):
		super(graph, self).__init__(in_path, corpus_name)
		self.punc 	= punc
		self.stpw 	= stpw
		self.min_wl = min_wl
		self.all_words = OrderedSet() # all unique
		self.tokens_list 	= [] # list of list of tokens of each datapoint, operation on punctuations only.
		self.tokenToID_list = [] # list of dictionaries, each dictionary for one datapoint, operation on punctuations only.
		self.K 				= None
		self.Y 				= None
		self.__helper()

	def __helper(self):
		# remove punc
		if self.punc: 
			contents = rmListStringPunctuations(self.contents)

		# remove stopwords
		if self.stpw:
			contents = rmListStringStopwords(contents)
		
		# remove word that its length less than min_wl
		contents = rmListStringShortWords(contents, self.min_wl)

		t_id = 1 # token id starts at 1
		for content in contents:
			tokenToID = OrderedDict()
			words = OrderedSet()
			tokens = word_tokenize(content.lower())  # uppercase --> lowercase
			self.tokens_list.append(tokens)
			# unique words
			for token in tokens:
				words.add(token)
				self.all_words.add(token)
			# generate dictionary for each sentence
			for word in words:
				tokenToID[word] = t_id
				t_id = t_id + 1
			# add to tokenToID dictionary
			self.tokenToID_list.append(tokenToID)

	# output DS_node_labels.txt
	def __getNodesLabels(self, nd_label_type, ner_model, pos_model):
		# Stanford PosTagger()
		# path_to_jar = '/Users/SunYu/nltk_data/stanford-postagger-2016-10-31/stanford-postagger.jar'
		# path_to_models = '/Users/SunYu/nltk_data/stanford-postagger-2016-10-31/models/english-bidirectional-distsim.tagger'
		# spost = StanfordPOSTagger(path_to_models, path_to_jar)

		#-- intialize path --#
		ds_node_labels_path 	 = '{}/{}_node_labels.txt'.format(self.corpus_name,self.corpus_name)
		ds_node_labels_dict_path = '{}/{}_node_labels_dict.txt'.format(self.corpus_name,self.corpus_name)

		#-- get labels -- #
		getLabel = nodeLabels(self.contents, self.tokenToID_list, self.min_wl, self.punc, self.stpw)

		# not remove stopwords in IDToTag
		for case in switch(nd_label_type):
			if case('pos'):
				IDToTag, node_labelToID = getLabel.posTag(pos_model)
				break
			if case('ner'):
				IDToTag, node_labelToID = getLabel.nerTag(ner_model)
				break
			if case('word'):
				IDToTag, node_labelToID = getLable.wordTag(self.all_words)

			if case('naive'):
				IDToTag, node_labelToID = getLabel.naive()
				break
			if case('none'):
				print 'No {}_node_labels.txt output'.format(self.corpus_name)
				try:
					os.remove(ds_node_labels_path)
				except:
					pass
				return
			if case():
				print 'nd_label_type is not available'
				quit()
				# IDToTag, node_labelToID = getLabel.naive()
				# No need to break here, it'll stop anyway
				# if case('word'):
					# IDToTag, node_labelToID = getLabel.wordTag(self.all_words)
					# break

		#-- output dictionary --#
		print 'An unique ID will be assigned to each node label. The dictionary will be exported as a text file in the database folder.\nNode_label Dictionary:'
		ds_node_labels_dict = open(ds_node_labels_dict_path,'w')
		for key in node_labelToID.keys():
			l_id = node_labelToID[key]
			ds_node_labels_dict.write(str(key)+ ': ' + str(l_id) + '\n')
			print '\t' + str(key) + ': ' + str(l_id)
		ds_node_labels_dict.close()

		#-- node_label files --#
		ds_node_labels = open(ds_node_labels_path,'w')
		for key in IDToTag.keys():
			label = IDToTag[key]
			ds_node_labels.write(str(label)+'\n')
		ds_node_labels.close()

	# output DS_node_attributes.txt
	def __getNodesAttributes(self, nd_attr_type, vec_dim, vec_win_size, vec_model):
		#-- intialize path --#
		ds_node_attr_path = '{}/{}_node_attributes.txt'.format(self.corpus_name,self.corpus_name)

		#-- get labels --#
		getAtrr = nodeAttributes(self.contents, self.tokenToID_list, self.corpus_name, self.punc, self.stpw)
		# switch
		for case in switch(nd_attr_type):
			if case('word2vec'):
				IDToTag = getAtrr.vecAttribute(vec_dim, vec_win_size, vec_model)
				break
			if case('tfidf'):
				IDToTag = getAtrr.tfidfAttribute()
				break
			if case('none'):
				print 'No {}_node_attributes.txt output'.format(self.corpus_name)
				try:
					os.remove(ds_node_attr_path)  # remove previous attribute files
				except:
					pass
				return
			if case():
				print 'nd_attr_type is not available'
				quit()

		#-- node attributes files --#
		print 'Use {} model to compute each word a unique embedding.'.format(nd_attr_type)
		ds_node_attr = open(ds_node_attr_path,'w')
		for key in IDToTag.keys():
			attr = IDToTag[key]
			ds_node_attr.write(attr + '\n')
		ds_node_attr.close()
	
	# output DS_A.txt, DS_edge_attr.txt, DS_grpah_indicator.txt
	# all files related to edges
	def __getEdges(self, winSize, graph_type):

		#-- initalize path --#
		# num of edges of all graphs is m.
		ds_a_path = '{}/{}_A.txt'.format(self.corpus_name,self.corpus_name)
		ds_edge_attr_path = '{}/{}_edge_attributes.txt'.format(self.corpus_name,self.corpus_name)
		ds_graph_indicator_path = '{}/{}_graph_indicator.txt'.format(self.corpus_name,self.corpus_name)

		ds_a = open(ds_a_path,'w') 					# each line represents for one edge. (size = m)	
		ds_edge_attr = open(ds_edge_attr_path,'w')  # indicate the attribute of the ith edge (each line represents one edge) (size  = m)
		ds_graph_indicator = open(ds_graph_indicator_path,'w') # indicate the ith edge belonging to jth graph (each line represents one edge) (size = m)

		#-- generate window --#
		win = window(winSize, graph_type)
		num_graph = 0
		for i in range(len(self.tokens_list)):
			num_graph = num_graph + 1 # graph num starts at 1
			edge_attr = win.slidingWindow(self.tokens_list[i], self.tokenToID_list[i]) # use sliding window
			for edge in sorted(edge_attr.keys()):
				ds_a.write(str(edge[0]) + ', ' + str(edge[1]) + '\n') # output edge
				ds_edge_attr.write(str(edge_attr[edge]) + '\n') # output attr 
			for j in sorted(self.tokenToID_list[i].values()):
				ds_graph_indicator.write(str(num_graph) + '\n') # node to graph indicator

		ds_a.close()
		ds_edge_attr.close()
		ds_graph_indicator.close()


	# return numpy arrary variables
	# 	K:	Kernel Matrix
	# 	Y:	Label
	# use attr_diff
	def toGraph(self, winSize, nd_attr_type, vec_dim, vec_win_size, vec_model, nd_label_type, label_transform_model, ner_model = '7classes', pos_model = 1.0, graph_type = 'undirected'):
		print ''
		print '********************'
		print '* toGraph() starts *'
		print '********************'
		# check & create result folder
		if not os.path.exists('{}/'.format(self.corpus_name)):
			os.mkdir('{}/'.format(self.corpus_name))

		#-- output graph_label_id_dic txt file --# 
		p = '{}/{}_graph_label_id_dict.txt'.format(self.corpus_name, self.corpus_name)
		d = open(p,'w')

		print 'GRAPH EDGES: '
		print 'An unique ID will be assigned to each graph label. The dictionary will be exported as a text file in the database folder.\nGraph_label Dictionary:'

		for key,item in self.labelToID.iteritems():
			print '\t' + key + ': ' + str(item)
			d.write(key + ': ' + str(item) + '\n')
		d.close()

		#-- output ds_graph_labels.txt --#
		ds_graph_labels_path = '{}/{}_graph_labels.txt'.format(self.corpus_name, self.corpus_name)
		f = open(ds_graph_labels_path, 'w')
		for label in self.labels:
			# self.labels_id = 
			f.write(str(self.labelToID[label]) + '\n')
		f.close()

		#-- output ds_a_path, ds_edge_attr_path, ds_graph_indicator --#
		self.__getEdges(winSize, graph_type)

		print 'NODE LABELS: '
		#-- output labels of nodes --#
		self.__getNodesLabels(nd_label_type, ner_model, pos_model)

		print 'NODE ATTRIBUTES: '
		#-- output attributes of nodes --#
		self.__getNodesAttributes(nd_attr_type, vec_win_size, vec_dim, vec_model) 

		#-- get kernel --#
		temp 	  = [str(self.corpus_name), str(self.punc), str(self.stpw), 
					str(winSize),   str(nd_attr_type),  str(vec_dim), str(vec_win_size), 
					str(vec_model), str(nd_label_type), str(label_transform_model), 
					str(ner_model), str(pos_model),     str(graph_type)]

		file_name = 'Kernels/' + '_'.join(temp) + '_Kernel'

		try: # load kernel
			self.K = numpy.load(file_name + '.npy')
			print 'KERNEL LOADED'

		except: # compute kernel
			print 'KERNEL COMPUTING...'
			self.K = propKernel('/Users/SunYu/Desktop/598_project/graph', 
								self.corpus_name, label_transform_model) 
			print 'KERNEL SAVING...'
			numpy.save(file_name, self.K)

		L = self.getLabelIdxList()
		self.Y = numpy.array(L)

		return self.K, self.Y # [self.labelToID[label] for label in self.labels] # as Y

	# get K
	def get_K(self):
		return self.K

	def get_Y(self):
		return self.Y

########################################################
#####                 BAG OF WORDS                 #####
########################################################

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

class bagOfWords(representations):
	'class bagOfWords, represents text as bag of words, successor of class representation.'	

	def __init__(self, in_path, corpus_name, punc = True, stpw = True):
		super(bagOfWords, self).__init__(in_path, corpus_name)
		self.punc = punc
		self.stpw = stpw
		self.X 	  = None
		self.Y    = None
		self.__helper()

	def __helper(self):
		# remove punc
		if self.punc: 
			self.contents = rmListStringPunctuations(self.contents)
		# remove stopwords
		if self.stpw:
			self.contents = rmListStringStopwords(self.contents)

	def toBagOfWords(self, bow_model = 'count'):
		print ''
		print '*************************'
		print '* toBagOfWords() starts *'
		print '*************************'
		#-- select --#
		for case in switch(bow_model):
			if case('count'):
				print 'COMPUTING COUNTS'
				countVectorizer = CountVectorizer()
				self.X = countVectorizer.fit_transform(self.contents)
				break
			if case('tfidf'):
				print 'COMPUTING TF-IDF'
				tfidfVectorizer = TfidfVectorizer()
				self.X = tfidfVectorizer.fit_transform(self.contents)
				break
			if case('hash'):
				print 'COMPUTING HASHING'
				hashingVectorizer = HashingVectorizer()
				self.X = hashVectorizer.fit_transform(self.contents)
				break
			if case():
				print 'required model is not available'
				quit()

		#-- get X,Y --#
		L = self.getLabelIdxList()
		self.Y = numpy.array(L)

		return  self.X, self.Y # [self.labelToID[label] for label in self.labels] # as Y

	def get_X():
		return self.X

	def get_Y(self):
		return self.Y

########################################################
#####                   VECTOR                     #####
########################################################

import word2vec

class vector(representations):
	'class doc2vec, represents text as vector, successor of class representation.'

	def __init__(self, in_path, corpus_name, punc = True, stpw = True):
		super(vector, self).__init__(in_path, corpus_name)
		self.temp_path = '{}_temp.txt'.format(corpus_name)
		self.punc 	   = punc
		self.stpw 	   = stpw
		self.X 		   = []
		self.Y 		   = None
		self.__helper()

	def __helper(self):
		temp = open(self.temp_path,"w")  # delete temp.txt when the function is finished
		
		# remove punc
		if self.punc: 
			self.contents = rmListStringPunctuations(self.contents)
		# remove stopwords
		if self.stpw:
			self.contents = rmListStringStopwords(self.contents)

		c_id = 1		
		for content in self.contents:
			temp.write(str(c_id) + " " + content.lower() + '\n')
			c_id += 1
		temp.close()

	def toVector(self, vec_dim, win_size, vec_model):
		print ''
		print '*********************'
		print '* toVector() starts *'
		print '*********************'
		# cbow = 0/1
		# size = vec_dim
		# window = win_size
		bin_path = '{}_vectors.bin'.format(self.corpus_name)
		word2vec.doc2vec(self.temp_path, bin_path, cbow = vec_model, 
						size = vec_dim, window = win_size, 
						negative = 5, hs = 0, sample = '1e-4', 
						threads = 12, iter_ = 20, 
						min_count = 1, verbose = True)
		mode = word2vec.load(bin_path)
		for c_id in range(len(self.contents)):
			self.X.append(mode[str(c_id+1)])
		os.remove(bin_path)
		os.remove(self.temp_path)

		#-- get X,Y --#
		L = self.getLabelIdxList()
		self.Y = numpy.array(L)

		return numpy.array(self.X), self.Y

	def get_X(self):
		return numpy.array(self.X)

	def get_Y(self):
		return self.Y

