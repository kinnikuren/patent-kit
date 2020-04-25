# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:51:49 2020

@author: alanyliu
"""
import file_reader as fr
import pytesseractest as pytess

import pytesseract
import pickle
import csv
import re
import nltk
from docx import Document
import sys


def main():
    """
    filepath = fr.get_filepath()
    print(filepath)

    images = fr.convert_pdf_to_images(filepath,300)
    """
    
    """
    filehandler = open('images.p', 'rb')
    images = pickle.load(filehandler)
    
    #print(pytesseract.image_to_string(images[0]))
    print(pytesseract.image_to_data(images[0]))
    """

    
    """
    ocr_dict = pytess.convert_images_to_string(images)
    
    filehandler = open('ocr_dict.p','wb')
    pickle.dump(ocr_dict, filehandler)
    
    print(ocr_dict)
    """
    
    #output_path = fr.convert_pdf_to_txt(filepath)
    
    #print(output_path)
    
    csv_dict = {}
    
    ref_numerals_set = set()
    
    ref_numerals_dict = {}


    with open('test.csv', newline='', encoding='utf-8-sig') as csvfile:
        
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            
            ref_numerals_set.add(row[1])
            
            #if page not in dict
            if row[0] not in csv_dict.keys():
                csv_dict[row[0]] = {}
            
            if row[1] not in csv_dict[row[0]].keys():
                csv_dict[row[0]][row[1]] = None
            
            if row[1] not in ref_numerals_dict.keys():
                ref_numerals_dict[row[1]] = None
            
            #print(', '.join(row))
       
    print(csv_dict)
    
    #sys.exit()
        
    raw_text = fr.get_string_from_txt('testapp.txt')
    
    words = nltk.word_tokenize(raw_text)
    
    

    
    no_count = 0
    
    previously_illustrated_ref_numerals = set()
    
    output_list = [] 
    output_list.append(["Page No", "Ref Numeral", "Found?", "Element", "Previously Illustrated?"])
    
    for page, ref_numerals in csv_dict.items():
        for ref_numeral in ref_numerals.keys():
            
            previously_illustrated = False
            if ref_numeral not in previously_illustrated_ref_numerals:
                previously_illustrated_ref_numerals.add(ref_numeral)
            else:
                previously_illustrated = True
                
            
            regex = "\s\w+\s\w+\s\w+\s\w+\s" + ref_numeral
            print(regex)
            x = re.search(regex, raw_text)
            element = None
            is_found = ""
            if x:
                #print(x.group(0))
                words = nltk.word_tokenize(x.group(0))
                #print(words)
                pos_tagged_words = nltk.pos_tag(words)
                print(pos_tagged_words)
                
                element = []
                for i in range(len(pos_tagged_words)-2,-1,-1):
                    if pos_tagged_words[i][1] not in ["TO", "CC", "VBP", "DT"]:
                        element.append(pos_tagged_words[i][0])
                    elif pos_tagged_words[i][1] == "DT":
                        element.append(pos_tagged_words[i][0])
                        break
                    else:
                        break
                    
                    #print(words[i])
                element.reverse()
                print(element)
                
                ref_numerals[ref_numeral] = "Yes"
                is_found = "Yes"
            else:
                ref_numerals[ref_numeral] = "No"
                is_found = "No"
                no_count += 1
                
            if element != None:
                element = ' '.join(element)
                
            output_list.append([page, ref_numeral, is_found, element, previously_illustrated])
    
    print(csv_dict)
    print(output_list)
    
    print("no count: " + str(no_count))
    
    with open('analyzed_drawings.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        for row in output_list:
            writer.writerow(row)
        
        
    #print(ref_numerals_set)
    #print(len(ref_numerals_set))
    
       
    #find all paragraphs
    regex = "(\[\d{1,10}\])(.+)"
    
    all_paragraphs = re.findall(regex, raw_text)
    print(all_paragraphs)
    
    para_dict = {}
    
    for para in all_paragraphs:
        pass
    
    
    #print(ref_numerals_dict)
    
    ref_numeral_breakdown = []
    
    for ref_numeral in sorted(ref_numerals_dict.keys()):
        print(ref_numeral)
        for para in all_paragraphs:
            regex = "\s\w+\s\w+\s\w+\s\w+\s" + ref_numeral
            
            results = re.findall(regex, para[1])
            if len(results) > 0:
                print(results)
                corresponding_paragraph = para[0]
                print(corresponding_paragraph)
                
            for result in results:
                words = nltk.word_tokenize(result)
                #print(words)
                pos_tagged_words = nltk.pos_tag(words)
                
                element = []
                for i in range(len(pos_tagged_words)-1,-1,-1):
                    if pos_tagged_words[i][1] not in ["TO", "CC", "VBP", "DT"]:
                        element.append(pos_tagged_words[i][0])
                    elif pos_tagged_words[i][1] == "DT":
                        element.append(pos_tagged_words[i][0])
                        break
                    else:
                        break
                    
                    #print(words[i])
                element.reverse()
                if element != None:
                    element = ' '.join(element)
                ref_numeral_breakdown.append([ref_numeral, element, corresponding_paragraph])

            
    print(ref_numeral_breakdown)
    
    with open('analyzed_ref_numerals.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        for row in ref_numeral_breakdown:
            writer.writerow(row)
    
    """
    document = Document('11-09-AY7072US-order.docx')
    count = 1
    for p in document.paragraphs:
        #print(count)
        print(p.text)
        print(count)
        count += 1
    """
        
        

#nltk.download('averaged_perceptron_tagger')
main()