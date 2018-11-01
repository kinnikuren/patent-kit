# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 19:57:56 2018

@author: alanyliu
"""

import re
import pydot
import filereadtest
import file_reader
import datetime


claims = {}
#filepath = '8836S-1189 claims.txt'
filepath = "cases/8054L-1152/8054L-1152 claims.txt"
claimsString = file_reader.get_string_from_txt(filepath)

list = re.findall(r'[0-9]{1,2}\..*$',claimsString,re.M)

print(list)
print(len(list))

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

filepath = '{}_{}.png'.format(filepath.replace('.txt',''),currentTime)    
graph.write_png(filepath)
print("flowchart generated...")

#print(filereadtest.getStringFromTxt())

#test2 ="ABC"
#print(re.match(r'A',test2).group())

#test.split

#print("test")