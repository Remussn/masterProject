import os
import re
import word2vec
import math
from sklearn import svm
from sklearn import linear_model
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import CountVectorizer

class learning(object):
    
    def __init__(self):
        self.root = os.getcwd()
    
# ---------- GENERATING VECTOR FUNCTION -----------
# The function generate a vector for each text, and combine all the vectors as a single output .bin file,
# which will be stored under the directory named "learning_tempData".
# This function will return the generated vector as list
#
# FORMAT:
# the id format: id*file_id.
# example:
#   0*1, 1231*3
# such that each line in the files has an unique id

# generate a dict to store meta data:
#   (file_id : label)
# ex:
#   (file_id : Anstronaut)
#   (file_id : Glacier)
#
# AUGS:
# 1. varying number of input_path parameters.(using **dict for store the augs)
# 2. your input_path format is:
#       class1_name = "input_path"
#       class2_name = "input_path"
#          .
#          .
#          .
# 3. you can the parameters other than **input_path blank. The function will use the default ones
# 4. return list[list[],list[],dict{}]
#
# Note: If binFile = true, the temperary files will be deleted
#       you can specify the size of final vector through size_l
#       you can set multiple pathes in the function
#
# Return: list[data, label, file_label]
#               []     []       {}
#


    def getVector(self, size_l, window_l, binFile=True, **input_paths):

        # set file path
        output_path = os.path.join(self.root,"learning_tempData")
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        temp_path = os.path.join(output_path,"temp.txt")
        temp = open(temp_path,"w")  # delete temp.txt when the function is finished

        # initialization
        file_num_id = {} # file: corresponding num of ids
        file_label = {} # file: corresponding label
        file_id = 1

        # create temp file
        for key,input_path in input_paths.iteritems():
            input = open(input_path, "r")
            id = 0
            for line in input:
                fractions = line.rstrip().split('\t')
                label = fractions[0]
                content = fractions[1]
                line_id = str(id) + "*" + str(file_id)
                temp.write(line_id + " " + content + '\n')
                id = id + 1
            file_label[str(file_id)] = label
            file_num_id[label] = id
            file_id = file_id + 1
        temp.close()

        # calculation
        bin_path = os.path.join(output_path,"vectors.bin")

        # not deal with passing **dict parameters
        word2vec.doc2vec(temp_path, bin_path, cbow=0, size=size_l, window=window_l, negative=5, hs=0, sample='1e-4', threads=12, iter_=20, min_count=1, verbose=True)
    #    word2vec.doc2vec(temp_path, bin_path, cbow, size, window, negative, hs, sample, threads, iter_, min_count, verbose)


        model = word2vec.load(bin_path)

        # get data and label
        data = list()
        label = list()
        for file_key in file_label.keys():
            current_file = file_label[file_key]
            num = file_num_id[current_file]
            for i in range(num):
                line_id = "{}*{}".format(str(i),file_key)
                vector = model[line_id]
                data.append(vector)
                label.append(int(file_key))

        # delete the temp.txt file
        os.remove(os.path.join(output_path,"temp.txt"))
        if not binFile:
            os.remove(bin_path)

        return [data,label,file_label]



    # ---------- GENERATING BAG OF WORDS FUNCTION -----------
    # The function is designed for computing bag of words for given raw documents.
    # Three types are available for consideration.
    #
    # ARGS:
    #   there are two kinds of args: 1. type for choosing vectorizer
    #                                2. input pathes
    #   1. there are three vectorizers available for getting bag of words.
    #      "countVectorizer", "tfidfVectorizer" and "hashingVectorizer"
    #      the default is "countVectorizer"
    #   2. input pathes:
    #       class1_name = "input_path"
    #       class2_name = "input_path"
    #          .
    #          .
    #          .
    # OUTPUTS:
    #   there are three outputs: 1. matrix X as list
    #                            2. vector Y as list
    #                            3. file_label as dict
    #
    #
    #
    #
    #
    #

    def getBagOfWords(self, type = "countVectorizer",**input_paths):
        
        # preprocessing
        corpus = list()
        y = list()
        file_label = {}

        label_id = 0
        for key,input_path in input_paths.iteritems():
            input = open(input_path, "r")
            for line in input:
                fractions = line.rstrip().split('\t')
                label = fractions[0]
                content = fractions[1]
                corpus.append(content)
                y.append(str(label_id))
            file_label[label] = label_id
            label_id = label_id + 1
        
        # initialize & compute
        if type == "countVectorizer":
            countVectorizer = CountVectorizer()
            x = countVectorizer.fit_transform(corpus)
        elif type == "tfidfVectorizer":
            tfidfVectorizer = TfidfVectorizer()
            x = tfidfVectorizer.fit_transform(corpus)
        elif type == "hashVectorizer":
            hashingVectorizer = HashingVectorizer()
            x = hashVectorizer.fit_transform(corpus)

        return [x,y,file_label]


