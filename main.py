from preprocessing import *
from learning import *
import re
import os
import numpy
from time import time
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score



root = os.getcwd()
input_rel = "original_data/long_abstracts_en.ttl"
input_path = os.path.join(root, input_rel)

# *************** Preprocessing ***************
preprocessor = preprocessing()
# test parse()
#preprocessor.parse(input_path)

# test match()
#preprocessor.match()

# test classify()
#preprocessor.classify()

# test rmStopWords()
#test_input = os.path.join(root, "subclasses_longAbstracts/airport_longAbstracts.txt")
#preprocessor.rmStopWords(test_input,output_path = os.path.join(root,"stopwords_removed/airport.txt"))
#
#test_input = os.path.join(root, "subclasses_longAbstracts/protein_longAbstracts.txt")
#preprocessor.rmStopWords(test_input,output_path = os.path.join(root,"stopwords_removed/protein.txt"))
#
#test_input = os.path.join(root, "subclasses_longAbstracts/protectedarea_longAbstracts.txt")
#preprocessor.rmStopWords(test_input,output_path = os.path.join(root,"stopwords_removed/protectedarea.txt"))

test_input = os.path.join(root, "subclasses_longAbstracts/basketballplayer_longAbstracts.txt")
rmStopWords(test_input,output_path = os.path.join(root,"stopwords_removed/basketballplayer.txt"))

test_input = os.path.join(root, "subclasses_longAbstracts/rugbyplayer_longAbstracts.txt")
rmStopWords(test_input,output_path = os.path.join(root,"stopwords_removed/rugbyplayer.txt"))

test_input = os.path.join(root, "subclasses_longAbstracts/soccermanager_longAbstracts.txt")
rmStopWords(test_input,output_path = os.path.join(root,"stopwords_removed/soccermanager.txt"))

# test get_statistic()
#get_statistics()


# ************** Learning *****************

learner = learning()

output_rel = "test/comparison_similar_classes.tsv"
output_path = os.path.join(root,output_rel)

d = os.path.dirname(output_path)
if not os.path.exists(d):
    os.mkdir(d)
output = open(output_path,"w")

#output.write("size  svn knn decisionTree" + '\n')
output.write("svn" +'\t' + "knn" + '\n')


#for size in range(20) :
#    data,label = getVector(size+1, binFile = False,
#                       snookerchamp = os.path.join(root,"subclasses_longAbstracts/musical_longAbstracts.txt"),
#                      volleyballcoach = os.path.join(root,"subclasses_longAbstracts/hockeyteam_longAbstracts.txt"),
#                      spacestation = os.path.join(root,"subclasses_longAbstracts/lighthouse_longAbstracts.txt"))
#    # svm
#    clf = svm.SVC(kernel = 'linear', C =1)
#    score_SVC = cross_val_score(clf, data, label, cv=10)
#    print "SVM cross_val score: {}  Vec Size: {}".format(numpy.mean(score_SVC),size+1)
#    # knn
#    neigh = KNeighborsClassifier(n_neighbors=3)
#    score_KNN = cross_val_score(neigh, data, label, cv=10)
#    print "KNN cross_val score: {}  Vec Size: {}".format(numpy.mean(score_KNN),size+1)
#    # decision tree
#    tree = DecisionTreeClassifier(criterion='entropy')
#    score_tree = cross_val_score(tree, data, label, cv=10)
#    print "DecisionTree cross_val score: {}  Vec Size: {}".format(numpy.mean(score_tree),size+1)
#   output.write(str(size+1) + '\t' + str(numpy.mean(score_SVC)) + '\t' + str(numpy.mean(score_KNN)) + '\t' + str(numpy.mean(score_tree)) + '\n')


# word2vec:
train_time_word2vec = time()
vecSize = 100;
windSize = 100;
data1,label1,file_label1 = learner.getVector(vecSize, windSize, binFile = False,
                                     input1 = os.path.join(root,"stopwords_removed/soccermanager.txt"),
                                     input2 = os.path.join(root,"stopwords_removed/rugbyplayer.txt"),
                                     input3 = os.path.join(root,"stopwords_removed/basketballplayer.txt"))
train_time_word2vec = time() - train_time_word2vec

# bag of words:
train_time_bag = time()
data2,label2,file_label2 = learner.getBagOfWords(type = "countVectorizer",
                                         input1 = os.path.join(root,"stopwords_removed/rugbyplayer.txt"),
                                         input2 = os.path.join(root,"stopwords_removed/basketballplayer.txt"),
                                         input3 = os.path.join(root,"stopwords_removed/soccermanager.txt"))
train_time_bag = time() - train_time_bag

