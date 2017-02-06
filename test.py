from convert import representations
from convert import window
from convert import graph
from prep_amazon import *
from time import time
from nltk.tokenize import word_tokenize
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tag import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
import util

##################  test of stanford  ####################
# set stanford parser
path_to_jar = '/Users/SunYu/nltk_data/stanford-parser-full-2016-10-31/stanford-parser.jar'
path_to_models_jar = '/Users/SunYu/nltk_data/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar'
dep_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

# test case
sentence = 'Recent studies have demonstrated that specificity is an important characterization of texts potentially beneficial for a range of applications such as multi-document news summarization and analysis of science journalism' 

s = time()
t = dep_parser.raw_parse(sentence)
te = t.next()
print time() - s
print list(te.triples())

# set stanford pos-tagger
path_to_jar = '/Users/SunYu/nltk_data/stanford-postagger-2016-10-31/stanford-postagger.jar'
path_to_models = '/Users/SunYu/nltk_data/stanford-postagger-2016-10-31/models/english-bidirectional-distsim.tagger'
st = StanfordPOSTagger(path_to_models, path_to_jar)
s = time()
tagged = st.tag(sentence.split())
print time() - s
print tagged

# set stanford ner-tagger 
# something wrong with stanford ner tagger()
path_to_jar = '/Users/SunYu/nltk_data/stanford-ner-2016-10-31/stanford-ner.jar'
path_to_models = '/Users/SunYu/nltk_data/stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz'
snt = StanfordNERTagger(path_to_models, path_to_jar)
s = time()
tagged = snt.tag(sentence.split())
print time() - s
print tagged

##############  test of graph  #################
# sentence = 'Recent studies have demonstrated that'
# tokens = util.rmPunctuations(word_tokenize(sentence.lower()))
# win = window(3)
# g = graph(3)
# tokenToID = g.helper([tokens])
# print tokenToID
# edge_attr = win.slidingWindow(tokens,tokenToID)
# print edge_attr