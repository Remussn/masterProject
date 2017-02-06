import os
import re
import sys
import string
import util
from collections import deque
from sets import Set
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#####******* all representaions ********######

# input format:
#	label + '\t' + text(should all in lowercase, punc and stopword can be kept)


class representations:

	self.g_labels = []
	self.g_tokens_list = []

	# preprocessing with father class
	def __init__(self，in_path, corpus_name):
		# initialize parameters
		self.in_path = in_path
		self.corpus_name = corpus_name
		# parse
		data = open(self.in_path,'r')
		for l in data:
			sections = l.split('\t')[0]
			g_label = sections[0]
			g_tokens = word_tokenize(sections[1].lower())
			self,g_labels.append(g_label)
			self.g_tokens_list.append(g_tokens) # a list of list of tokens
		data.close()


###########################  Graph  #############################

class graph(representation):
	'class Graph, represent text as graph, successor of class representation.'
	# should give input path when initialize the graph object
	# Input Format:
	# 	label + \t + content(lowercase) 

	def __init__(self, winSize, punc, stpw):
		self.tokenToID = {}
		words = set()
		for tokens in self.g_tokens_list:
			# remove punc
			if punc: 
				tokens = util.rmPunctuations(tokens)
			# remove stopwords
			if stpw:
				tokens = util.rmStopwords(tokens)
			for token in tokens:
				words.add(token)
		
		t_id = 1
		for word in words:
			self.tokenToID[word] = t_id
			t_id = t_id + 1

	# specify the name of your dataset
	def toGraph(self,winSize):
		# output three txt files.
		getEdges(winSize)
		# output labels of nodes


	def getNodes(self):
		path_to_jar = '/Users/SunYu/nltk_data/stanford-postagger-2016-10-31/stanford-postagger.jar'
		path_to_models = '/Users/SunYu/nltk_data/stanford-postagger-2016-10-31/models/english-bidirectional-distsim.tagger'
		spost = StanfordPOSTagger(path_to_models, path_to_jar)

		ds_a_path = '{}_graph_result/{}_A.txt'.format(self.corpus_name)
		for tokens in self.g_tokens_list:
			tagged = spost.tag(tokens):		
				for ele in tagged:
					pass

	# output DS_A.txt, DS_edge_attr.txt, DS_grpah_id.txt
	# all files related to edges
	def getEdges(self, winSize):
		# terminology corresponding to https://ls11-www.cs.tu-dortmund.de/staff/morris/graphkerneldatasets
		# num of edges of all graphs is m.
		ds_a_path = '{}_graph_result/{}_A.txt'.format(self.corpus_name)
		ds_edge_attr_path = '{}_graph_result/{}_edge_attributes.txt'.format(self.corpus_name)
		ds_graph_indicator_path = '{}_graph_result/{}_graph_indicator.txt'.format(self.corpus_name)
		ds_a = open(ds_a_path,'w') # each line represents for one edge. (size = m)
		ds_edge_attr = open(ds_edge_attr_path,'w') # indicate the attribute of the ith edge (each line represents one edge) (size  = m)
		ds_graph_indicator = open(ds_graph_indicator_path,'w') # indicate the ith edge belonging to jth graph (each line represents one edge) (size = m)

		# generate window
		win = window(winSize)
		num_graph = 0
		for tokens in g_tokens_list:
			num_graph = num_graph + 1 # graph num starts at 1
			edge_attr = win.slidingWindow(tokens, self.tokenToID) # use sliding window
			for edge in edge_attr.keys():
				ds_a.write(edge + '\n') # output edge
				ds_edge_attr.write(edge_attr[edge] + '\n') # output attr
				ds_graph_indicator.write(str(num_graph) + '\n')

		ds_a.close()
		ds_edge_attr.close()
		ds_graph_indicator.close()


# WINDOW
# we can add another window function if we want
class window(object):
	def __init__(self, winSize):
		self.size = winSize
		self.queue = deque()
		self.edge_attr = {}
	
	# emit DS_A.txt file
	# return a dict....
	# windowSize must be greater than one
	def slidingWindow(self, tokens, tokenToID):
		for cur_token in tokens:
			# pop()
			q_l = len(self.queue)
			if q_l == 0:
				pass
			elif q_l % self.size == 0: # pop the first element when length of queue reach the window size
				self.queue.popleft()

			# sliding window
			if len(self.queue) == 0:
				pass
			else: # link cur_token to every token in queue
				for token in self.queue:
					# for undirected graph, ignore the order
					# for directed graph, order indicate the direction of edge
					token_id = tokenToID[token]
					cur_token_id = tokenToID[cur_token]
					try:
						self.edge_attr[(token_id,cur_token_id)] += 1 # follows text natural order
					except:
						self.edge_attr[(token_id,cur_token_id)] = 1
			# append cur_token at last
			self.queue.append(cur_token)
		return self.edge_attr











			
