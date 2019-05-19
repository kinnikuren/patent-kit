# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:49:09 2019

@author: alanyliu
"""

import file_reader
import file_writer

import re

input_paragraphs_string = []
input_paragraphs = []
input_path = ""

#test
input_paragraphs_string = ["103 - 109","123-131","108","29","36", "98", "108", "108"]

for i in input_paragraphs_string:
    if i.isdigit():
        if int(i) not in input_paragraphs:
            input_paragraphs.append(int(i))
    else:
        range_hyphen_split = i.split("-")
        print(range_hyphen_split)
        start_para = range_hyphen_split[0].strip()
        end_para = range_hyphen_split[1].strip()
        for j in range(int(start_para), int(end_para)+1):
            if j not in input_paragraphs:
                input_paragraphs.append(j)

print(input_paragraphs)

#test
#input_paragraphs = [103,104,105,106,107,108,109,29]
input_path = "input/test_reference.txt"

input_paragraphs.sort()

reference_string = file_reader.get_string_from_txt(input_path)

#print(reference_string)
reference_split = reference_string.split("\n")
#print(reference_split)

output_string = []

for para in input_paragraphs:
    print(para)
    regex = r'\[\d+' + str(para) + r'\].+'
    match_obj = re.search(regex, reference_string)
    if (match_obj):
        print(match_obj[0])
        output_string.append(match_obj[0])
        
file_writer.print_string_to_txt("\n\n".join(output_string),"output/analyzed_reference.txt")
    
    