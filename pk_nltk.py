# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 17:12:19 2018

@author: alanyliu
"""
import nltk
import file_reader
import numpy as np
import re

#nltk.download('treebank')
#nltk.download()

#retrain classifier

class ClassifiedSentenceData:
    def __init__(self, sentences):
        self.tokens = []
        self.boundaries = set()
        self.offset = 0
        self.featuresets = []
        
        for sent in sentences:
            #print(sent)
            self.tokens.extend(sent)
            self.offset += len(sent)
            self.boundaries.add(self.offset-1)
            
        self.featuresets = [(punct_features(self.tokens, i), (i in self.boundaries))
                for i in range(1, len(self.tokens)-1)
                if self.tokens[i] in '.?!']

def create_classifier():
    sents = nltk.corpus.treebank_raw.sents()
    #sents is list of sentences, each sentence is list of words
    #print(sents)
    #print(type(nltk.corpus.treebank_raw))
    #print(type(sents))
    #4193 sentences
    #print(len(sents))
      
    #print(boundaries)
    
    #print(tokens[0:10])
    
    #featuresets is tuple (features, label)

    nltk_treebank_data = ClassifiedSentenceData(sents)
    
    my_data = create_labeled_set()
    #print(my_data.featuresets)
    
    combined_featuresets = nltk_treebank_data.featuresets + my_data.featuresets

    classifier_final = train_classifier(nltk_treebank_data.featuresets)

    
    print("NLTK Treebank:")
    classifier = train_classifier(nltk_treebank_data.featuresets)
    print("My Data:")
    classifier_final = train_classifier(my_data.featuresets)
    print("Both:")
    #nltk_treebank_data.featuresets.update(my_data.featuresets)
    classifier = train_classifier(combined_featuresets)
    
    np.random.shuffle(nltk_treebank_data.featuresets)
    np.random.shuffle(my_data.featuresets)
    np.random.shuffle(combined_featuresets)
    
    print("NLTK Treebank:")
    classifier = train_classifier(nltk_treebank_data.featuresets)
    print("My Data:")
    classifier = train_classifier(my_data.featuresets)
    print("Both:")
    #nltk_treebank_data.featuresets.update(my_data.featuresets)
    classifier = train_classifier(combined_featuresets)

    
    return classifier_final

def create_labeled_set():
    raw_text = file_reader.get_string_from_txt('training/train_1.txt')
    
    #print(raw_text)
    
    linebreak_split = raw_text.strip().split("\n")
    #print(linebreak_split)
    sents = []
    
    for l in linebreak_split:
        sent = nltk.word_tokenize(l)
        #print(sent)
        sents.append(sent)
        
    data = ClassifiedSentenceData(sents)
    #print(data.featuresets)
    #print(len(data.featuresets))
    
    return data
    

def train_classifier(featuresets):
    """
    print(tokens[0])
    print(tokens[1])
    
    for i in range(1,3):
        print(i)
    """
    
    #print(featuresets)
     	
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    accuracy = nltk.classify.accuracy(classifier, test_set)
    print("Accuracy: " + str(accuracy))
    
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
#create_classifier()

#create_labeled_set()

"""
test_list = list(range(10))
print(test_list)
np.random.shuffle(test_list)
print(test_list)
"""