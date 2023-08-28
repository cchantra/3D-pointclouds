import glob
import os
import pandas as pd
import networkx as nx 
import gmatch4py as gm

import numpy as np

# Gmatch4py use networkx graph 

# import the GED using the munkres algorithm



import os
 
import gmatch4py as gm

num_ele = 20 



dfilename = 'HED_DISTANCE' 
 
ged = gm.HED(1,1,1,1) # all edit costs are equal to 1
 
#ged=gm.BP_2(1,1,1,1)
input_file = glob.glob('data/palm/p?.ply')+glob.glob('data/palm/p??.ply')
input_file = input_file[:-1]
output_file = []
for file in input_file:
    _,filename = os.path.split(file)
    
    outfile = os.path.join('pc2graph/data/batch',filename)
    output_file.append(outfile)
output_file = output_file[:-1]


G_list = []
 


#print(item_dict)



for file2 in  output_file[:num_ele]:
     
    path,fname =  os.path.split(file2)
    fname = fname.split('.')[0]
    G = nx.Graph()
    g_item = dict()
    g_item['name'] = fname
    with   open(file2) as f:

        for line in f.readlines():
            l = line.strip()
            l = l.split()
            n1,n2,w = float(l[0]), float(l[1]), float(l[2])
            #print(n1,n2,w)
            G.add_edge(n1,n2,weight=w)
            
    print('fname %s edges %d nodes %d'%(fname,len(G.edges()),len(G.nodes)))
    #print('nodes %d'%(len(G.nodes())))
    

    g_item['graph'] = G
     
    G_list.append(g_item)


compare_result = dict()

compare_result['label'] = []
compare_result['result'] = []


f = open(dfilename+'.npy','ab')
print(dfilename)

for i, g1 in enumerate(G_list):
     
    for j, g2 in enumerate(G_list):
        if i == j :
            continue
        G1 =g1['graph']
        G2 = g2['graph']
        
        cname = g1['name']+'_'+g2['name']
        print(cname)
        compare_result['label'].append(cname)
        result= ged.compare([G1,G2],None) 
        compare_result['result'].append(ged.distance(result))
         
        print(result)
        print(ged.distance(result))
        np.save(f,ged.distance(result))
    if i >1:
        break
        