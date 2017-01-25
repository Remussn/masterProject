import re
import os
import util
import parser

# ****************************** MAIN FUNCTIONS ***********************************
# ---------------------------------------------------------------------------------


# -------- PREPROCESSING FUNCTION -------
# This function combines all other function togather to offer a straight workflow of
# preprocessing the input data.
# The only aug you need put is input_path of DBpedia file
#
#def preprocessing(input_path):
#    
#    # set output file path
#    self.root = os.getcwd()
#    output_path = os.path.join(self.root, "preprocessed/preprocessed_documents.txt")
#    d = os.path.dirname("preprocessed_documents.txt")
#    if not os.path.exists(d):
#        os.mkdir(d)
#
#    parse(input_path,os)
#    match()
#    classigy()

# =================********************=====================*************************



# ------------- PARSE FUNCTION -------------
# this program tries to parse the input text data in two parts: 1) url that describes the name of the entry. 2) long abstract content.
#
#
# input FORMAT DATA:
# The long_abstract_en.ttl file format is:
#
# <url> <url> "the long abstract of certain entry" @en
#
# The first two parts contains the url of the entry. Everything inside the quotation is text content. The last part indicates which language is writen in.
#
# Example:
# <http://dbpedia.org/resource/Animalia_(book)> <http://dbpedia.org/ontology/abstract> "Animalia is an illustrated children's book by Graeme Base. It was originally published in 1986, followed by a tenth anniversary edition in 1996, and a 25th anniversary edition in 2012. Over three million copies have been sold.   A special numbered and signed anniversary edition was also published in 1996, with an embossed gold jacket."@en
#
# OUTPUT FORMAT:
# the result format is like this:
#
# <url> + '\t' + content + '\n'
#   ^
# name
#
# LOG:
# 1. output data contains some corner cases (not splited well)
# 2. we have optimize the sperator
#
# AUGS:
# Two augs are: input_file_path, output_file_path(including file name)
# you can leave output_file_path blank. The function will generate a output file under the preprocessing.py directory, named 'parse_output.py'


def parse(input_path,
          output_path = os.path.join(os.getcwd(),"parse_out/parse_output.txt")):
        
    # load file
    input = open(input_path, "r")
    # check the path
    d = os.path.dirname(output_path)
    if not os.path.exists(d):
        os.mkdir(d)
    output = open(output_path, "w")

    # loop
    for line in input:
        if line[0] == "#":  # get rid of comments
            continue

        fractions = line.split("\"@")[0].split("> ")
        entry_name = fractions[0].rstrip()[1:]
        content = fractions[2].lower()
        
        if content > 0:
            output.write(entry_name + '\t' + content + '\n')
    
    input.close()
    output.close()
    
# Parser using standford parser. This parser can generate tokenizer with gammaratic label
# input FORMAT:
# label + tab +  content

def stdparse(input_path, output_path = os.path.join(os.getcwd(),"parse_out/parse_output.txt")):
    
    # load file
    input = open(input_path, "r")
    # check the path
    d = os.path.dirname(output_path)
    if not os.path.exists(d):
        os.mkdir(d)
    output = open(output_path, "w")       

    # loop 
    for line in input:
        p = parser.parser()
        fractions = line.split("\t")
        label = fractions[0].rstrip().lower()
        content = fractions[1].lower()
        tokens = p.parse(content)
        output.write(label + '\t' + tokens)

    output.close()
    input.close()

# ------------- MATCH FUNCTION ----------
# this program tries to match each entry in the input data to a catagory in the class_source data.
#
# input FORMAT:
# the url_longAbstract format is:
#
# url_entry + tab + "long abstract.
#
# Example:
# http://dbpedia.org/resource/Animalia_(book)     "animalia is an illustrated children's book by graeme base. it was originally published in 1986, followed by a tenth anniversary edition in 1996, and a 25th anniversary edition in 2012. over three million copies have been sold.   a special numbered and signed anniversary edition was also published in 1996, with an embossed gold jacket.

