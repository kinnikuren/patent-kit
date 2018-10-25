# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 15:47:08 2018

@author: alanyliu
"""
import pdf2imagetest as p2i

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

#print(pytesseract.image_to_string(Image.open('claims.png')))

#print(pytesseract.image_to_string(Image.open('resumetest.png')))

#print(pytesseract.image_to_string(Image.open('example1_graph.png')))


#oa_string = pytesseract.image_to_string(Image.open('office_action_test.png'))

def convertImagesToString(images):
    whole_oa_string = ''
    count = 1

    print('converting images to string')
    for img in images:
        whole_oa_string += pytesseract.image_to_string(img)
        print("page {} converted".format(count))
        count += 1
    print('done converting to string')
    
    return whole_oa_string

def printStringToTxt(string,outputfilename):
    with open(outputfilename, "w") as text_file:
        print(string, file=text_file)
    
    print('done printing')

def testfunction():
    whole_oa_string = ''
    #test
    for i in range(1,12):
        print(i)
        whole_oa_string += pytesseract.image_to_string(Image.open('output2/out_{}.jpg'.format(i)))
    #print(oa_string)
    
    #print(whole_oa_string)
    
    with open("Output.txt", "w") as text_file:
        print(whole_oa_string, file=text_file)
    
        
    print('done printing')

def main():
    filename = '2018-09-26 15332415 final rejection.pdf'
    images = p2i.convertPdfToImages(filename)

    #for img in images:
        
    print(pytesseract.image_to_string(images[0]))
    
    data = convertImagesToString(images)
    
    printStringToTxt(data,'Output2.txt')
    
