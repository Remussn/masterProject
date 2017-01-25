import os
import re

# **********************************************************************************
#   This utility file stores all addtional functions you need for prepocessing.py,
#   learning.py and main.py.
#
# **********************************************************************************

# ###################### FUNCTIONS FOR PREPROCESSING ####################

# --------- MATCH LOADSOURCE FUNCTION ---------
# One aug: source_path

def loadSource(source_path):
    classSource = open(source_path, "r")
    class_dicts = {}
    for line in classSource:
        if line[0] == "#":        # get rid of useless lines
            continue
        fractions = line.rstrip().split(" ")
        entry = fractions[0].split("/")[-1][:-1]
        class_name = fractions[2].split("/")[-1][:-1]
        class_dicts[entry] = class_name
    classSource.close()
    return class_dicts


# -------- LOADSTOPWORDS FUNCTION ----------
# One aug: source_path

def loadStopWords(source_path):
    source = open(source_path, "r")
    stopWords = set()
    for line in source:
        word = line.rstrip()
        stopWords.add(word)
    return stopWords