# the first part is entry name, the second part is content starting with a '\"', ending with '.'
#
# SOURCE FILE FORMAT:
# the instance_types_en.ttl format is:
#
# <url_entry> <url> <url_class> .
#
# Example:
# <http://dbpedia.org/resource/BDSM> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Thing> .

# OUTPUT FORMAT:
# the output file class_longAbstract format is :
#
# class_name + tab + longAbstract
#
# LOG:
# 1. there exists some corner case in the input file (not parsed well in parse.py, some special case). we just ignore them.
# 2. number of output data points reach over 3 million, which is enough for us to get rid of special cases
# 3. output data points: 3371827
# 4. input data points: 4641890
#
# AUGS:
# Three augs are input_file_path, output_file_path and source_path(including file name)
# You can leave all augs blank, the function will use default ones.
#

def match(input_path = os.path.join(os.getcwd(),"parse_out/parse_output.txt"),
          output_path = os.path.join(os.getcwd(),"match_output/match_output.txt"),
          source_path = os.path.join(os.getcwd(),"source/instance_types_en.ttl")):

    # load files
    input = open(input_path, "r")
    d = os.path.dirname(output_path)
    if not os.path.exists(d):
        os.mkdir(d)
    output = open(output_path, "w")
    class_dicts = util.loadSource(source_path)
    
    # loop
    for line in input:
        if len(line) == 0:
            continue
        
        fractions = line.rstrip().split('\t')
        entry = fractions[0].split("/")[-1]
        
        if len(fractions) == 1:
            continue
                
        content = fractions[1]
        
        if class_dicts.has_key(entry):
            class_blg = class_dicts[entry]
        else:
            continue
        output.write(class_blg.lower() + '\t' + content +'\n')

    output.close()
    input.close()



# --------------- CLASSIFY FUNCTION ---------------
# this program tries to create a file for each class, which contains all the entries in this catagory.
#
# input FORMAT:
# class_name + '\t' + longAbstract
#
# OUTPUT FORMAT:
# subclass_name + '\t' + longAbstract
#
# LOG:
# 1. create a bunch of file
# 2. contain no invalid file
# 3. should add a module to extract sepcific subclass that I want.
#
# THE MODULE:
# the module is designing for extracting all entries of the subclass you want. it creates a file with name
# subclassName_longAbstracts.txt. the format is as same as above one.
#
# AUGS:
# The function has two augs: input_path(including file name) and subclass_youWant. You can leave both blank. The function will use the default ones.
# The output is default. If you specify subclass_youWant, the output will be a single file under the default directory: "{}_longAbstracts/{}_longAbstracts.txt". If you don't specify any subclass, you will get a directory containing all subclass files.


def classify(subclass_youWant = "",
             input_path = os.path.join(os.getcwd(),"match_output/match_output.txt")):
    
    input = open(input_path, "r")
    classes = {}
    all_class = set()
    
    # two situations
    # 1. no specified subclass, classify everything subclass
    # 2. classify the specified subclass
    
    # situation 1
    if len(subclass_youWant) == 0:
        # scan loop
        for line in input:
            if len(line) == 0:
                continue
            fractions = line.rstrip().split('\t')
            class_blg = fractions[0]
            content = fractions[1]

            if class_blg not in all_class:
                all_class.add(class_blg)
    
            classes[content] = class_blg

        # output loop
        for class_blg in all_class:
            output_path = "subclasses_longAbstracts/{}_longAbstracts.txt".format(class_blg)
            d = os.path.dirname(output_path)
            if not os.path.exists(d):
                os.mkdir(d)
            f = open(output_path, "w")
            for content in classes.keys():
                if classes[content] == class_blg:
                    f.write(class_blg + '\t' + content +'\n')
            f.close()
    
    # situation 2
    else:
        # scan loop
        for line in input:
            if len(line) == 0:
                continue
            fractions = line.rstrip().split('\t')
            class_blg = fractions[0]
            content = fractions[1]
            if class_blg == subclass_youWant:
                classes[content] = class_blg
            else:
                continue
        
        # output
        output_path = "{}_longAbstracts/{}_longAbstracts.txt".format(subclass_youWant, subclass_youWant)
        d = os.path.dirname(output_path)
        if not os.path.exists(d):
            os.mkdir(d)
        f = open(output_path,"w")
        for content in classes.keys():
            f.write(subclass_youWant + '\t' + content +'\n')
        f.close()



