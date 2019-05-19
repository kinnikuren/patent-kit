# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 00:00:38 2018

@author: alanyliu
"""
from pdf2image import convert_from_path, convert_from_bytes
import pytesseractest as pytess

from tkinter import filedialog
from tkinter import *

import file_writer
 
#print(data)
#print(type(data))
  
def get_string_from_txt(txt_file_name):
    with open(txt_file_name, 'r', encoding="ansi") as myfile:
        data = myfile.read()
    return data

def rename_pdf_to_txt(pdf_file_name):
    txt_file_name = pdf_file_name.replace('.pdf','.txt')
    return txt_file_name

def convert_pdf_to_images(filename):

    print('converting {} to images...'.format(filename))
    images = convert_from_path(filename,dpi=500)
    for image in images:
        image.save('out.jpg', 'JPEG')
    print('done converting pdf to images!')
    
    return images

def convert_pdf_to_txt(pdf_file_path):
    output_path = rename_pdf_to_txt(pdf_file_path)
    #output_folder = "output/"
    #output_path = output_folder + output_text_file
    
    images = convert_pdf_to_images(pdf_file_path)
    
    raw_string = pytess.convertImagesToString(images)
    
    file_writer.print_string_to_txt(raw_string,output_path)
    
    return output_path

def get_filepath(filepath=""):
    if (filepath == ""):
        #get data
        #filepath = input("provide file path (pdf or raw txt):")
        root = Tk()
        #specifies initial dir
        #initialdir = "/",
        root.filename =  filedialog.askopenfilename(
                title = "Select file",
                filetypes = (
                        ("pdf files","*.pdf"),
                        ("txt files","*.txt"),
                        ("docx files","*.docx"),
                        ("all files","*.*")))
        print(root.filename)
        filepath = root.filename
        root.destroy()
        
    return filepath
    

def get_string_from_file(filepath = ""):
    #data = get_test_string()
    
    if (filepath.endswith("pdf")):
        txt_path = convert_pdf_to_txt(filepath)
    else:
        txt_path = filepath
    
    return get_string_from_txt(txt_path)
       
    #temporary    
    #txt_path = "cases/8071-762/2018-10-10 15337185 nonfinal rejection.txt"