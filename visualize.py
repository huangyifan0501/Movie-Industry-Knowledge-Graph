#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
from py2neo import Graph, Relationship,NodeMatcher, Subgraph
from py2neo.matching import *
import pandas as pd


# In[2]:


def place(place_type,dic,graph):
    b_place=dic[place_type]
    if b_place=={}:
        return
    if b_place['country']!='':
        graph.run("MERGE(p:Place:country{name:'%s'})"%b_place['country'])
        graph.run("MATCH(a:Person), (n:Place:country)                 WHERE a.name=['%s'] AND n.name='%s'                 MERGE(a)-[r:%s]->(n)" % (dic['name'][0],b_place['country'],place_type))
    if b_place['state']!='':
        graph.run("MERGE(p:Place:state{name:'%s'})"%b_place['state'])
        graph.run("MATCH(a:Place:state), (n:Place:country)                   WHERE a.name='%s' AND n.name='%s'                   MERGE(a)-[r:LocateIn]->(n)" % (b_place['state'], b_place['country']))
        graph.run("MATCH(a:Person), (n:Place:state)                 WHERE a.name=['%s'] AND n.name='%s'                 MERGE(a)-[r:%s]->(n)" % (dic['name'][0], b_place['state'],place_type))
    if b_place['city']!='':
        graph.run("MERGE(p:Place:city{name:'%s'})"%b_place['city'])
        graph.run("MATCH(a:Place:city), (n:Place:state)                   WHERE a.name='%s' AND n.name='%s'                   MERGE(a)-[r:LocateIn]->(n)" % (b_place['city'], b_place['state']))
        graph.run("MATCH(a:Person), (n:Place:city)                 WHERE a.name=['%s'] AND n.name='%s'                 MERGE(a)-[r:%s]->(n)" % (dic['name'][0], b_place['city'],place_type))
            
        


# In[3]:


def person(relation,dic,graph):
    person=dic[relation]
    for i in person:
        graph.run("MERGE(p:Person{name:['%s']})"%i)
        graph.run("MATCH(a:Person), (n:Person)                 WHERE a.name=['%s'] AND n.name=['%s']                 CREATE(a)-[r:%s]->(n)" % (dic['name'][0],i,relation))


# In[4]:


def works(relation,dic,graph):
    works=dic[relation]
    for i in works:
        graph.run("MERGE(p:Movie{name:'%s'})"%i)
        graph.run("MATCH(a:Person), (n:Movie)                 WHERE a.name=['%s'] AND n.name='%s'                 CREATE(a)-[r:%s]->(n)" % (dic['name'][0],i,relation))


# In[5]:


def works_n(dic,graph):
    dic_help={'actor':'act','director':'direct','screenwriter':'write'}
    keysss=['actor','director','screenwriter']
    works=dic['notableWork']+dic['debutWork']
    for i in keysss:
        if i in dic['type']:
            for j in works:
                graph.run("MATCH(a:Person), (n:Movie)                         WHERE a.name=['%s'] AND n.name='%s'                         CREATE(a)-[r:%s]->(n)" % (dic['name'][0],j,dic_help[i]))


# In[2]:



def save_person(csv,graph,num):
    print("正在存储实例，请稍等...")
    row_num=csv.shape[0]
    keys=[]
    for key in csv:
        keys.append(key)
    keys=keys[2:]
    #print(keys)
    dic={}
    for i in range(13253):
        num[0]=i
        for j in range(22):
            dic[keys[j]]=eval(csv.loc[i][keys[j]])
        sentence="MERGE(p:Person"
        for i in dic['type']:
            sentence+=':'+i
        sentence+='{'+'name:'+str(dic['name'])+',IMDb:'+str(dic['IMDb'])
        +',originalName:'+str(dic['originalName'])+',foreignName:'+str(dic['foreignName'])
        +',nickname:'+str(dic['nickname'])+',romanPinyin:'+str(dic['romanPinyin'])+',activeTime:'
        +str(dic['activeTime'])+',debutTime:'+str(dic['debutTime'])+',award:'+str(dic['award'])
        +',language:'+str(dic['language'])+',website:'+str(dic['website'])+',almaMater:'
        +str(dic['almaMater'])+ ',education:'+str(dic['education'])+',religion:'
        +str(dic['religion'])+',ethnicity:'+str(dic['ethnicity'])+',agency:'+str(dic['agency'])+'})'


        graph.run(sentence)
        place('birthPlace',dic,graph)
        place('deathPlace',dic,graph)
        place('nationality',dic,graph)
        works('notableWork',dic,graph)
        works('debutWork',dic,graph)
        works_n(dic,graph)



    print('所有节点存储完毕')


# In[32]:


def save_person_relation(csv,graph,num):
    print("正在存储实例，请稍等...")
    row_num=csv.shape[0]
    keys=[]
    for key in csv:
        keys.append(key)
    keys.pop(0)
    key=keys[-5:-1]

    dic={}
    for i in range(13253):
        num[0]=i
        dic['name']=eval(csv.loc[i]['name'])
        for j in range(4):

            dic[key[j]]=eval(csv.loc[i][key[j]])
        #print(dic)
        for j in range(4):
            person(key[j],dic,graph)
    

    print('所有节点存储完毕')


# In[8]:


g = Graph(auth=('neo4j', 'w2newage'))
#g.run('match(n) detach delete n')


# In[26]:


data = pd.read_csv("graph_ready.csv")
print(data.shape)


# In[27]:


num=[0]
save_person(data,g,num)


# In[33]:


num1=[0]
save_person_relation(data,g,num1)


# In[23]:


print(num)


# In[ ]:




