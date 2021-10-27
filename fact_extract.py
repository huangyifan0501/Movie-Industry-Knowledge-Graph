import pandas as pd
import numpy as np
import utils
from tqdm import tqdm
import os
import regex
from improved_extract import improved_extract

root_dir = '../filtered_data/'
ontology = pd.read_excel('../graph/ontology.xlsx')
fact = {}

data_list=['actor','writer','director']

counters = {'infobox':0, 're':0, 'jiagu':0}

for data in data_list:
    data_dir=root_dir+data

    count = len([lists for lists in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, lists))])
    pbar = tqdm(total=count)
    pbar.set_description("Processing "+data+" pages")

    for f in os.listdir(data_dir):
        page_dir = os.path.join(data_dir, f)
        pbar.update(1)
        page_fact = {}
        page = utils.page_extract(page_dir)
        infobox = utils.infobox_extract(page['text'])

        page_fact['name'] = [page['title']]

        rule={'actor':[['电影','演员'],['协会','处女作','奖']],
              'writer':[['电影','编剧'],['协会','处女作','奖','编剧电影']],
              'director':[['电影','导演'],['协会','处女作','奖','导演电影']],
             }
        page_fact['type'] = utils.type(page_dir, rule)

        for i in range(ontology.shape[0]):
            carry = ontology.loc[i]
            p = carry[0]
            fact_keys = carry[1].split('；')
            re_list = [] if type(carry[2]) == float else carry[2].split('；')
            
            for info in infobox:
                info_keys = list(info.keys())
                for key in info_keys:
                    if key in fact_keys:
                        page_fact[p] = [info[key]]
            
            if p not in page_fact.keys():
                page_fact[p] = []
                for pattern in re_list:
                    re_result = regex.finditer(pattern, page['text'])
                    for item in re_result:
                        page_fact[p].append(item.group())

        # extract by jiagu
        triples = improved_extract(page['text'])
        for triple in triples:
            for i in range(ontology.shape[0]):
                carry = ontology.loc[i]
                p = carry[0]
                fact_keys = carry[1].split('；')
                if triple[1] in fact_keys and len(page_fact[p]) == 0:
                    page_fact[p] = [triple[2]]

        fact[page['id']] = page_fact

fact_df=pd.DataFrame(fact).T
fact_df.to_csv('../graph/graph_base.csv', encoding='utf_8_sig')