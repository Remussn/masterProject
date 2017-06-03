# This script is used for preprocess amazon review data, including parsing, tokenizing and etc.
import re
import os
import random
import math

def preparseAmazon(path):
	f = open(path,'r')
	for l in f:
		yield eval(l)


def parseAmazon(in_path, out_path):
	output = open('rate_reviews_Amazon_Instant_Video_small.txt', 'w')
	for l in preparseAmazon('reviews_Amazon_Instant_Video_5.json'):
		num = math.floor(15 * random.random() + 1)
		if num <= 1:
			rate 	= l['overall']
			content = re.sub(r'[^\x00-\x7f]',r' ',l['reviewText']) # remove all non utf-8 characters
			output.write(str(rate) + '\t' + content + '\n')
		else:
			pass

def mergeAmazon(path1,path2):
	f1 = open(path1, 'r')
	f2 = open(path2, 'r')
	for l in f1:
		




# parseAmazon('reviews_Amazon_Instant_Video_5.json', 'rate_reviews_Amazon_Instant_Video_small.txt')
# mergeAmazon('rate_reviews_Amazon_Instant_Video_small.txt', 'rate_reviews_Amazon_Musical_Instruments_small.txt')