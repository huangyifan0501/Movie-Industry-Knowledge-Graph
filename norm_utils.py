import geocoder
import pandas as pd
import numpy as np
import re

def address_norm(initial):
    initial = initial.replace('[', '').replace(']', '')
    result = {}
    
    try:
        g = geocoder.arcgis(initial).latlng
        address = geocoder.arcgis(g, method='reverse')
    except:
        return result
    else:
        result['country']=address.country
        result['state']=address.state
        result['city']=address.city
        return result


def time_norm(str, flag):
    #flag=1时，对出道时间进行规范化；flag=0时，对活跃时期进行规范化
    str=re.findall(r"\d*",str)
    str_list = list(filter(None, str))
    str_nlist=[]
    for i in str_list:
        if len(i)==4:
            str_nlist.append(i)
        elif len(i)==8:
            first=i[:3]
            second=i[4:]
            str_nlist.append(first)
            str_nlist.append(second)
        else:
            continue
        
    result_list=[]

    if len(str_nlist)==0:
        return []
    if flag==1:
        return [str_nlist[0]+'年']

    judge=len(str_nlist)%2
    n=len(str_nlist)//2
    for j in range(n):
        result_list.append(str_nlist[j]+'年-'+str_nlist[j+1]+'年')
    if judge==1:
        result_list.append(str_nlist[2*n]+'年-2021年')

    return result_list


def name_norm(origin_name):
    def process_single_name(name):
        # 去除多余符号
        name = name.strip().replace('-{', '').replace('}-', '')
        if name=='': return None
        pattern = r'(.+?)([(（].*?[)）])' # 去除括号
        match = re.search(pattern, name)
        if match is not None:
            name = match.group(1).strip()
        return name

    if origin_name is None: return []
    # 按顿号拆分
    if '、' in origin_name:
        names = origin_name.split('、')
        result = [process_single_name(name) for name in names]
    else:
        result = [process_single_name(origin_name)]

    result=filter(None, result)
    return list(set(result))


def works_norm(work_list):
    def process_work_list(work):
        work = work.strip().replace('：', '').replace('歌曲','').replace('电视剧','').replace('电影','').replace('连续剧','').replace('音乐','')
        if work=='': 
            return []#
        pattern = r'[\<《](.*?)[\》]'
        match = re.findall(pattern, work)
        if len(match):
            whole_list = match
        else:
            kuohao_pattern = r'(.+?)([(（].*?[)）])'
            kuohao_match = re.findall(kuohao_pattern, work)
            # print('kuohao',kuohao_match)
            if '、' in work:
                whole_list= work.split('、')
            elif '，' in work:
                whole_list= work.split('，')
            elif len(kuohao_match):
                whole_list = [kuohao_match[i][0] for i in range(len(kuohao_match))]
            else:
                whole_list=[work] 
            
        for i in range(len(whole_list)):
            whole_list[i] = '《'+ whole_list[i]+ '》'
        return whole_list

    if work_list is None: 
        return []

    result = process_work_list(work_list) 
    return list(set(result))


def award_norm(award_list):
    def process_award_list(award):
        if award=='':
            return []
        # 判断是否包含中文
        pattern0 = r'[\u4e00-\u9fa5]'
        match0 = re.search(pattern0, award)
        if not match0:
            return []
        # 去除括号和书名号中的内容
        pattern = r'([\<《](.*?)[\》])'
        pattern2 = r'([\<（|\(](.*?)[\）|\)])'
        match = re.findall(pattern, award)
        match = [ele[0] for ele in match]
        match2 = re.findall(pattern2, award)
        match2 = [ele[0] for ele in match2]
        for element in match:
            award = award.replace(element, ' ')
        for element in match2:
            award = award.replace(element, ' ')
        # 去除年份
        pattern3 = r'[0-9]+年'
        match3 = re.findall(pattern3, award)
        for element in match3:
            award = award.replace(element, ' ')
        # 删去多余符号
        award = award.replace('了', '')
        award = award.replace('和', ' ')
        award = award.replace('；', '')
        award = award.replace('，', '')
        award = award.replace('、', '')
        award = award.replace('-', '')
        award = award.replace('「', ' ')
        award = award.replace('」', ' ')
        whole_list = award.split()
        useless = ['的奖', '颁奖', '项奖', '次奖', '等奖', 
                    '此奖', '奖项', '获奖', '该奖', '之奖', 
                    '个奖', '冠军', '季军', '亚军', '个']
        useful = ['奖', '最', '小姐', '先生']
        for ul in useless:
            for ele in whole_list:
                if len(ele) <=2:
                    whole_list.remove(ele)
                elif ul in ele:
                    whole_list.remove(ele)
        for ele in whole_list:
            check = False
            for uf in useful:
                if uf in ele:
                    check = True
            if check == False:
                whole_list.remove(ele)
        return whole_list

    if award_list is None:
        return []

    result = process_award_list(award_list)
    return list(set(result))

