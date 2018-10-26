# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 19:40:41 2018

@author: alanyliu
"""
import re
from pdf2image import convert_from_path, convert_from_bytes
import pytesseractest as pytess

import file_reader
import file_writer
import pk_nltk

class OfficeAction:
    rejections = []
    
    #def __init__(self):

class Rejection:
    def __init__(self):
        self.raw_text = ''
        self.claims = []
        self.references = {}
        self.claims_refs = {}
        self.rejectionType = ''
        self.rejectionText = ''

def findRejections(oa):
    neg_lookbehind = '(?<!U\.S\.C)'
    #doesn't work
    #regex = r'(Claim.+rejected\sunder.{1,10}as.+\.)'
    #regex = r'(Claim.+rejected\sunder.+35\sU\.S\.C\..+\n{0,2}.+(?<![PGPub|al])\.)'
    regex = r'(Claim.+rejected\sunder.+35\sU\.S\.C\..+\.\n\n)'
    regex = r'\.\n\n'
    #regex = r'U\.S\.C\.'
    #regex = r'(under.+as.+\w\.)'
    #regex = r'as'
    #regex = r'\.'
    list = re.findall(regex,oa,re.M)
    
    if len(list) > 0:
        #print(list[0])
        #print(type(list[0]))
        print(list)
    else:
        print('list is empty')
    print(len(list))

def rename_pdf_to_txt(pdf_file_name):
    txt_file_name = pdf_file_name.replace('.pdf','.txt')
    return txt_file_name

def convert_pdf_to_images(filename):

    print('converting pdf to images...')
    images = convert_from_path(filename,dpi=200)
    print('done converting pdf to images!')
    
    return images

def convert_pdf_to_txt(pdf_file_name):
    output_text_file = rename_pdf_to_txt(pdf_file_name)
    output_folder = "output/"
    output_path = output_folder + output_text_file
    
    images = convert_pdf_to_images(pdf_file_name)
    
    raw_string = pytess.convertImagesToString(images)
    
    file_writer.printStringToTxt(raw_string,output_path)
    
    return output_path

def clean_oa(raw_oa):
    regex = r'(Application/Control.+,\d{3})|(Page.+\d{1,2})|(Art Unit.+\d{4})'
    list = re.findall(regex,raw_oa,re.M)

    print(list)
    
    (clean_oa, numsubs) = re.subn(regex, '', raw_oa)
    
    #print(clean_oa)
    #print(numsubs)
    
    return clean_oa, numsubs

def find_rejections(oa_sentences):
    rej_sentences = []
    regex_three_digits = re.compile(r'\d{3}')
    regex_ref_no = re.compile(r'\d{1}')
    
    for s in oa_sentences:
        rej_sentence = ''
        count = 0
        is_rejected = False
        is_usc = False
        found_section = False
        ref_list = []
        
        for i in range(len(s)):
            rej_sentence += s[i] + ' '
            section_index = 0
            
            if s[i] == 'rejected':
                count+=1
                is_rejected = True
            if s[i] == 'U.S.C' and is_rejected:
                count+=1
                is_usc = True
            if re.match(regex_three_digits,s[i]) and (len(s[i]) == 3) and is_usc:
                code_section = s[i]
                found_section = True
                section_index = i
            if found_section and (i > section_index):
                digit_list = re.findall(regex_ref_no,s[i])
                #print(digit_list)
                if (len(digit_list) > 6):
                    ref_list.append("".join(digit_list))
        if count >= 2:
            #print(s)
            print(rej_sentence + '\n')
            print(code_section + '\n')
            print(ref_list)
            rej_sentences.append(rej_sentence)
            #pass
        #print(s)

def get_test_string():
    return file_reader.get_string_from_txt(
            '2018-09-21 15694060 nonfinal rejection.txt')
    
        
def main():
    filename = ""
    invalid_input = True
    
    while invalid_input:
        user_input = input("Convert PDF (Y/N)?")

        if user_input.lower() == "y":
            user_input = input("Provide PDF filename:")
            filename = user_input            
            output_path = convert_pdf_to_txt(filename)
            
            invalid_input = False
        elif user_input.lower() == "n":
            filename = "test.pdf"
            output_path = "output/test.txt"
            invalid_input = False
        else:
            print("did not understand")
            invalid_input = True

    data = file_reader.getStringFromTxt(output_path)
    clean_data = data.replace('\n\n','\n')
    data_split_space = data.split('\n')
    print(clean_data)
    print(data_split_space)
    print(len(data_split_space))
    
    oa1 = OfficeAction()
    
    regex = r'.+Claim.+rejected\sunder.+'
    test = []

    for i in range(len(data_split_space)):
        temp = ''
        if re.match(regex, data_split_space[i]):
            rej = Rejection()
            for j in range(i,i+5):
                temp += ' ' + data_split_space[j]
                #print(data_split_space[j])
                if (data_split_space[j].strip().endswith('.')):
                    #print(data_split_space[j])
                    break
            #print(temp)
            test.append(temp)
            
            rej.rejectionText = temp
            
            matchObj = re.search(r'(Claim.+)(?:\s)(?:is|are)',temp)
            #matchObj = re.search(r'(Claim.+)(?:(\s(is|are)))',temp)
            print(type(matchObj))
            print(rej.claims_refs)
            if matchObj:
                #print(temp)
                #print('yes')
                print(matchObj.groups())
                print(matchObj.group(1))
                rej.claims_refs[matchObj.group(1)] = None
                rej.claims = matchObj.group(1)
            
            oa1.rejections.append(rej)

    
    #print(test)
    for r in oa1.rejections:
        print(r.rejectionText)
        print(r.claims_refs)
        print(r.claims)
            #print(data_split_space[i+1])
    #findRejections(data)
    
def test_main():
    oa = OfficeAction()
    
    classifier = pk_nltk.create_classifier()
    
    test_data = get_test_string()
    oa.raw_text = test_data
    #print(test_data)
    
    cleaned_oa, num_subs = clean_oa(test_data)
    
    oa_sentences = pk_nltk.segment_sentences(classifier, cleaned_oa)
    
    find_rejections(oa_sentences)
    
    #print(oa_sentences)
    
#main()
test_main()