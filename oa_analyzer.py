# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 19:40:41 2018

@author: alanyliu
"""
import re

import file_reader
import file_writer
import pdf2imagetest as p2i
import pytesseractest as pytess


class OfficeAction:
    rejections = []
    
    #def __init__(self):

class Rejection:
    def __init__(self):
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


        
def main():
    filename = '2018-09-21 15694060 nonfinal rejection.pdf'
    outfilename = filename.replace('.pdf','.txt')
    images = p2i.convertPdfToImages(filename)
    
    rawdata = pytess.convertImagesToString(images)
    
    file_writer.printStringToTxt(rawdata,outfilename)

    data = file_reader.getStringFromTxt(outfilename)
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
    
main()