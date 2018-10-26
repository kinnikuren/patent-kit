# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 11:13:36 2018

@author: alanyliu
"""

import file_reader
import file_writer
import re

input_path = "training/2018-09-21 15694060 nonfinal rejection.txt"
text = file_reader.get_string_from_txt(input_path)

print(text)

text = re.sub(r'(]\.)','\g<1>\n',text)
text = re.sub(r'\n\s+\n','\n',text)
text = re.sub(r'\n{2,}','\n',text)
#print(re.findall(r'\w\n\w',text))
#print(re.findall(r'(\w)(\n)(\w)',text))
text = re.sub(r'(\w|,)(\n)(\w)','\g<1> \g<3>',text)
text = re.sub(r'(\.)\s','\g<1>\n',text)

file_writer.print_string_to_txt(text,"training/train.txt")


#punct-features ideas
#next word is punctuation
#last letter of previous word is capitalized
#probably doesn't end with acronym
#false positives, false negatives
#single double quotes

#claim interpretation