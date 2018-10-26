# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 17:12:19 2018

@author: alanyliu
"""
import nltk
import file_reader
import re

#nltk.download('treebank')
#nltk.download()

#retrain classifier

def create_classifier():
    sents = nltk.corpus.treebank_raw.sents()
    tokens = []
    boundaries = set()
    offset = 0
    
    #print(sents)
    #print(type(nltk.corpus.treebank_raw))
    #print(type(sents))
    
    for sent in sents:
        tokens.extend(sent)
        offset += len(sent)
        boundaries.add(offset-1)
    
    print(tokens[0:10])
    
    featuresets = [(punct_features(tokens, i), (i in boundaries))
                    for i in range(1, len(tokens)-1)
                    if tokens[i] in '.?!']
    
     	
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    accuracy = nltk.classify.accuracy(classifier, test_set)
    print(accuracy)
    
    return classifier
    
def segment_sentences(classifier, one_string):
    words = nltk.tokenize.word_tokenize(one_string)
    
    start = 0
    sents = []
    for i, word in enumerate(words):
        if word in '.?!' and classifier.classify(punct_features(words, i)) == True:
            sents.append(words[start:i+1])
            start = i+1
    if start < len(words):
        sents.append(words[start:])
    return sents

def sentence_seg(data):
    classifier = create_classifier()
    
    #data = file_reader.getStringFromTxt('2018-09-21 15694060 nonfinal rejection.txt')
    words = nltk.tokenize.word_tokenize(data)
    
    temp_string = ''
    for w in words:
        temp_string += w + '\n'
    file_writer.printStringToTxt(temp_string,'mushedwords.txt')

    sents_new = segment_sentences(classifier, words)    

    #check_classifier(classifier, words)


def check_classifier(classifier, words):
    for i in range(len(words)):
        if words[i] in '.?!':
            temp_sentence = ''
            for j in range(10,-1,-1):
                temp_sentence += words[i-j] + ' '
            print(classifier.classify(punct_features(words, i)))
            print(temp_sentence + '\n')
            

def punct_features(tokens, i):
    features = {'prev-word': tokens[i-1].lower(),
                'punct': tokens[i]
                #'prev-word-is-one-char': len(tokens[i-1]) == 1
                }
    if i+1 >= len(tokens):
        features['next-word-capitalized-or-none'] = True
    else:
        #print(i)
        #print(len(tokens))
        features['next-word-capitalized-or-none'] = tokens[i+1][0].isupper()
    return features

"""
def ref_features(word):
    return {'has-numbers', 
            'length': len(word)}
"""

def tokenize_test():
    data = file_reader.getStringFromTxt('2018-09-21 15694060 nonfinal rejection.txt')
    #print(data)
    words = nltk.tokenize.word_tokenize(data)
    #print(words)


def main():
    filename = '2018-09-21 15694060 nonfinal rejection.txt'
    #tokenize_test()
    #sentence_seg()
   
    data = file_reader.getStringFromTxt(filename)
    clean_oa, numsubs = clean_OA(data)
   
    sentence_seg(clean_oa)

    
#main()