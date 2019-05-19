# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 19:57:56 2018

@author: alanyliu
"""

import re
import pydot
import file_reader
import datetime
import docx
from docx.shared import Pt 

def add_original_identifier(claims_string_regex_list):
    list_with_original = []
    for i in range(len(claims_string_regex_list)):
        current_entry = claims_string_regex_list[i].strip()
        if i%2 != 0:
            current_entry += "\t(Original)  "
        list_with_original.append(current_entry)
    print(list_with_original)
    

def main():
    claims = {}
    filepath=""
    #filepath = '8836S-1189 claims.txt'
    #filepath = "cases/8054L-1152/8054L-1152 claims.txt"
    
    #Temp
    #filepath = "input/8836S_1317_claims.txt"
    
    filepath = file_reader.get_filepath()
    
    if (filepath.endswith(".txt") or filepath.endswith(".pdf")):    
        claims_string = file_reader.get_string_from_file(filepath).strip()
    elif (filepath.endswith(".docx")):
        claims_docx = docx.Document(filepath)
        style = claims_docx.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = Pt(12)
        
        for i in range(len(claims_docx.paragraphs)):
            p = claims_docx.paragraphs[i]
            
            #p.style = claims_docx.styles['Normal']
            p.style.font.name = 'Times New Roman'
            p.style.font.size = Pt(12)
            print(p.style.name)
            #print(i)
            print(p.text)
           
            claim_no_regex = r'([0-9]{1,2}\.)'
            #if(re.match(claim_no_regex,p.text)):
            line_split = re.split(claim_no_regex,p.text)
            if (len(line_split) > 1):
                print(line_split)
                line_split[1] += "\t(Original)  "
                claims_docx.paragraphs[i].text = line_split[1] + line_split[2].strip()
                print(claims_docx.paragraphs[i].text)
           
        #claims_docx.styles.style.__ParagraphStyle.font.size = Pt(14)
        claims_docx.save("output/test.docx")
        raise SystemExit("docx")
    else:
        print("Unsupported file format")
        raise SystemExit("Unsupported file format")
    
    list = re.findall(r'[0-9]{1,2}\..*',claims_string,re.M)
    list2 = re.split(r'([0-9]{1,2}\.)',claims_string)
    
    #print(list)
    #print(len(list))
    
    print(list2)
    
    list3 = add_original_identifier(list2)
    print(list3)
    
    for i in list:
        claimNo = re.match(r'[0-9]{1,2}',i).group(0)
        print(claimNo)
        #print(type(claimNo))
        #matchObj = re.search(r'claim [0-9]{1,2}',i,re.I)
        
        claims[claimNo] = []
    
        #regex to find dependent claims
        depClaimRegex = r'(claim) (\d+)'
        
        matchObj = re.search(depClaimRegex,i,re.I)
        if matchObj:
            parClaimStr = matchObj.group(0)
            
            #depClaimNo = re.sub(depClaimRegex, r'\1', i)
            parClaimNo = parClaimStr.lower().replace('claim ','')
            print('parent: ' + parClaimNo)
                    
            if parClaimNo in claims:
                claims[parClaimNo].append(claimNo)
            #depClaimNo = depClaimStr.replace()
            #print(matchObj.group(0))
            
        else:
            print('no match')
        
        
        #claims.update()
        
    
    print(claims)
    
    graph = pydot.Dot(graph_type='graph')
    
    for i in claims:
        print(i)
        # we can get right into action by "drawing" edges between the nodes in our graph
        # we do not need to CREATE nodes, but if you want to give them some custom style
        # then I would recomend you to do so... let's cover that later
        # the pydot.Edge() constructor receives two parameters, a source node and a destination
        # node, they are just strings like you can see
        node = pydot.Node(i)
        graph.add_node(node)
        for j in claims[i]:
            edge = pydot.Edge(i, j)
            graph.add_edge(edge)
        
        # and we obviosuly need to add the edge to our graph
    
    currentTime = str(datetime.datetime.now()).split('.')[0].replace('-','').replace(' ','').replace(':','')
    
    #filepath = '{}_{}.png'.format(filepath.replace('.txt',''),currentTime)    
    output_path = "output.png"
    graph.write_png(output_path)
    print("flowchart generated at {}...".format(output_path))
    
    #print(filereadtest.getStringFromTxt())
    
    #test2 ="ABC"
    #print(re.match(r'A',test2).group())
    
    #test.split
    
    #print("test")

main()