# tfidf wordcount:
train_time_tfidf = time()
data3,label3,file_label3 = learner.getBagOfWords(type = "tfidfVectorizer",
                                         input1 = os.path.join(root,"stopwords_removed/rugbyplayer.txt"),
                                         input2 = os.path.join(root,"stopwords_removed/basketballplayer.txt"),
                                         input3 = os.path.join(root,"stopwords_removed/soccermanager.txt"))
train_time_tfidf = time() - train_time_tfidf


output.write(str(train_time_word2vec) + '\t' + str(train_time_bag) + '\t' + str(train_time_tfidf) + '\n')



# svm_linear
clf = svm.SVC(kernel = 'linear', C =0.1)
start = time()
score_SVC_word2vec = cross_val_score(clf, data1, label1, cv=10)
end = time() - start
print "SVM cross_val_word2vec score: {}".format(numpy.mean(score_SVC_word2vec))
output.write("svm_word2vec" + '\t' + str(numpy.max(score_SVC_word2vec)) + '\t' + str(numpy.min(score_SVC_word2vec)) + '\t' + str(numpy.mean(score_SVC_word2vec)) + '\t' + str(end) + '\n')

start = time()
score_SVC_bag = cross_val_score(clf, data2, label2, cv=10)
end = time() - start
print "SVM cross_val_bagOfWords score: {}".format(numpy.mean(score_SVC_bag))
output.write("svm_bagOfWords" + '\t' + str(numpy.max(score_SVC_bag)) + '\t' + str(numpy.min(score_SVC_bag)) + '\t' + str(numpy.mean(score_SVC_bag)) + '\t' + str(end) + '\n')

start = time()
score_SVC_tfidf = cross_val_score(clf, data3, label3, cv=10)
end = time() - start
print "SVM cross_val_tfidf score: {}".format(numpy.mean(score_SVC_tfidf))
output.write("svm_tfidf" + '\t' + str(numpy.max(score_SVC_tfidf)) + '\t' + str(numpy.min(score_SVC_tfidf)) + '\t' + str(numpy.mean(score_SVC_tfidf)) + '\t' + str(end) + '\n')

# knn_kd_tree
neigh = KNeighborsClassifier(n_neighbors=3)
start = time()
score_KNN_word2vec = cross_val_score(neigh, data1, label1, cv=10)
end = time() - start
print "KNN cross_val_word2vec score: {}".format(numpy.mean(score_KNN_word2vec))
output.write("knn_word2vec" + '\t' + str(numpy.max(score_KNN_word2vec)) + '\t' + str(numpy.min(score_KNN_word2vec)) + '\t' + str(numpy.mean(score_KNN_word2vec)) + '\t' + str(end) + '\n')

start = time()
score_KNN_bag = cross_val_score(neigh, data2, label2, cv=10)
end = time() - start
print "KNN cross_val_bagofwords score: {}".format(numpy.mean(score_KNN_bag))
output.write("knn_bagofwords" + '\t' + str(numpy.max(score_KNN_bag)) + '\t' + str(numpy.min(score_KNN_bag)) + '\t' + str(numpy.mean(score_KNN_bag)) + '\t' + str(end) + '\n')

start = time()
score_KNN_tfidf = cross_val_score(neigh, data3, label3, cv=10)
end = time() - start
print "KNN cross_val_bagofwords score: {}".format(numpy.mean(score_KNN_tfidf))
output.write("knn_tfidf" + '\t' + str(numpy.max(score_KNN_tfidf)) + '\t' + str(numpy.min(score_KNN_tfidf)) + '\t' + str(numpy.mean(score_KNN_tfidf)) + '\t' + str(end) + '\n')









# AdaBoost
#ada_boost = AdaBoostClassifier().fit(data,label)
#score_ada = cross_val_score(ada_boost, data, label, cv=10)
#print "ada cross_val score: {}  Vec Size: {}".format(numpy.mean(score_ada),4)

# GBRT
#gb_boost = GradientBoostingClassifier().fit(data,label)
#score_gb = cross_val_score(gb_boost, data, label, cv=10)
#print "gb cross_val score: {}  Vec Size: {}".format(numpy.mean(score_ada),4)

#output.write(str(4) + '\t' + str(numpy.mean(score_SVC)) + '\t' + str(numpy.mean(score_KNN)) + '\t' + str(numpy.mean(score_ada)) + '\t' + str(numpy.mean(score_gb)) + '\n')

#output.write(str(clf) + '\t' + str(neigh) + '\t' + str(ada_boost) + '\t' + str(gb_boost) + '\n')

#for x in data:
#    output2.write(str(x) + '\n')
#
#for y in label:
#    output3.write(str(y) + '\n')


output.close()

















