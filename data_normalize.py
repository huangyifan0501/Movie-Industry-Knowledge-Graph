import norm_utils
import utils
import numpy as np
import pandas as pd
from tqdm import tqdm

pd.options.mode.chained_assignment = None

graph = pd.read_csv('../graph/graph_base.csv')
relatives=pd.read_csv('../graph/relatives.csv')
total_number = graph.shape[0]

# normalize address
address_property=['birthPlace','deathPlace','nationality']
for p in address_property:
    pbar = tqdm(total=total_number)
    pbar.set_description(p)
    for i in range(len(graph[p])):
        pbar.update(1)
        carry=eval(graph[p][i])
        if len(carry)>=1:
            graph[p][i]=norm_utils.address_norm(carry[0])
        else:
            graph[p][i] = {}


# normalize time
time_property=['activeTime','debutTime']
for p in time_property:
    pbar = tqdm(total=total_number)
    pbar.set_description(p)
    for i in range(len(graph[p])):
        pbar.update(1)
        carry=graph[p][i]
        flag=1 if p=='debutTime' else 0
        graph[p][i] = norm_utils.time_norm(carry, flag)
        

# normalize name
name_property=['name','originalName','foreignName','nickname']
for p in name_property:
    pbar = tqdm(total=total_number)
    pbar.set_description(p)
    for i in range(len(graph[p])):
        pbar.update(1)
        carry=eval(graph[p][i])
        if len(carry)>=1:
            graph[p][i]=norm_utils.name_norm(carry[0])
        else:
            graph[p][i] = []
            

# normalize award
award_property=['award']
for p in award_property:
    pbar = tqdm(total=total_number)
    pbar.set_description(p)
    for i in range(len(graph[p])):
        pbar.update(1)
        carry=eval(graph[p][i])
        if len(carry)>=1:
            graph[p][i]=norm_utils.award_norm(carry[0])
        else:
            graph[p][i] = []
            

# normalize works
works_property=['notableWork','debutWork']
for p in works_property:
    pbar = tqdm(total=total_number)
    pbar.set_description(p)
    for i in range(len(graph[p])):
        pbar.update(1)
        carry=eval(graph[p][i])
        if len(carry)>=1:
            graph[p][i]=norm_utils.works_norm(carry[0])
        else:
            graph[p][i] = []
            
# add works property
graph['works'] = graph['notableWork'] + graph['debutWork']

graph['hasSibling'] = relatives['hasRelative']
graph['hasSpouse'] = relatives['hasSpouse']
graph['hasParent'] = relatives['hasParent']
graph['hasChild'] = relatives['hasChild']

graph.to_csv('../graph/graph.csv', encoding='utf_8_sig')
print('Normalize finished')