# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 16:11:08 2018

@author: alanyliu
"""
import re
import nltk
import csv
import numpy as np
import docx
import io

import file_reader
import file_writer
import pk_nltk


"""
features of reference numerals
all caps
starts with cap
all numbers / percent that is a digit
has underscore
combination letters and numbers
length
itself?
"""
def ref_numeral_features(token):
    """
    features = {'length': len(token),
                'has-underscore': "_" in token,
                #these two are related, might be a problem
                'starts-with-cap': token[0].isupper(),
                'all-caps': sum([0 if i.isupper() else 1 for i in token]) == 0}
    """
    features = {'length': len(token)}
    
    has_all_numbers = False
    try:
        int(token)
        #features['all-numbers'] = True
        has_all_numbers = True
    except ValueError:
        #features['all-numbers'] = False
        has_all_numbers = False
        
    probably_ref_numeral = False
        
    if sum([0 if i.isupper() else 1 for i in token]) == 0:
        probably_ref_numeral = True
    elif token[0].isupper():
        probably_ref_numeral = True   
    elif ("_" in token):
        probably_ref_numeral = True
    elif has_all_numbers:
        if token[0] != "0":
            probably_ref_numeral = True             
    
    """ maybe not so helpful
    elif token[0].isupper():
        probably_ref_numeral = True
    """
    
    features['probably-ref-numeral'] = probably_ref_numeral
        
    return features
    

def test_main():
    #only detailed description
    raw_text = file_reader.get_string_from_txt('test.test')
    
    words = nltk.word_tokenize(raw_text)
    
    file_writer.print_string_to_txt("|\n".join(words),'words.test')

    
    regex_all_num = re.compile(r'\d+',re.M)
    
    ref_numerals = []
    
    for i, w in enumerate(words):
        matchObj = re.fullmatch(regex_all_num,w)
        if matchObj:
            #print(matchObj.group(0))
            ref_numerals.append((w,i))
            print(ref_numeral_features(w))
            
    #print(ref_numerals)

test_main()

#print(ref_numeral_features("111"))
#print(int("11x"))


def get_featuresets():
    #read csv of labeled data
    #create list of feature sets with labels
    #test_2 = np.genfromtxt(io.StringIO('test.csv'), delimiter='|', names=True)
    data = []
    featuresets = []
    count = 0
    with open('test.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')
        print(type(csvreader))
        for row in csvreader:
            #print(row)
            featureset = ref_numeral_features(row[0])
            label = False
            if row[1] == "1":
                label = True
                count += 1
            else:
                label = False
            row[1] = label
            
            featuresets.append((featureset,label))
            data.append(row)
            #print(', '.join(row))
            #print(type(row))
            
    print(data)
    print(featuresets)
    return featuresets

def get_trained_classifier():
    featuresets = get_featuresets()
    
    #randomize data
    np.random.shuffle(featuresets)
    classifier = pk_nltk.train_classifier(featuresets)
    
    return classifier

classifier = get_trained_classifier()

#read app in .txt to string
raw_text = file_reader.get_string_from_txt('1225.txt')

#tokenize raw text
words = nltk.word_tokenize(raw_text)

test_set = set()

new_dataset = []

for w in words:
    #print(w)
    #print(classifier.classify(ref_numeral_features(w)))
    
    new_dataset.append((w,classifier.classify(ref_numeral_features(w))))
    if (classifier.classify(ref_numeral_features(w))):
        #print(w)
        test_set.add(w)
        
#print(test_set)
   
print(new_dataset)
#print(classifier.classify(ref_numeral_features("Since")))

#print(test_2)
#print(len(test_2))

