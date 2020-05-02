# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 00:00:38 2018

@author: alanyliu
"""
from pdf2image import convert_from_path, convert_from_bytes
import pickle
from docx import Document
from docx.shared import Inches

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

def convert_pdf_to_images(filename,dpi=500,output_files=False,generate_pickle=False):

    print('converting {} to images at {} dpi...'.format(filename, dpi))
    images = convert_from_path(filename,dpi=dpi)
    document = Document()

    if output_files:
        for i in range(len(images)):
            output_file_name = 'output/out' + str(i+1) + '.jpg'
            
            if output_files:
                print('converting page ' + str(i+1) + ' and outputting as ' + output_file_name)
                images[i].save(output_file_name, 'JPEG')
            
                document.add_picture(output_file_name,width=Inches(6))
                document.add_page_break()
    
        document.save("drawings.docx")
    print('done converting pdf to {} images!'.format(len(images)))
    
    if generate_pickle:
        print('saving images to images.p')
        filehandler = open('images.p','wb')
        pickle.dump(images, filehandler)
    else:
        print("pickle not generated")
    
    return images

def convert_pdf_to_txt(pdf_file_path,use_pickle=True):
    output_path = rename_pdf_to_txt(pdf_file_path)
    #output_folder = "output/"
    #output_path = output_folder + output_text_file
    
    if use_pickle:
        filehandler = open('images.p', 'r')
        images = pickle.load(filehandler)
    else:
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
    
def get_folder(filepath):
    slash_split = re.split(r'(\/)',filepath)
    print(slash_split)
    
    folder = "".join(slash_split[0:len(slash_split)-1])
    
    print(folder)
    return folder
    

def main():
    filepath = get_filepath()
    print(filepath)
    
    get_folder(filepath)

    #convert_pdf_to_images(filepath,200,True)


#main()

#temp
#convert_pdf_to_images("LO-290903-US(DRAWINGS).pdf",200)
