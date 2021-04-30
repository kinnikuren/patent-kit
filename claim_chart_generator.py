# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 19:57:56 2018

@author: alanyliu
"""

import os
import re
import pydot
import datetime
import docx
from docx.shared import Pt 

def remove_tabs(claims_string):
    #remove initial tabs
    claims_string_linebreak_split = claims_string.split('\n')
    removed_tab_list = []
    for line in claims_string_linebreak_split:
        #print(line.strip())
        removed_tab_list.append(line.strip())
    new_claims_string = '\n'.join(removed_tab_list)
    print('tabs removed:')
    print(new_claims_string)   

    return new_claims_string

def create_claims_dict(claims_string):
    claims_string = remove_tabs(claims_string)                                                     
    claims_dict = {}

    claims_list = re.findall(r'[0-9]{1,2}\..*',claims_string,re.M)
    
    print('\nFINDALL results:')
    print(claims_list)
    print('\n\n')


    for i in claims_list:
        claimNo = re.search(r'[0-9]{1,2}',i).group(0)
        print('CLAIM ' + claimNo)
        #print(type(claimNo))
        #matchObj = re.search(r'claim [0-9]{1,2}',i,re.I)
        
        claims_dict[claimNo] = []
    
        #regex to find dependent claims
        depClaimRegex = r'(claim) (\d+)'
        
        matchObj = re.search(depClaimRegex,i,re.I)
        if matchObj:
            parClaimStr = matchObj.group(0)
            
            #depClaimNo = re.sub(depClaimRegex, r'\1', i)
            parClaimNo = parClaimStr.lower().replace('claim ','')
            print('parent: ' + parClaimNo)
                    
            if parClaimNo in claims_dict:
                claims_dict[parClaimNo].append(claimNo)
                print('added dependent claim {} to parent claim {}'.format(claimNo, parClaimNo))
            #depClaimNo = depClaimStr.replace()
            #print(matchObj.group(0))
                print(claims_dict)
            
        else:
            print('no match')
        
        
        #claims.update()
    
    return claims_dict

def generate_claim_chart(claims_dict, filepath="./"):
    graph = pydot.Dot(graph_type='graph')
    location = os.path.dirname(filepath)

    for i in claims_dict:
        #print(i)
        # we can get right into action by "drawing" edges between the nodes in our graph
        # we do not need to CREATE nodes, but if you want to give them some custom style
        # then I would recomend you to do so... let's cover that later
        # the pydot.Edge() constructor receives two parameters, a source node and a destination
        # node, they are just strings like you can see
        node = pydot.Node(i)
        graph.add_node(node)
        for j in claims_dict[i]:
            edge = pydot.Edge(i, j)
            graph.add_edge(edge)
        
        # and we obviosuly need to add the edge to our graph
    
    #currentTime = str(datetime.datetime.now()).split('.')[0].replace('-','').replace(' ','').replace(':','')
    
    #filepath = '{}_{}.png'.format(filepath.replace('.txt',''),currentTime)    
    #output_path = location + "claim_chart.png"
    output_path = location + "/static/output/claim_chart.png"
    graph.write_png(output_path)
    print("flowchart generated at {}...".format(output_path))