# ------------- REMOVE_STOP_WORDS FUNCTION -------------
# this program tries to remove all the stop words in the chosen documents
#
# input FORMAT:
# subclass + '\t' + longAbstract
#
# OUTPUT FORMAT:
# subclass + '\t' + content_without_words
#
# LOGS:
# 1. in the content, there are plenty of punctuations such as paranthese, comma...
#       we need to strip all of them
# 2. keep the numbers in the clean content
# 3. this program is general to all subclass file
#
# AUGS:
# The function has three augs, input_path, output_path and source_path (including file name)
# The later two can be left as blank
#

def rmStopWords(input_path,
                output_path = os.path.join(os.getcwd(), "stopwords_removed/reuslt.txt"),
                source_path = os.path.join(os.getcwd(), "source/english_stop.txt")):
    # load files
    input = open(input_path, "r")
    d = os.path.dirname(output_path)
    if not os.path.exists(d):
        os.mkdir(d)
    output = open(output_path, "w")
    stopWords = util.loadStopWords(source_path)

    # the loop
    for line in input:
        if len(line) == 0:
            continue
        fractions = line.rstrip().split('\t')
        subclass = fractions[0]
        content = fractions[1][1:]
        words = re.sub('\W+', " ", content).rstrip().split(" ")
        cleanContent = []
        for word in words:
            if word not in stopWords:
                cleanContent.append(word)
        output.write(subclass + '\t' + " ".join(cleanContent) + '\n')
    input.close()
    output.close()


# --------- STATISTICS FUNCTION ---------
# this program tries to obtain the statistic of all/a certain subclass.
#
# input FORMAT:
# class + '\t' + longAbstract
#
# OUTPUT FORMAT:
# class + '\t' + statistics
#
# LOG:
# 1. create two file: one is tsv, one is txt
#
# Augs:
# input_path need contain file name, but output mustn't contain file name

def get_statistics(input_path = os.path.join(os.getcwd(),"match_output/match_output.txt")):

    output_path = os.path.join(os.getcwd(),"statistic")
    txtFile = "class_statistic.txt"
    tsvFile = "class_statistic_es.tsv"
    
    input = open(input_path, "r")
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    output_txt = open(os.path.join(output_path,txtFile),"w")
    output_tsv = open(os.path.join(output_path,tsvFile),"w")

    # initialize parameter
    num_lines = {}
    whole_len = {}
    all_class = set()

    # loop
    for line in input:
    
        if len(line) == 0:
            continue

        fractions = line.rstrip().split('\t')
        class_blg = fractions[0]
        content = fractions[1][1:]
        words = content.split(" ")

        # collect statistics
        if class_blg not in all_class:
            all_class.add(class_blg)
            num_lines[class_blg] = 1
            whole_len[class_blg] = len(words)
        else:
            num_lines[class_blg] += 1
            whole_len[class_blg] += len(words)


        # set format for output
    output_tsv.write("Name" + '\t' + "num of lines" + '\t' + "length" + '\t' + "AvgLength" + '\n')

    # write output file
    for class_blg in all_class:
        length = whole_len[class_blg]
        numLines = num_lines[class_blg]
        output_txt.write(class_blg + '\t' + "Number of lines: " + str(numLines) + '\t' + "Length: " + str(length) + '\t' + "AvgLength: " + str(length/numLines) + '\n')
        output_tsv.write(class_blg + '\t' + str(numLines) + '\t' + str(length) + '\t' + str(length/numLines) + '\n')

    input.close()
    output_txt.close()
    output_tsv.close()


