from prep_amazon import *
from util import *
from time import time
from nltk.tokenize import word_tokenize
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tag import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
from representations import vector
from representations import bagOfWords
import numpy

##################  test of stanford  ####################
# set stanford parser
# path_to_jar = '/Users/SunYu/nltk_data/stanford-parser-full-2016-10-31/stanford-parser.jar'
# path_to_models_jar = '/Users/SunYu/nltk_data/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar'
# dep_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

############  test of stanford functions  ##############

# test case
# sentence1 = 'I kissed Irene in my sleep I love her at Washington University in St Louis I make $100 a day from 9:00pm to 10:00pm' 
# sentence2 = 'Panama Buena Vista Union School District is a Kindergarten - 8th grade public school district in Bakersfield, California. The district has 23 schools, and serves Southwest Bakersfield .'
# sentences = []
# sentences.append(sentence1.encode().split())
# sentences.append(sentence2.encode().split())
# sentence3 = sentence1 + ' . ' + sentence2


# s = time()
# t = dep_parser.raw_parse(sentence)
# te = t.next()
# print time() - s
# print list(te.triples())

# set stanford pos-tagger
# path_to_jar = '/Users/SunYu/nltk_data/stanford-postagger-2016-10-31/stanford-postagger.jar'
# path_to_models = '/Users/SunYu/nltk_data/stanford-postagger-2016-10-31/models/english-bidirectional-distsim.tagger'
# st = StanfordTokenizer(path_to_models, path_to_jar)
# s = time()
# tagged = st.tag(sentence.split())
# print time() - s
# print tagged

# set stanford ner-tagger 
# path_to_jar = '/Users/SunYu/nltk_data/stanford-ner-2016-10-31/stanford-ner.jar'
# path_to_models = '/Users/SunYu/nltk_data/stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz'
# snt = StanfordNERTagger(path_to_models, path_to_jar)
# s = time()
# tagged = snt.tag(sentence2.split())
# tagged2 = snt.tag(sentence3.split())
# print sentence3
# print time() - s
# print tagged[0]
# print tagged[1]
# print tagged2

# from pycorenlp import StanfordCoreNLP
# nlp = StanfordCoreNLP('http://localhost:9000')
# output = nlp.annotate(sentence, 
# 					  properties={
# 					  	'annotators': 'tokenize,ssplit,pos,depparse,parse',
# 					  	'outputFormat':'json'}
# 					  )

# print(output['sentences'][0]['parse'])
# output = nlp.tokensregex(text, pattern='/Pusheen|Smitha/', filter=False)
# print(output)
# output = nlp.semgrex(text, pattern='{tag: VBD}', filter=False)
# print(output)

############# spacy ner test ###############
# import spacy
# s = time()
# nlp = spacy.load('en')
# doc = nlp(sentence)
# for ent in doc.ents:
#     print(ent.label_, ent.text)
# print time() - s

##############  test of graph  #################
# g = graph('test.txt', 'test_example', punc = True, stpw = False)
# g.toGraph(5)
# print g.tokenToID_list[0]

##############  test of matlab API ############
# from prop_kernel import propKernel
# from sklearn import svm
# clf = svm.SVC(kernel='precomputed')
# K = propKernel('/Users/SunYu/Desktop/598_project/graph', 'test_example')
# # Y = [1,2,3]
# # clf.fit(K,Y)
# print K

############# test of util ############
# sentence = 'I kissed Irene in my sleep. I do like her. I hope she is alive.'
# s = rmStringPunctuations(sentence)
# print s[0]

############# test of vector ############
dataset_name = 'eduIns_horRdr'
v = vector('{}.txt'.format(dataset_name), dataset_name, 
							punc = True, stpw = True)
X_v, Y_v = v.toVector(10, 10, 0)

print X_v
print Y_v
############ test of bagofwords ##########
dataset_name = 'eduIns_horRdr'
b = bagOfWords('{}.txt'.format(dataset_name), dataset_name, 
			   punc = True, stpw = True)

X_b, Y_b = b.toBagOfWords(bow_model = 'count')

print Y_b






